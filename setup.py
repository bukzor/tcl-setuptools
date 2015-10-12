#!/usr/bin/env python
# this really only works on linux systems, at the moment
from __future__ import print_function

from os import environ
from os import system

# set $DISTUTILS_DEBUG to get extra output from distutils
environ['DISTUTILS_DEBUG'] = 'true'

from setuptools import setup
from distutils.core import Command
from setuptools.command.sdist import sdist as orig_sdist
from distutils.command.build import build as orig_build


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


class fetch_sources(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        system('./get_sources.sh')


class sdist(orig_sdist):
    def run(self):
        self.run_command('fetch_sources')
        return orig_sdist.run(self)


class build(orig_build):
    def run(self):
        self.run_command('fetch_sources')
        cmd = './build.sh %s' % self.build_temp
        print(cmd)
        system(cmd)
        return orig_build.run(self)


setup(
    name='s6',
    version='2.2.0.1',
    cmdclass={
        'sdist': sdist,
        'fetch_sources': fetch_sources,
        'build': build,
    }
)
