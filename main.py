#! /usr/bin/env python3
"""
Main module
This is a proof-of-concept command-line svn client with ncurses, written in python.
"""
import sys
import os
import curse
import traceback
from svn import local
from config import Config
from dir import Dir

from exceptions import QuitSignal
from log import get_logger, debug_start_done

logger = get_logger()


def _get_working_copy(argv):
    if len(argv) > 1:
        cwd = argv[1]
    else:
        cwd = os.getcwd()
    return cwd


@debug_start_done
def main():
    """Main function."""
    logger.info('Program started.')
    try:
        base = _get_working_copy(sys.argv)
        client = local.LocalClient(base)
        client.callback_get_login = login_handler

        nav = Navigation(client, base)
        nav.base_status()
        nav.input_nav()
    except OSError as exc:
        logger.error(traceback.format_exc())
        print(exc)
        sys.exit(1)
    except Exception:
        logger.error(traceback.format_exc())
    logger.info('Program done.')


class NavigationStatus:
    """Navigation status class."""
    def __init__(self):
        self._map = {
            Config.keys['up']: 'up',
            Config.keys['down']: 'down',
            Config.keys['enter_dir']: 'enter directory',
            Config.keys['back']: 'previous directory',
            Config.keys['view_status']: 'view working copy status',
            Config.keys['browse_repo']: 'browse remote repo',
            Config.keys['revert_file']: 'revert file',
            Config.keys['quit']: 'quit'
        }
        self.text = None
        self.enter_previous = True
        self.main = True
        self.text_only = False

    def shortcuts_(self, navigation):
        """Shortcuts masking function."""
        nav_menu = {}

        if self.text:
            self.main = False
        if self.main:
            nav_menu[Config.keys['view_status']] = self._map[Config.keys['view_status']]
            nav_menu[Config.keys['browse_repo']] = self._map[Config.keys['browse_repo']]
            nav_menu[Config.keys['quit']] = self._map[Config.keys['quit']]
        else:
            if navigation.mode == 'local':
                nav_menu[Config.keys['up']] = self._map[Config.keys['up']]
                nav_menu[Config.keys['down']] = self._map[Config.keys['down']]
                nav_menu[Config.keys['enter_dir']] = self._map[Config.keys['enter_dir']]
                nav_menu[Config.keys['back']] = self._map[Config.keys['back']]
                nav_menu[Config.keys['revert_file']] = self._map[Config.keys['revert_file']]
                nav_menu[Config.keys['quit']] = self._map[Config.keys['quit']]
            elif navigation.mode == 'remote':
                nav_menu[Config.keys['up']] = self._map[Config.keys['up']]
                nav_menu[Config.keys['down']] = self._map[Config.keys['down']]
                nav_menu[Config.keys['enter_dir']] = self._map[Config.keys['enter_dir']]
                nav_menu[Config.keys['back']] = self._map[Config.keys['back']]
                nav_menu[Config.keys['quit']] = self._map[Config.keys['quit']]

            if not navigation.history:
                nav_menu.pop(Config.keys['back'])

        nav_menu = ', '.join(['{}: {}'.format(x, y) for x, y in sorted(nav_menu.items())])
        return nav_menu


class Navigation:
    """Navigation status class."""
    def __init__(self, client, base):
        self.c = curse.Curse()
        self._client = client
        self._base = base
        self.history = []
        self.parent_selected = None
        self.show_unversioned = False
        self.mode = None
        self._status = NavigationStatus()

    @property
    def path(self):
        """Returns navigation path."""
        try:
            return os.path.join(*self.history)
        except TypeError:
            return None

    def input_nav(self):
        """Input nav responsible for reading input keys and do corresponding action."""
        try:
            while True:
                cha = self.c.screen.getch()
                if cha == ord(Config.keys['quit']):
                    raise QuitSignal("Quit from input_nav.")
                if not self._status.main:
                    if cha == ord(Config.keys['back']) and self.mode == 'remote':
                        if self._remove():
                            self.browse_repo(self.path)
                    elif cha == ord(Config.keys['down']):
                        self.c.go_down()
                    elif cha == ord(Config.keys['up']):
                        self.c.go_up()
                    elif cha == ord(Config.keys['enter_dir']) and self.mode == 'remote':
                        if self._append():
                            self.browse_repo(self.path)
                    elif cha == ord(Config.keys['revert_file']) and self.mode == 'local':
                        filename = str(self.c.lines[self.c.selected])
                        self.revert_file(filename)
                        self.c.screen.clear()
                        self.view_status(self._base)
                    elif cha == ord(Config.keys['toggle_unversioned_files']) and self.mode == 'local':
                        self.show_unversioned = not self.show_unversioned
                        self.c.screen.clear()
                        self.view_status(self._base)
                else:
                    if cha == ord(Config.keys['browse_repo']):
                        self.mode = 'remote'
                        self._status.enter_previous = False
                        self.browse_repo()
                    elif cha == ord(Config.keys['view_status']):
                        self.mode = 'local'
                        self.view_status(self._base)
        except QuitSignal:
            logger.info('Quiting')
            self.c.quit()


    def base_status(self, text=None, text_only=False):
        """Base status changes status bar with given text. When text_only is True it displays
        only the text without navigation keys."""
        self._status.text_only = text_only
        if text and text_only:
            self._status.text = str(text)
            self.c.update_status_line(self._status.text)
        elif text:
            self._status.text = str(text)
            self.c.update_status_line(' - '.join([self._status.text,
                                                  self._status.shortcuts_(self)]))
        else:
            self.c.update_status_line(self._status.shortcuts_(self))

    @debug_start_done
    def view_status(self, working_copy):
        """View status of given local working_copy."""
        self.base_status("status loading...", text_only=True)
        files = self._client.status()

        self.base_status(working_copy)
        self.c.print_local_files(files, self.show_unversioned)

    @debug_start_done
    def browse_repo(self, rel=None):
        """Browse remote repo function."""
        self.c.screen.clear()
        self.base_status("browse loading...", text_only=True)
        _directory = Dir(self._client)
        files = _directory.list(rel)
        if files is None:
            msg = os.path.join(self._base, rel) + " - Not under version control."
            logger.warning(msg)
            self.base_status(msg, text_only=True)
            self.history = self.history[:-1]
        else:
            self.base_status(os.path.join(self._base, rel if rel else ''))
            if self.parent_selected:
              selected_index = next((index for (index, d) in enumerate(files) if d["path"] == self.parent_selected), None)
              self.c.set_default_selected(selected_index)
            self.c.print_remote_files(files)

    def revert_file(self, path):
        self._client.run_command("revert", [path])

    def _append(self):
        """Returns True if append something, else False."""
        line = str(self.c.lines[self.c.selected])
        if line.endswith('/'):
            self.history.append(line.strip('/'))
            return True
        return False

    def _remove(self):
        """Returns True if remove something, else False."""
        if self.history:
            self.parent_selected = self.history.pop() + '/'
            return True
        return False


def login_handler(*args):
    # TODO: Use python keyring

    # hard-code credentials
    # return True, "username", "password", True

    # or prompt user
    user = input("Username: ")
    passw = getpass.getpass("Password: ")
    return True, user, passw, True


if __name__ == '__main__':
    main()
