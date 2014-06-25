from setuptools import setup

setup(name='bitvault',
      version='0.1.0',
      description='Python client for BitVault.io',
      url='http://github.com/BitVault/bitvault-py',
      author='Dustin Laurence',
      author_email='dustin@pandastrike.com',
      license='MIT',
      packages=['bitvault'],
      install_requires=[
          'PyYAML',
      ],
      zip_safe=False)
