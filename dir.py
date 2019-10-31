"""
Dir class.
"""


class Dir:
    """ Dir class"""
    def __init__(self, client):
        self.client = client
        self.previous = None

    def list(self, rel=None):
        """ It lists the given rel path based on clients base path"""
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
