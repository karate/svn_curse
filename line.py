"""
Line module.
"""
from curses import error


class Line:
    """ Line class"""
    def __init__(self, idx, text, screen, colors):
        self.text = text
        self.colors = colors
        self.color = colors[0]
        self.screen = screen
        self.selected = False
        self.mlines, self.mcols = self.screen.getmaxyx()
        self._y = self.mlines - idx - 2

    def __str__(self):
        return self.text

    def print(self):
        """ Print on curses ui"""
        if self.selected:
            self.color = self.colors[1]
        else:
            self.color = self.colors[0]
        try:
            self.clear_line(self._y)
            self.screen.addstr(self._y, 0, self.text, self.color)
        except error:
            pass

    def clear_line(self, line_no):
        """ Clear line"""
        try:
            self.screen.addstr(line_no, 0, ' '.ljust(self.mcols, ' '))
        except error:
            pass

    def set_selected(self, selected=True):
        """ Set selected"""
        self.selected = selected

    def get_text(self):
        """ Get text"""
        return self.text
