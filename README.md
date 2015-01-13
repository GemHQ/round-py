# round-py: A Python client for the Gem API


`round-py` is still alpha code but is in active development. Bug reports and
patches welcome.


## Installing round-py:

### Ubuntu:

#### Prerequisites:

* A python 2.7 environment (your distro probably does this as part of the base system, but the nicer way is with `pyenv` and/or `virtualenv`). `coinop-py` is currently developed under 2.7.7.

* Git and a python extension build environment.

* libffi

#### Installing:

1. Ask us to add you to the round-py github repo (https://github.com/GemHQ/round-py). While you wait impatiently, continue with the following.


### Linux

1. Clone the git repository and run setup.py:

  ```bash
  $ sudo apt-get install gcc make libffi-dev python-dev python-pip git
  $ git clone git@github.com:GemHQ/round-py.git
  $ cd round-py
  $ sudo python setup.py install
  ```

  (if you're using a virtual environment, you obviously don't need to run
setup.py with sudo)

### Mac OSX:

1.  Install Xcode Command Line Tools
  ```bash
  $ xcode-select --install
  ```

2.  ```bash
  $ brew install libffi libsodium
  ```

3.  ```bash
  $ export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/
  ```

4. ```bash
  $ pip install PyNaCl PyYAML patchboard coinop
  ```

5. clone the git repository and run setup.py:

  ```bash
  $ git clone git@github.com:GemHQ/round-py.git
  $ cd round-py
  $ python setup.py develop **for production environments use `python setup.py install`***
  ```

### Heroku

[Heroku](http://www.heroku.com) introduces some complexities around libsodium ([PyNaCl](https://pynacl.readthedocs.org/en/latest/)), the cryptography library `round` uses.

1. Include the following in your `requirements.txt`.
  ```
  pycrypto
  cffi
  cryptography
  PyNaCl
  git+https://[GH_USERNAME]:[GH_PASSWORD_OR_ACCESS_TOKEN]@github.com/GemHQ/round-py.git#egg=round
  ```

1. Install the [heroku-buildpack-multi](https://github.com/ddollar/heroku-buildpack-multi) to allow multiple buildpacks
  ```bash
  $ heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
  ```

2. Add these lines to the *top* to your `.buildpacks` file.
  ```
  git://github.com/fletom/heroku-buildpack-python-libffi.git
  git://github.com/fletom/heroku-buildpack-libsodium.git
  ```

3. Set the `SODIUM_INSTALL` environment variable
  ```bash
  $ heroku config:set SODIUM_INSTALL=system
  ```

From here you should be able to `import round` into your heroku project without error. (Most errors related to `round` on Heroku will mention `<sodium.h>` or `cffi` -- this is because PyNaCl compiles on import, which is likely to change in the next major release, see [this discussion](https://github.com/pyca/pynacl/issues/79).)
