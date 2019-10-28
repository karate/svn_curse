from configparser import ConfigParser

class Config():

    def __init__(self, filename):
        self.config = ConfigParser()
        self.config.read(filename)

    def get_colors(self):
        return self.config['COLORS']

