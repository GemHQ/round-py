# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run(self):
        errno = 0
        if u"host" not in self.pytest_args:
            pass
            #import sys,subprocess
            #errno = subprocess.call([sys.executable, "patchboard/tests/scripts/play.py"])
            #if errno > 0:
            #    raise SystemExit(errno)
        import pytest
        errno = max(errno, pytest.main(self.pytest_args))
        raise SystemExit(errno)

setup(name='round',
      version='0.5.4',
      description='Python client for Gem.co',
      url='http://github.com/GemHQ/round-py',
      author='Dustin Laurence <dustin@gem.co>, Matt Smith <matt@gem.co>',
      author_email='developers@gem.co',
      license='MIT',
      packages=find_packages(exclude=[
          u'*.tests', u'*.tests.*', u'tests.*', u'tests']),
      install_requires=[
          'PyYAML',
          'patchboard',
          'PyNaCl',
          'coinop',
      ],
      tests_require=[
        'pytest',
        ],
      cmdclass = {'test': PyTest},
      zip_safe=False
      )
