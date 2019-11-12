"""
Curses Class responsible to draw curses UI.
"""
import curses
from filter import Filter
from line import Line
from log import debug_start_done, get_logger

logger = get_logger()


class Curse:
    """Curses class."""
    def __init__(self):
        # Initialize screen
        self.screen = curses.initscr()
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()

        # Initialize and define colors
        self._set_colors()

        # Initial Class values
        self.status_line = ""
        self.selected = None
        self.previously_selected = None
        self.previous = None
        self.working_copy = None
        self.mlines, self.mcols = self.screen.getmaxyx()
        self.status_line_position = self.mlines - 1

        self.lines = []

    def _set_colors(self):
        """Set color codes."""
        curses.start_color()
        curses.use_default_colors()
        # Normal colors
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)
        curses.init_pair(6, curses.COLOR_BLACK, -1)
        # Inverted colors, for selected items
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self.colors = {
            "white":  [curses.color_pair(1), curses.color_pair(7)],
            "red":    [curses.color_pair(2), curses.color_pair(8)],
            "green":  [curses.color_pair(3), curses.color_pair(9)],
            "blue":   [curses.color_pair(4), curses.color_pair(10)],
            "yellow": [curses.color_pair(5), curses.color_pair(11)],
            "black":  [curses.color_pair(6), curses.color_pair(12)],
        }

    def _clear_selection(self):
        """Clear selected and previously selected items."""
        self.selected = None
        self.previously_selected = None

    def update_status_line(self, text):
        """Update status line with given text."""
        text = text.ljust(self.mcols)
        _line = Line(0, text, self.screen, [curses.A_REVERSE, None])
        _line.print()
        self.screen.refresh()

    def print_local_files(self, files):
        """Print given local files."""
        _filter = Filter(self.screen, self.colors)
        self.lines = _filter.filter_local_files(files)
        self.print_lines()

    def print_remote_files(self, files):
        """Print given remote files."""
        self._clear_selection()
        _filter = Filter(self.screen, self.colors)
        self.lines = _filter.filter_remote_repo(files)
        self.print_lines()

    def print_lines(self):
        """Print lines."""
        if len(self.lines) == 0:
            self.update_status_line(' * Nothing to show * ')
        else:
            if self.selected is None:
                self.selected = len(self.lines) - 1

            if self.previously_selected is not None:
                self.lines[self.previously_selected].set_selected(False)

            self.lines[self.selected].set_selected()

            for line in self.lines:
                line.print()

        self.screen.refresh()

    def quit(self):
        """Quit curses."""
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    @debug_start_done
    def go_down(self):
        """Navigate down."""
        if self.selected is not None:
            self.previously_selected = self.selected

        if self.selected < 1:
            self.selected = len(self.lines) - 1
        else:
            self.selected = self.selected - 1
        logger.debug("go_down selected: {} {}".format(self.selected,
                                                      self.lines[self.selected]))
        self.print_lines()

    @debug_start_done
    def go_up(self):
        """Navigate up."""
        if self.selected is not None:
            self.previously_selected = self.selected

        if self.selected > (len(self.lines) - 2):
            self.selected = 0
        else:
            self.selected = self.selected + 1
        logger.debug("go_down selected: {} {}".format(self.selected,
                                                      self.lines[self.selected]))
        self.print_lines()
