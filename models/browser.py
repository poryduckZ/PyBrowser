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
        self.canvas.pack(fill=tkinter.BOTH, expand=True)
        self.scroll = 0
        self.text = ""
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.window.bind("<Configure>", self.on_resize)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        if self.scroll > 0:
            self.scroll -= SCROLL_STEP
            self.draw()

    def on_mousewheel(self, e):
        self.scroll -= e.delta;
        self.scroll = max(self.scroll, 0) # Prevent scrolling past the top
        self.scroll = min(self.scroll, self.max_scroll()) # Prevent scrolling past the bottom
        self.draw()

    def max_scroll(self):
        if self.display_list:
            max_y = max(y for _, y, _ in self.display_list)
            return max(0, max_y - self.canvas.winfo_height())
        return 0

    def on_resize(self, event):
            self.display_list = layout(self.text, event.width)
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        height = self.canvas.winfo_height()
        for x, y, c in self.display_list:
            if y > self.scroll + height: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        body, view_source = url.request()
        self.text = lex(body, view_source)
        self.display_list = layout(self.text, self.canvas.winfo_width())
        self.draw()


def layout(text, width):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if c == "\n":
            cursor_y += (VSTEP * 1.15)
            cursor_x = HSTEP
            continue
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= width - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list
