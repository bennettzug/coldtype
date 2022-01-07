import re

from coldtype.sh.context import SHContext
from coldtype.sh import SH_UNARY_SUFFIX_PROPS, sh, SHContext
from coldtype.geometry import Point, Rect, Curve


class ShorthandMixin(SHContext):
    def __init__(self):
        SHContext.__init__(self)

        self.defs = None
        self.macros = {}
    
    def define(self, *args, **kwargs):
        return self.context_record("$", "defs", None, *args, **kwargs)
    
    def declare(self, *whatever):
        # TODO do something with what's declared somehow?
        return self
    
    def macro(self, **kwargs):
        for k, v in kwargs.items():
            self.macros[k] = v
        return self
    
    def sh(self, s, subs={}):
        if not self.val_present():
            return self

        try:
            start = self._val.value[0][1][-1]
        except:
            start = None
        #print("SH", s, self.defs)
        res = sh(s, self, subs={"¬":self._last, "§":start, **subs})
        if res[0] == "∫":
            res = [type(self)().gs(res[1:])]
        return res
    
    def gss(self, s):
        dps = type(self)()
        sh(s, ctx=self, dps=dps)
        for p in dps._els:
            self.record(p)
        return self
    
    def ez(self, r, start_y, end_y, s):
        self.moveTo(r.edge("W").t(start_y))
        self.gs(s, do_close=False, first_move="lineTo")
        self.lineTo(r.edge("E").t(end_y))
        self.endPath()
        return self
    
    def gs(self, s, fn=None, tag=None, writer=None, ctx=None, dps=None, macros={}, do_close=True, first_move="moveTo"):
        ctx = ctx or self
        macros = {**self.macros, **macros}

        def expand_multisuffix(m):
            out = []
            arrows = list(m.group(2))
            for a in arrows:
                out.append(m.group(1)+a)
            return " ".join(out)

        def sp(_s):
            return [x.strip() for x in re.split(r"[\s\n]+", _s)]

        if isinstance(s, str):
            s = s
            s = re.sub(r"([\$\&]{1}[a-z]+)([↖↑↗→↘↓↙←•⍺⍵µ]{2,})", expand_multisuffix, s)
            #e = sh(s, ctx, dps)
            moves = sp(s)
        else:
            e = s
            moves = sp(e)
        
        def one_move(_e, move="lineTo"):
            #print("ONE_MOVE", _e, move)
            if _e is None:
                return
            elif isinstance(_e, Point):
                getattr(self, move)(_e)
            elif isinstance(_e, Rect):
                self.rect(_e)
            elif isinstance(_e, Curve):
                _, b, c, d = _e
                self.curveTo(b, c, d)
            elif isinstance(_e, str):
                getattr(self, _e)()
            elif _e[0][0] == "∑":
                    macro = "".join(_e[0][1:])
                    if macro in macros:
                        macro_fn = macros[macro]
                        macro_fn(self, *_e[1:])
                    else:
                        raise Exception("unrecognized macro '" + macro + "'")
            elif _e[1] == "eio":
                if len(_e) > 2:
                    self.ioEaseCurveTo(_e[0], *_e[2:])
                else:
                    self.ioEaseCurveTo(_e[0])
            else:
                if len(_e) >= 5:
                    self.interpCurveTo(*_e)
                else:
                    self.boxCurveTo(*_e)

        locals = {}
        mvs = [moves[0]]
        if isinstance(mvs[0], str):
            res = sh(mvs[0], ctx, dps)
        else:
            res = [mvs[0]]
        one_move(res[0], move=first_move)

        try:
            start = self._val.value[0][1][-1]
        except:
            start = None

        for _m in moves[1:]:
            last = self._last
            ctx._last = last
            if isinstance(_m, str):
                res = sh(_m, ctx, dps, subs={"¬":last,"§":start})
            else:
                res = [_m]
            if res:
                one_move(res[0], move="lineTo")
        
        if self.unended() and do_close:
            self.closePath()

        if tag:
            self.tag(tag)
        if fn:
            fn(self)
        return self
    
    def shprop(self, s):
        if s in SH_UNARY_SUFFIX_PROPS:
            return SH_UNARY_SUFFIX_PROPS[s]
        return s