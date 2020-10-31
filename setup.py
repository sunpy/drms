#!/usr/bin/env python
import os
from itertools import chain

from setuptools import setup
from setuptools.config import read_configuration

################################################################################
# Programmatically generate some extras combos.
################################################################################
extras = read_configuration('setup.cfg')['options']['extras_require']

# Dev is everything
extras['dev'] = list(chain(*list(extras.values())))

# All is everything but tests and docs
exclude_keys = ('tests', 'docs', 'dev')
ex_extras = dict([i for i in list(extras.items()) if i[0] not in exclude_keys])
# Concatenate all the values together for 'all'
extras['all'] = list(chain.from_iterable(list(ex_extras.values())))

setup(
    extras_require=extras, use_scm_version={'write_to': os.path.join('drms', '_version.py')},
)
