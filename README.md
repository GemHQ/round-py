# round-py: A Python client for the Gem API


`round-py` is still alpha code but is in active development. Bug reports and
patches welcome.


## Installing round-py:

### Ubuntu:

#### Prerequisites:

* A python 2.7 environment (your distro probably does this as part of the base system, but the nicer way is with `pyenv` and/or `virtualenv`). `coinop-py` is currently developed under 2.7.7.

* Git and a python extension build environment. You probably have most or all of this on your machine already, but the  following should do it on a bare Debian/Ubuntu system (package names correct on Ubuntu 13.10 and 14.04 at least):

  ```bash
  $ sudo apt-get install gcc make libffi-dev python-dev python-pip git
  ```

#### Installing:

1. Ask us to add you to the round-py github repo (https://github.com/GemHQ/round-py). While you wait impatiently, continue with the following.


### Linux

1. Clone the git repository and run setup.py:

  ```bash
  $ git clone git@github.com:GemHQ/round-py.git
  $ cd round-py
  $ sudo python setup.py install
  ```

  (if you're using a virtual environment, you obviously don't need to run
setup.py with sudo)

### Mac OSX:

1.  Install Xcode Command Line Tools
```bash
xcode-select --install
```

1.  ```bash
brew install libffi
```

1.  ```bash
$ export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/
```

1. clone the git repository and run setup.py:

  ```bash
  $ git clone git@github.com:GemHQ/round-py.git
  $ cd round-py
  $ python setup.py install
  ```
