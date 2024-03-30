from models.text import Text
from utils.constants import HSTEP, VSTEP
from utils.font import get_font


class Layout:
    def __init__(self, tokens, canvas_width):
        self.tokens = tokens
        self.canvas_width = canvas_width
        self.display_list = []

        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        self.center = False

        self.line = []
        for tok in tokens:
            self.token(tok)
        self.flush()

    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP
        elif tok.tag == 'h1 class="title"':
            self.flush()
            self.size += 8
            self.center = True
            self.weight = "bold"
        elif tok.tag == "/h1":
            if self.center:
                self.flush()
                self.size -= 8
                self.center = False
                self.weight = "normal"

    def word(self, word):
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        # TODO: Text is not centered correctly, for example, formatting text is leans to the right
        # since w is just the width of the first word which is not the same as the width of the whole line
        if self.center and self.cursor_x == HSTEP:
            self.cursor_x = (self.canvas_width / 2) - w / 2
        if self.cursor_x + w > self.canvas_width - HSTEP:
            self.flush()
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")

    def flush(self):
        """
        Three responsibilities:
            - Align the words along the baseline
            - Add all those words to the display list
            - Update the cursor_x and cursor_y fields
        Note: Ascent is the distance from the baseline to the top of the font
        Note: Descent is the distance from the baseline to the bottom of the font
        """
        if not self.line:
            return
        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = HSTEP
        self.line = []
