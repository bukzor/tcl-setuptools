#!/usr/bin/env python
# this really only works on linux systems, at the moment
from __future__ import print_function

# set $DISTUTILS_DEBUG to get extra output from distutils
from os import environ
environ['DISTUTILS_DEBUG'] = 'true'


from setuptools import setup
from distutils.core import Command
from distutils.dist import Distribution
from setuptools.command.sdist import sdist as orig_sdist


# ############# NOTES #####################
# setuptools.command.sdist.sdist

# setuptools/command/egg_info.py:egg_info.find_sources()
#   seems to be in charge of generating a file list
#   writes SOURCES.txt for its list
#   also reads MANIFEST.in; maybe this is the interface

# setuptools/command/sdist.py:add_defaults
#   adds various files to the file list based on the distribution object

# distutils/command/sdist.py:sdist.make_release_tree(base_dir, files)
#   copy files to base_dir. this will become the sdist

class s6_distribution(object):
    def __init__(self, *args, **kwargs):
        print('__init__:', args, kwargs)
        self.__dict__['dist'] = Distribution(*args, **kwargs)

    def __getattr__(self, key):
        result = getattr(self.dist, key)
        print('getattr(%r) -> %r' % (key, result))
        return result

    def __setattr__(self, key, value):
        print('setattr(%r, %r)' % (key, value))
        setattr(self.dist, key, value)


class fetch_sources(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        os.system('./get_sources.sh')


class sdist(orig_sdist):
    sub_commands = [
        ('fetch_sources', None),
    ] + orig_sdist.sub_commands

    def make_release_tree(self, base_dir, files):
        result = orig_sdist.make_release_tree(self, base_dir, files)
        return result

setup(
    name='s6',
    version='2.2.0.1',
    distclass=s6_distribution,
    cmdclass={
        'sdist': sdist,
        'fetch_sources': fetch_sources,
    }
)
