import socket

class URL:
    # Scheme is separated from the rest of the URL by ://
    # Only supports http
    # Host comes before the first /, the path is that slash and everything after it
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http"
        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url

    def request(self):
        # Socket has an address family and it begins with AF
        # Socket has a type, for example SOCK_STREAM and SOCK_DGRAM
        # Socket has a protocol and it has names that depends on address family
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, 80))
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
