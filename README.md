bitvault-py: A Python client for the BitVault API


bitvault-py is still alpha code but is in active development. Bug reports and
patches welcome.


Installing bitvault-py:

1. Install a python 2.7 environment (the nicest way to do this is with pyenv
   and virtualenv).  It is developed under 2.7.7, and while it may work with
   earlier versions that is currently untested. The goal is compatibility with
   at least the 2.7 and perhaps the 2.6 series. If those versions don't fit
   your needs drop us a line and we can talk about it.

2. Install a C build environment if you don't already have one: you'll need gcc
   (Debian/Ubuntu: gcc) and make (make)

3. Install the python C extension libraries: libpython (libpython-all-dev),
   libffi (libffi-dev)

4. Make sure you've installed pip (Ubuntu: python-pip), or at least setuptools
   (python-setuptools) if you only plan to work from the git repository.

5. Ask us to add you to the bitvault-py github repo
   (https://github.com/BitVault/bitvault-py). Clone the repo and run 'python
   setup.py install' ('python setup.py develop' if you plan to work on the
   codebase yourself).
