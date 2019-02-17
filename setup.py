#!/usr/bin/env python
from setuptools import setup
import versioneer

NAME = 'drms'
DESCRIPTION = 'Access HMI, AIA and MDI data with Python'
LONG_DESCRIPTION = open('README.rst').read()
AUTHOR = 'Kolja Glogowski'
AUTHOR_EMAIL = '"Kolja Glogowski" <kolja@pixie.de>'
URL = 'https://github.com/sunpy/drms'
LICENSE = 'MIT'

setup(name=NAME,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      license=LICENSE,
      packages=['drms', 'drms.tests', 'drms.tests.online'],
      install_requires=[
          'numpy>=1.9.0',
          'pandas>=0.15.0',
          'six>=1.8.0'],
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: Astronomy'],
      platforms='any')
