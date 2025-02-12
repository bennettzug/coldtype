from coldtype import *
from coldtype.drawbot import *

co = Font("assets/ColdtypeObviously.designspace")

long_txt = """This code is a mix of DrawBot and Coldtype, meant to demonstrate that Coldtype primitives (like designspace-reading) can be combined with DrawBot primitives like multi-line text support and the Mac Font library."""

@drawbot_renderable(rect=(900, 500), bg=0)
def composition(r):
    ri = r.inset(20, 20)

    db.fill(*hsl(0.5))
    db.oval(*ri.take(0.5, "mxx").square())

    im = db.ImageObject()
    with im:
        db.size(500, 500)
        db.image("https://static.goodhertz.co/statics/store/img/logos/hertz-color-danico-250-lssy.png", (0, 0))
        im.photoEffectMono()
    
    x, y = im.offset()
    db.image(im, (250+x, -10+y))

    db.fontSize(19)
    db.font("Georgia-Italic")
    db.fill(*hsl(0.9, s=0.7, l=0.6))
    db.textBox(long_txt, ri.take(200, "mny").take(250, "mnx"))

    (StSt("COLDTYPE", co, 150, ro=1)
        .align(ri, "mnx", "mxy")
        .f(Gradient.Horizontal(ri,
            hsl(0.05, s=0.7, l=0.6),
            hsl(0.15, s=0.7, l=0.6)))
        .s(0)
        .sw(3)
        | dbdraw)
    
    (StSt("COLDTYPE", co, 50, ro=1, r=1, tu=-100)
        .align(ri, "mnx", "mdy")
        .translate(0, 40)
        .f(0)
        .understroke(s=1, sw=5)
        | dbdraw)


"""
When you’re ready to create a PDF, just hit the "R" key in the viewer app
"""

def release(_):
    db.saveImage("~/Desktop/composition.pdf")