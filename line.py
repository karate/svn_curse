import curses


class Line():
    def __init__( self, idx, text, screen, colors ):
        self.text = text
        self.text = text
        self.colors = colors
        self.color = colors[0]
        self.screen = screen
        self.selected = False
        (self.mlines, self.mcols) = self.screen.getmaxyx()
        self.y = self.mlines - idx - 2

    def __str__(self):
        return self.text

    def print( self ):
        if self.selected:
            self.color = self.colors[1]
        else:
            self.color = self.colors[0]
        try:
            self.clear_line(self.y)
            self.screen.addstr(self.y, 0, self.text, self.color)
        except curses.error as e:
            pass

    def clear_line(self, line_no):
        try:
            self.screen.addstr(line_no, 0, ' '.ljust(self.mcols, ' '))
        except curses.error as e:
            pass

    def set_selected( self, selected = True ):
        self.selected = selected

    def get_text( self ):
        return self.text
