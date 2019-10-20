#! /usr/bin/env python3
import sys
import os
import dir
import curse
from svn import local

from exceptions import QuitSignal


def _get_working_copy( argv ):
    if (len(argv) > 1):
        cwd = argv[1]
    else:
        cwd = os.getcwd()
    return cwd


def main():
    base = _get_working_copy(sys.argv)
    client = local.LocalClient(base)
    client.callback_get_login = login_handler

    nav = Navigation(client, base)
    nav.main_nav()


class Navigation(object):
    def __init__(self, client, base):
        self.c = curse.Curse()
        self._client = client
        self._base = base
        self._nav_path = [self._base]

    @property
    def path(self):
        return os.path.join(*self._nav_path)

    def input_main(self):
        try:
            while True:
                ch = self.c.screen.getch()
                if ch == ord('r'):
                    self.browse_repo()
                elif ch == ord('w'):
                    self.view_status(self._base)
                elif ch == ord('q'):
                    raise QuitSignal("Exit from input_main.")
        except QuitSignal:
            self.c.quit()

    def input_nav(self):
        try:
            while True:
                cha = self.c.screen.getch()
                if cha == ord('q'):
                     raise QuitSignal("Quit from input_nav.")
                elif cha == ord('j'):
                    self.c.go_down()
                elif cha == ord('k'):
                    self.c.go_up()
                elif cha == ord('l'):
                    self._append()
                    self.browse_repo(self.path)
                elif cha == ord('h'):
                    self._remove()
                    self.browse_repo(self.path)
        except QuitSignal:
            self.c.quit()
            sys.exit(0)

    def base_status(self, text):
        self.c.update_status_line(text + " - j/k: up/down, l/h: in/out q: quit")

    def main_nav(self):
        self.c.update_status_line("w: view working copy status, r: browse remote repo, q: quit")
        self.input_main()

    def view_status(self, working_copy):
        self.c.update_status_line("status loading...")
        files = self._client.status()

        self.base_status(working_copy)
        self.c.print_local_files(files)

        self.input_nav()

    def browse_repo(self, rel=None):
        self.c.update_status_line("browse loading...")
        d = dir.Dir(self._client)
        files = d.ls(rel)
        if files is None:
            self.c.update_status_line(os.path.join(self._base, rel) + " - Not under version control. q: quit")
        else:
            self.base_status(self.path)
            self.c.print_remote_files(files)

        self.input_nav()

    def _append(self):
        if self.c.selected:
            self._nav_path.append(str(self.c.lines[self.c.selected]).strip('/'))

    def _remove(self):
        if len(self._nav_path) > 1:
            self._nav_path = self._nav_path[:-1]


def login_handler(*args):
    # TODO: Use python keyring

    # hard-code credentials
    # return True, "username", "password", True

    # or prompt user
    user = input( "Username: " )
    passw = getpass.getpass( "Password: " )
    return True, user, passw, True


if __name__ == '__main__':
    main()
