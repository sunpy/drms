#!/usr/bin/env python
import re
from setuptools import setup

NAME = 'drms'
DESCRIPTION = 'HMI, AIA and MDI data access using the JSOC DRMS'
AUTHOR = 'Kolja Glogowski'
AUTHOR_EMAIL = '"Kolja Glogowski" <kolja@pixie.de>'
URL = 'https://github.com/kbg/drms'
LICENSE = 'MIT'


# Read version string from __init__.py without importing the drms package, to
# prevent an import error in case numpy, pandas or six are not installed yet.
m = re.search(r"""^\s*__version__\s*=\s*["'](.+)["']\s*$""",
              open('drms/__init__.py').read(), re.MULTILINE)
VERSION = m.group(1)


# The readme file uses Markdown, which does not seem to be supported by PyPI.
# To solve this problem, we try to convert the README.md to reStructuredText
# using pypandoc.
try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert_file('README.md', 'rst')
except:
    # Fall back using the original Markdown text.
    print('Warning: Pypandoc not found. Skipping README.md conversion.')
    LONG_DESCRIPTION = open('README.md').read()


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      license=LICENSE,
      packages=['drms'],
      install_requires=[
          'numpy>=1.9.0',
          'pandas>=0.14.1',
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
          'Topic :: Scientific/Engineering :: Astronomy'],
      platforms='any'
      )
