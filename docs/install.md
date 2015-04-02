## Installing round-py:


### Prerequisites:

* Python 2.7
* Git and a python extension build environment.
* libffi

#### Virtualenv (optional)

1. Install virtualenv & wrapper

  ```bash
  $ pip install --user virtualenv
  $ pip install --user virtualenvwrapper
  ```

2. Edit your ~/.bashrc or ~/.bash_profile

  ```bash
  export PATH="${HOME}/.local/bin:${PATH}"
  export WORKON_HOME="${HOME}/.virtualenvs"
  source ${HOME}/.local/bin/virtualenvwrapper.sh
  ```

3. Make an environment

  ```bash
  $ mkvirtualenv py27
  ```

### Linux (debian-based, tested on Ubuntu 14.04)

1. Install system dependencies (*this is the only time you need sudo!*)

  ```bash
  $ sudo apt-get install gcc make libffi-dev python-dev python-pip git
  ```

2. Install the client

  ```bash
  $ pip install round
  ```

 [[back]](../README.md)

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

4. Pip install the client
  ```bash
  $ pip install round
  ```

 [[back]](../README.md)

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

 [[back]](../README.md)
