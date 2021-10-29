from coldtype import *
from coldtype.time.nle.ascii import AsciiTimeline

at = AsciiTimeline(4, """
                                <
[B   ]    [B       ]
            [A          ]
                [C         ]
                    [wght     ]
""")

print(at.clips)

@animation((1080, 540), timeline=at, bg=0.97, render_bg=1)
def ascii(f):
    def wdth(g):
        return at.get_at(g.c, f.i).io2(f.i, 8, "eeio")

    return (Glyphwise("ABC", lambda g:
        Style(Font.MutatorSans(), 250,
            wdth=wdth(g),
            wght=at["wght"].io2(f.i, 10, "eeio")))
        .align(f.a.r))
