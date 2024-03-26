import tkinter
import tkinter.font

from models.tag import Tag
from models.text import Text

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 12, 16
SCROLL_STEP = 100

def lex(body, view_source=False):
    out = []
    buffer = ""
    in_tag = False
    body = body.replace("&lt;", "<").replace("&gt;", ">")
    if view_source:
        return body
    # Example: <a href="http://www.example.com">Example</a>
    #          ^ in_tag = True                 ^ in_tag = False, print "Example"
    for c in body:
        if c == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        elif not in_tag:
            buffer += c
    if not in_tag and buffer:
            out.append(Text(buffer))
    return out


FONTS = {}

def get_font(size, weight, slant):
    key = (size, weight, slant)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight,
            slant=slant)
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]
