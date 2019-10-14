class Dir():
    def __init__(self, client):
        self.client = client
        self.previous = None

    def ls(self, directory):
        files = []
        try:
            results = sorted(self.client.list(directory), reverse=True)
            if not results:
                return False

            for file in results:
                files.append({'path': file[0].repos_path, 'status': 'remote'})
        except:
            return None

        return files
