import tkinter
import tkinter.font
from models.layout import Layout
from utils.constants import HEIGHT, SCROLL_STEP, VSTEP, WIDTH
from utils.lexer import lex

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
        )
        self.canvas.pack(fill=tkinter.BOTH, expand=True)

        self.scroll = 0
        self.tokens = []
        self.display_list = []

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
            max_y = max(y for _, y, _, _ in self.display_list)
            return max(0, max_y - self.canvas.winfo_height())
        return 0

    def on_resize(self, event):
            self.display_list = Layout(self.tokens, event.width).display_list
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        height = self.canvas.winfo_height()
        for x, y, word, font in self.display_list:
            if y > self.scroll + height: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=word, font=font, anchor="nw")

    def load(self, url):
        body, view_source = url.request()
        self.tokens = lex(body, view_source)
        self.display_list = Layout(self.tokens, self.canvas.winfo_width()).display_list
        self.draw()
