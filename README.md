# bitvault-py: A Python client for the BitVault API


`bitvault-py` is still alpha code but is in active development. Bug reports and
patches welcome.


## Installing bitvault-py:

### Ubuntu:

#### Prerequisites:

* A python 2.7 environment (your distro probably does this as part of the base system, but the nicer way is with `pyenv` and/or `virtualenv`). `coinop-py` is currently developed under 2.7.7.

* Git and a python extension build environment. You probably have most or all of this on your machine already, but the  following should do it on a bare Debian/Ubuntu system (package names correct on Ubuntu 13.10 and 14.04 at least):

  ```bash
  $ sudo apt-get install gcc make libpython-all-dev libffi-dev python-pip git
  ```

#### Installing:

1. Ask us to add you to the bitvault-py github repo (https://github.com/BitVault/bitvault-py). While you wait impatiently, continue with the following.

1. *Manually* install PyNaCl to work around a bug getting PyNaCl to install correctly on some machines:

  ```bash
  $ sudo pip install PyNaCl
  ```

  (if you're using a virtual environment, you don't need to run pip
with sudo)

1. clone the v0.1 branch of the git repository and run setup.py:

  ```bash
  $ git clone -b v0.1 git@github.com:BitVault/bitvault-py.git
  $ cd bitvault-py
  $ sudo python setup.py install
  ```

  (if you're using a virtual environment, you obviously don't need to run
setup.py with sudo)
