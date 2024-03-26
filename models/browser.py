import tkinter
from utils.utils import lex

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 12, 16
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        if self.scroll > 0:
            self.scroll -= SCROLL_STEP
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        body, view_source = url.request()
        text = lex(body, view_source)
        self.display_list = layout(text)
        self.draw()


def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if c == "\n":
            cursor_y += (VSTEP * 1.15)
            cursor_x = HSTEP
            continue
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list
