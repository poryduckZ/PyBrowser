def lex(body, view_source=False):
    text = ""
    in_tag = False
    body = body.replace("&lt;", "<").replace("&gt;", ">")
    if view_source:
        return body
    # Example: <a href="http://www.example.com">Example</a>
    #          ^ in_tag = True                 ^ in_tag = False, print "Example"
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
    return text
