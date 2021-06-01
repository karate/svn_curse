## svn-curse
This is a proof-of-concept command-line svn client with ncurses, written in python.

Features:
- [x] View status with colors
- [x] Browse remote repository
- [x] Revert files
- [ ] View diff
- [ ] Commit files
- [ ] Blame

Tips, issues, comments and pull requests are more than welcome.


## Installation
Prerequisites:
- python3
- subversion

### Checkout
```bash
git clone https://github.com/karate/svn_curse.git
cd svn_curse
```

### Install and activate virtualenv (optional)
```bash
# Install virtualenv
sudo pip3 install virtualenv
# Set-up
virtualenv -p python3 venv
# Activate
source venv/bin/activate
```

### Install requirements:
#### On Linux:
```
$ pip install -r requirements.txt
```
#### On Windows:
```
$ pip install -r requirements_win.txt
```

## Usage
```bash
./main.py path/to/svn/repo
```
or
```bash
python main.py path\to\svn\repo
```
