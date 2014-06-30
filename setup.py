from setuptools import setup, find_packages
from setuptools.command.install import install
import os


class MyCommand(install):
    """Dirty hack to install coinop with pip as it doesn't work automatically
    on some machines."""

    def run(self):
        os.system("pip install --exists-action=i coinop")
        install.run(self)


setup(name='bitvault',
      cmdclass={'install': MyCommand},
      version='0.1.0',
      description='Python client for BitVault.io',
      url='http://github.com/BitVault/bitvault-py',
      author='Dustin Laurence',
      author_email='dustin@pandastrike.com',
      license='MIT',
      packages=find_packages(exclude=[
          u'*.tests', u'*.tests.*', u'tests.*', u'tests']),
      install_requires=[
          'PyYAML',
          'patchboard',
          'coinop',
      ],
      zip_safe=False)
