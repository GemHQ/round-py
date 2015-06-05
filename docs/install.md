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
  $ mkvirtualenv round
  ```

### Linux (apt)-based)

1. Just install

  ```bash
  $ pip install round
  ```

 [[back]](../README.md)

### Mac OSX:

1. Just install

  ```bash
  $ pip install round
  ```

 [[back]](../README.md)

### Windows:

TODO

### Heroku

[Heroku](http://www.heroku.com) introduces some complexities around libsodium ([PyNaCl](https://pynacl.readthedocs.org/en/latest/)), the cryptography library `round` uses.

1. Include the following in your `requirements.txt`.
  ```
  round
  ```

 [[back]](../README.md)
