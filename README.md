# round-py: A Python client for the Gem API


`round-py` is still alpha code but is in active development. Bug reports and
patches welcome.


## Installing round-py:

### Prerequisites:

* Python 2.7

* Virtualenv and virtualenvwrapper (or equivalent virtual environment solution) is required for Linux and recommended for everyone.

* Git and a python extension build environment.

* libffi


### Linux (debian-based, tested on Ubuntu 14.04)

1. Install system dependencies (*this is the only time you need sudo!*)

  ```bash
  $ sudo apt-get install gcc make libffi-dev python-dev python-pip git
  ```

2. Install virtualenv

  ```bash
  $ pip install --user virtualenv virtualenvwrapper
  ```

3. Edit .bashrc or .bash_profile to add ENV variables.

  ```bash
  export PATH="${HOME}/.local/bin:${PATH}"
  export WORKON_HOME="${HOME}/.virtualenvs"
  source ${HOME}/.local/bin/virtualenvwrapper.sh
  ```

4. Source that.
  ```bash
  $ source ~/.bashrc
  ```

5. Make a virtual environment (optionally add `workon py` to your .bashrc to use this env automatically)

  ```bash
  $ mkvirtualenv py
  ```

6. Clone this repo and install.

  ```bash
  $ git clone git@github.com:GemHQ/round-py.git
  $ cd round-py && git checkout devnacl
  $ python setup.py install
  ```

### Mac OSX:

1.  Install Xcode Command Line Tools
  ```bash
  $ xcode-select --install
  ```

2. Install libffi and libsodium
  ```bash
  $ brew install libffi libsodium
  ```

3. Add libffi to your `PKG_CONFIG_PATH`
  ```bash
  $ export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/
  ```

4. Pip install dependencies
  ```bash
  $ pip install PyNaCl PyYAML patchboard coinop
  ```

5. clone the git repository and run setup.py:
  ```bash
  $ git clone git@github.com:GemHQ/round-py.git
  $ cd round-py
  $ python setup.py develop **for production environments use:** `python setup.py install`
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

2. Install the [heroku-buildpack-multi](https://github.com/ddollar/heroku-buildpack-multi) to allow multiple buildpacks
  ```bash
  $ heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
  ```

3. Add these lines to the *top* to your `.buildpacks` file.
  ```
  git://github.com/fletom/heroku-buildpack-python-libffi.git
  git://github.com/fletom/heroku-buildpack-libsodium.git
  ```

4. Set the `SODIUM_INSTALL` environment variable
  ```bash
  $ heroku config:set SODIUM_INSTALL=system
  ```

From here you should be able to `import round` into your heroku project without error. (Most errors related to `round` on Heroku will mention `<sodium.h>` or `cffi` -- this is because PyNaCl compiles on import, which is likely to change in the next major release, see [this discussion](https://github.com/pyca/pynacl/issues/79).)
