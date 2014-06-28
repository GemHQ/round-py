bitvault-py: A Python client for the BitVault API


bitvault-py is still alpha code but is in active development. Bug reports and
patches welcome.


Installing bitvault-py:

Ubuntu:

Prerequisites:

1. A python 2.7 environment (your distro probably does this as part of the base
   system, but the nicer way is with pyenv and/or virtualenv). coinop-py is
   currently developed under 2.7.7.

2. A python extension build environment. You probably have most or all of this
   on your machine already, but the following should do it on a bare system:

   $ sudo apt-get install gcc make libpython-all-dev libffi-dev python-pip

Installing:

1. Ask us to add you to the bitvault-py github repo
   (https://github.com/BitVault/bitvault-py).

2. clone the git repository and run setup.py:

    $ git clone https://github.com/BitVault/bitvault-py.git
    $ cd bitvault-py
    $ sudo python setup.py install

(if you're using a virtual environment, you obviously don't need sudo in
either case)
