
#!/usr/bin/env python

from setuptools import setup
from drmutils import __version__

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='dmrutils',
    version=__version__,
    author='Devin Riley',
    author_email='rileyde@umich.edu',
    packages=['dmrutils'],
    url='https://github.com/devmacrile/dmrutils',
    download_url='https://github.com/devmacrile/dmrutils/tarball/%s' % __version__,
    install_requires=required
)
