class Dir(object):
    def __init__ ( self, client ):
        self.client = client
        self.previous = None

    def ls( self, dir ):
        files = []
        try:
            list = sorted(self.client.list(), reverse=True)
            if not list:
                return False

            for file in list:
                files.append({'path': file, 'status': 'remote'})
        except:
            # add log
            return None

        return files
