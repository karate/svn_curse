import pysvn
from line import Line

class Filter():
    def __init__( self, screen, colors ):
        self.screen = screen
        self.color_codes = {
            pysvn.wc_status_kind.added       : colors['white'],
            pysvn.wc_status_kind.unversioned : colors['green'],
            pysvn.wc_status_kind.missing     : colors['red'],
            pysvn.wc_status_kind.deleted     : colors['red'],
            pysvn.wc_status_kind.modified    : colors['blue'],
            pysvn.wc_status_kind.ignored     : colors['yellow'],
            'remote'                         : colors['yellow'],
        }

    def filter_local_files ( self, files ):
        lines = []
        for idx, f in enumerate(files):
            filename = f.path
            status = f.text_status
            line = self.construct_line( filename, status, idx+1 )
            lines.append( line )
        return lines

    def filter_remote_repo ( self, files ):
        lines = []
        for idx, f in enumerate(files):
            filename = f['path']
            status = f['status']
            line = self.construct_line( filename, status, idx+1 )
            lines.append( line )
        return lines

    def construct_line( self, filename, status, idx ):
        color = self.color_codes[status]
        return Line( idx, filename ,self.screen, color )
