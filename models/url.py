import socket
import ssl

class URL:
    """
    URL is defined as:
    scheme "://" host [ ":" port ] [ "/" path ]
    scheme is http or https
    host is the domain name
    port is the port number, default is 80 for http and 443 for https
    path is the path to the resource on the server
    Example: http://www.example.com:8080/path/to/resource
    """
    def __init__(self, url):
        if url.startswith("data"):
            self.scheme = "data"
            if "," in url:
                mine_type, data = url.split(",", 1)
                self.data = data
        else:
            self.view_source = False
            if url.startswith("view-source:"):
                self.view_source = True
                url = url[len("view-source:"):]
            self.scheme, url = url.split("://", 1)
            assert self.scheme in ["http", "https", "file"]
            if self.scheme == "file":
                self.path = url
                return
            elif self.scheme == "http":
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
        if self.scheme == "file":
            try:
                f = open(self.path, "r", encoding="utf-8")
                content = f.read()
                f.close()
                return content, False
            except FileNotFoundError:
                return "File not found"

        if self.scheme == "data":
            return self.data, False

        if self.scheme in ["http", "https"]:
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

            request_headers = {
                "Host": self.host,
                "Connection": "close", # Connection will close after the response
                "User-Agent": "PythonBrowser/0.1", # Identifies the browser to the host
            }

            request_lines = [f"GET {self.path} HTTP/1.1"]
            request_lines.extend(["{}: {}".format(header, value) for header, value in request_headers.items()])
            request_message = "\r\n".join(request_lines) + "\r\n\r\n"
            s.send(request_message.encode("utf-8"))

            # Note: utf8 is not correct
            # but it’s a shortcut that will work on most English-language websites
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
            return body, self.view_source
