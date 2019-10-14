#! /usr/bin/env python3

import sys
import os
import getpass
import keyring
import pysvn
import dir
import curse

# User Modifiable Configuration
USERNAME = ""

def _get_working_copy ( argv ):
    if (len(argv) > 1):
        return argv[1].rstrip('/')
    else:
        return os.getcwd().rstrip('/')

def main ():
    working_copy = _get_working_copy( sys.argv )
    client = pysvn.Client()
    client.callback_get_login = login_handler

    c = curse.Curse();
    c.update_status_line( "w: view working copy status, r: browse remote repo, q: quit" )

    while True:
        ch = c.screen.getch()
        if ch == ord('r'):
            browse_repo( c, client, working_copy )
        elif ch == ord('w'):
            view_status(c, client, working_copy )
        elif ch == ord('q'):
            c.quit()
            break  # Exit the while()

def view_status ( c, client, working_copy ):
    c.update_status_line( "loading..." )
    files = client.status( working_copy, get_all = False)

    c.update_status_line( working_copy + " - j/k: up/down, q: quit")
    c.print_local_files( files )

    while True:
        cha = c.screen.getch()
        if cha == ord('q'):
            c.quit()
            sys.exit()
        elif cha == ord('j'):
            c.go_down()
        elif cha == ord('k'):
            c.go_up()

def browse_repo ( c, client, working_copy ):
    c.update_status_line( "loading..." )
    d = dir.Dir( client )
    files = d.ls( working_copy )
    if ( files is None ):
        c.update_status_line( working_copy + " - Not under version control. q: quit")
    else:
        c.update_status_line( working_copy + " - j/k: up/down, q: quit")
        c.print_remote_files( files )

    while True:
        cha = c.screen.getch()
        if cha == ord('q'):
            c.quit()
            sys.exit()
        elif cha == ord('j'):
            c.go_down()
        elif cha == ord('k'):
            c.go_up()

def login_handler(username=USERNAME):
    """pysvn expect the callback_get_login to return a tuple of four values
    (retcode, username, password, save).

    More info: https://tools.ietf.org/doc/python-svn/pysvn_prog_ref.html#pysvn_client_callback_get_login
    """
    if not username:
        print("[info] Configure the 'USERNAME' variable in 'main.py' to avoid "
              "this prompt in the future.")
        username = input("Username: ")
    # Check for existing keyring record
    password = keyring.get_password("svn_curse", username)
    if not password:
        print("[info] No password located for user '%s' in keyring."
              % (username))
        keyring.set_password("svn_curse", username,
                             getpass.getpass("Password: "))
        password = keyring.get_password("svn_curse", username)
    return True, username, password, True

main()
