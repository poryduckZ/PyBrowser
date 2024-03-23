import socket
import ssl

class URL:
    # Scheme is separated from the rest of the URL by ://
    # Only supports http
    # Host comes before the first /, the path is that slash and everything after it
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self):
        # Socket has an address family and it begins with AF
        # Socket has a type, for example SOCK_STREAM and SOCK_DGRAM
        # Socket has a protocol and it has names that depends on address family
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        s.send(("GET {} HTTP/1.0\r\n".format(self.path) +\
            "HOST: {}\r\n\r\n".format(self.host)).encode("utf-8"))
        # Note: utf8 is not correct but it’s a shortcut that will work on most English-language websites
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        body = response.read()
        s.close()
        return body

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

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))
