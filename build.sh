#!/bin/bash
set -eu
dst="$(readlink -m $1)"
TOP="$PWD"

# let's speed things up a bit; tell make to use some parallelism
NCPU=$(getconf _NPROCESSORS_CONF)
j=$((NCPU < 10 ? NCPU * 3 : 30))
export MAKE="make -j $j"


set -x

cd $TOP/vendor/make
./configure && make
export PATH="$TOP/vendor/make:$PATH"


skaopts="--prefix=$dst --libdir=$dst/lib --with-include=$dst/include --with-lib=$dst/lib --with-dynlib=$dst/lib --enable-static --disable-shared --enable-allstatic"
cd $TOP/vendor/skalibs
./configure $skaopts --enable-force-devr
make
make install

cd $TOP/vendor/execline
./configure $skaopts
make
make install

cd $TOP/vendor/s6
./configure $skaopts
make
make install
