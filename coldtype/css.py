from coldtype.geometry.rect import Rect
from coldtype.color import hsl
from coldtype.pens.runonpen import RunonPen


def cubicBezier(x1, y1, x2, y2):
    p = RunonPen()
    p.moveTo((0, 0))
    p.curveTo(
        (x1*1000, y1*1000),
        (x2*1000, y2*1000),
        (1000, 1000))
    p.endPath()
    p.data(frame=Rect(1000, 1000))
    return p.fssw(-1, hsl(0.6), 2)