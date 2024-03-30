from models.tag import Tag
from models.text import Text


def lex(body, view_source=False):
    # TODO: Entities support (e.g. &lt; &gt;)
    # body = body.replace("&lt;", "<").replace("&gt;", ">")
    if view_source:
        return body

    out = []
    buffer = ""
    in_tag = False

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
        else:
            buffer += c
    if not in_tag and buffer:
            out.append(Text(buffer))
    return out
