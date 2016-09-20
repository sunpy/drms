#!/usr/bin/env python
from setuptools import setup
import versioneer


NAME = 'drms'
DESCRIPTION = 'Access HMI, AIA and MDI data with Python'
AUTHOR = 'Kolja Glogowski'
AUTHOR_EMAIL = '"Kolja Glogowski" <kolja@pixie.de>'
URL = 'https://github.com/kbg/drms'
LICENSE = 'MIT'


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
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
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
