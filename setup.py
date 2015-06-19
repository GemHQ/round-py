# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(name = 'round',
      version = '0.8.1',
      description = 'Python client for Gem.co',
      url = 'http://github.com/GemHQ/round-py',
      author = 'Matt Smith <matt@gem.co>, Dustin Laurence <dustin@gem.co>',
      author_email = 'developers@gem.co',
      license = 'MIT',
      packages = find_packages(exclude=[
          u'*.tests', u'*.tests.*', u'tests.*', u'tests']),
      scripts = [ 'gemcli' ],
      install_requires = [
          'PyYAML',
          'patchboard==0.5.1',
          'pyotp',
          'coinop==0.2.1',
          'future',
          'tabulate'
      ],
      tests_require = [
          'pytest',
          'tox'
      ],
      dependency_links=[
          'https://github.com/marcobiscaro2112/pyotp/tarball/python3#egg=pyotp'
      ],
      zip_safe = False
)
