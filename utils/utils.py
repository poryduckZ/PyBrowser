def show(body):
    in_tag = False
    # Example: <a href="http://www.example.com">Example</a>
    #          ^ in_tag = True                 ^ in_tag = False, print "Example"
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    body = url.request()
    show(body)
