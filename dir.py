class Dir(object):
    def __init__ ( self, client ):
        self.client = client
        self.previous = None

    def ls(self, rel=None):
        files = []
        try:
            list = sorted(self.client.list(rel_path=rel), reverse=True)
            if not list:
                return False

            for file in list:
                files.append({'path': file, 'status': 'remote'})
        except:
            return None

        return files
