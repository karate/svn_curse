import pysvn
import sys
import getpass

class Dir():
    def __init__ ( self, client ):
        self.client = client
        self.previous = None;

    def ls( self, dir ):
        files = []
        try:
            list = sorted(self.client.list( dir ), reverse=True)
            if ( len( list ) == 0 ):
                return False

            for file in list:
                files.append({'path': file[0].repos_path, 'status': 'remote'})
        except:
            return None

        return files
