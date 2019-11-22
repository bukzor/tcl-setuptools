#!/bin/bash
set -eu

source versions.sh

./get_package.sh tcl https://prdownloads.sourceforge.net/tcl/tcl$version-src.tar.gz
