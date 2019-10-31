from line import Line
from config import Config


class Filter():
    def __init__(self, screen, colors):
        # Load colors from config
        self.COLORS = Config.colors

        # Assign colors
        self.screen = screen
        self.color_codes = {
            'added': colors[self.COLORS['added']],
            'normal': colors[self.COLORS['normal']],
            'unversioned': colors[self.COLORS['unversioned']],
            'incomplete': colors[self.COLORS['incomplete']],
            'missing': colors[self.COLORS['missing']],
            'deleted': colors[self.COLORS['deleted']],
            'modified': colors[self.COLORS['modified']],
            'ignored': colors[self.COLORS['ignored']],
            'remote': colors[self.COLORS['remote']],
        }

    def filter_local_files (self, files):
        lines = []
        for idx, f in enumerate(files):
            filename = f.name
            status = f.type_raw_name
            line = self.construct_line( filename, status, idx+1 )
            lines.append( line )
        return lines

    def filter_remote_repo (self, files):
        lines = []
        for idx, f in enumerate(files):
            line = self.construct_line(f['path'], f['status'], idx+1)
            lines.append(line)
        return lines

    def construct_line(self, filename, status, idx):
        color = self.color_codes[status]
        return Line( idx, filename ,self.screen, color )
