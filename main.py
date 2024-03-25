import tkinter
from models.url import URL
from models.browser import Browser

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
    elif len(sys.argv) == 2:
        Browser().load(URL(sys.argv[1]))
        tkinter.mainloop()
