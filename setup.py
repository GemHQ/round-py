from setuptools import setup, find_packages


setup(name='bitvault',
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
          # Not explicitly listed as a dependency to ensure that you
          # install manually--see README for explanation
          # 'coinop',
      ],
      zip_safe=False)
