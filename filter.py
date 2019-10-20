from line import Line


class Filter():
    def __init__( self, screen, colors ):
        self.screen = screen
        self.color_codes = {
            'added': colors['white'],
            'normal': colors['white'],
            'unversioned': colors['green'],
            'incomplete': colors['yellow'],
            'missing': colors['red'],
            'deleted': colors['red'],
            'modified': colors['blue'],
            'ignored': colors['yellow'],
            'remote': colors['yellow'],
        }

    def filter_local_files ( self, files ):
        lines = []
        for idx, f in enumerate(files):
            filename = f.name
            status = f.type_raw_name
            line = self.construct_line( filename, status, idx+1 )
            lines.append( line )
        return lines

    def filter_remote_repo ( self, files ):
        lines = []
        for idx, f in enumerate(files):
            line = self.construct_line(f['path'], f['status'], idx+1)
            lines.append(line)
        mlines, _ = self.screen.getmaxyx()
        for i in range(len(files), mlines):
            line = self.construct_line(' ', 'remote', i+1)
            lines.append(line)
        return lines

    def construct_line( self, filename, status, idx ):
        color = self.color_codes[status]
        return Line( idx, filename ,self.screen, color )
