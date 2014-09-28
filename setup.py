from setuptools import setup, find_packages


setup(name='round',
      version='0.1.0',
      description='Python client for Gem.co',
      url='http://github.com/BitVault/round-py',
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
