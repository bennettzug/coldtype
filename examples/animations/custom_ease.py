from coldtype import *
from coldtype.fx.xray import skeleton

@animation(timeline=60, bg=1)
def easer(f):
    p = P().withRect(1000, lambda r, p: p
        .m(r.psw)
        .ioc(r.pn, 5, 50)
        .ioc(r.pse, 15, 50))
    
    return PS([
        (p.copy()
            .scaleToWidth(f.a.r.w-50)
            .align(f.a.r)
            .layerv(
                lambda p: p.fssw(-1, hsl(0.9), 2),
                lambda p: p.ch(skeleton(scale=1.5)).s(hsl(0.65)))),
        (StSt("COLD", Font.ColdtypeObviously()
            , 300
            , wdth=f.e(p, 0))
            .align(f.a.r)
            .f(0, 0.5))])