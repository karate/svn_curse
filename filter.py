"""
Module responsible for creating line objects and filtering.
"""
from line import Line
from config import Config


class Filter:
    """ Filter class"""
    def __init__(self, screen, colors):
        # Load colors from config
        self._colors = Config.colors

        # Assign colors
        self.screen = screen
        self.color_codes = {
            'added': colors[self._colors['added']],
            'normal': colors[self._colors['normal']],
            'unversioned': colors[self._colors['unversioned']],
            'incomplete': colors[self._colors['incomplete']],
            'missing': colors[self._colors['missing']],
            'deleted': colors[self._colors['deleted']],
            'modified': colors[self._colors['modified']],
            'ignored': colors[self._colors['ignored']],
            'remote': colors[self._colors['remote']],
        }

    def filter_local_files(self, files):
        """ Filter given local files"""
        lines = []
        for idx, _file in enumerate(files):
            filename = _file.name
            status = _file.type_raw_name
            line = self.construct_line(filename, status, idx+1)
            lines.append(line)
        return lines

    def filter_remote_repo(self, files):
        """ Filter given remote files"""
        lines = []
        for idx, _file in enumerate(files):
            line = self.construct_line(_file['path'], _file['status'], idx+1)
            lines.append(line)
        return lines

    def construct_line(self, filename, status, idx):
        """ Construct line object"""
        color = self.color_codes[status]
        return Line(idx, filename, self.screen, color)
