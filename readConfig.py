def readConfig(path):
    try:
        file = open(path, 'r')
        colors = [file.readline().replace('\n', '').replace('colors: ', '')]
        svn_username = [file.readline().replace('\n', '').replace('svn_username: ', '')]
        keybindings = [file.readline().replace('\n', '').replace('keybindings: ', '')]
        return [None, colors, svn_username, keybindings]
    except:
        colors = ['red', 'blue', 'green']
        svn_username = []
        keybindings = ['j/k', 'w', 'r']
        return ['file not found', colors, svn_username, keybindings]

