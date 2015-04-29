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
        import pytest
        errno = max(errno, pytest.main(self.pytest_args))
        raise SystemExit(errno)

setup(name='round',
      version='0.7.3',
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
          'pyotp',
          'PyNaCl==0.3.0',
          'coinop==0.1.3',
      ],
      tests_require=[
        'pytest',
      ],
      cmdclass = {'test': PyTest},
      zip_safe=False
)
