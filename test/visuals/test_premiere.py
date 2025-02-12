from coldtype import *
from coldtype.time.nle.premiere import PremiereTimeline

pp = Path("test/visuals/media/test_premiere_coldtype.json")
tl = PremiereTimeline(pp)

co = Font.Cacheable("assets/ColdtypeObviously-VF.ttf")
recmono = Font.Cacheable("assets/RecMono-CasualItalic.ttf")

@animation(timeline=tl, bg=0, watch=[pp])
def render(f):
    def render_clip_fn(tc):
        if "coldtype" in tc.clip.styles:
            style = tc.clip.style_matching("coldtype")
            e = style._progress(f.i, easefn="eei").e
            return tc.text.upper(), Style(co, 200, wdth=0.5, tu=-150+e*150, rotate=e*360)
        if tc.text == "!":
            return tc.text, Style(recmono, 200, xShift=-30, rotate=-5)
        return tc.text, Style(recmono, 72)

    cg = tl.clip_group(0, f, styles=[1])
    pens = (cg
        .pens(f, render_clip_fn, f.a.r)
        .f(1)
        .xa()
        .align(f.a.r)
        .remove_futures())
    
    for clip, pen in pens.iterate_clips():
        if "coldtype" in clip.styles:
            pen.f(hsl(0.57, s=0.6, l=0.6)).understroke(sw=10)
    
    if zoom := cg.style_matching("zoom"):
        e = zoom._progress(f.i, easefn="eei").e
        pens.scale(1+pow(e, 2)*150, point=f.a.r.point("C").offset(0, 51))
    
    return pens