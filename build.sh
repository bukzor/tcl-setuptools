#!/bin/bash
set -eu
dst="$(readlink -m $1)"
TOP="$PWD"
configure_options="--prefix=$dst --libdir=$dst/lib --with-include=$dst/include --with-lib=$dst/lib --with-dynlib=$dst/lib --enable-static --disable-shared --enable-allstatic --enable-force-devr"

# let's speed things up a bit; tell make to use some parallelism
NCPU=$(getconf _NPROCESSORS_CONF)
j=$((NCPU < 10 ? NCPU * 3 : 30))
export MAKE="make -j $j"

untar() {
    set +x
    package="$1"
    tar=$TOP/vendor/$package.tar.bz2
    dst=$TOP/vendor/$package

    set -x
    mkdir -p $dst.tmp
    tar -xf $tar -C $dst.tmp --strip-components 1

    rm -rf $dst
    mv -T $dst.tmp $dst
    echo $dst
}

build() {
    set +x
    package="$1"
    tar=$TOP/vendor/$package.tar.bz2

    set -x
    cd $(untar $package)
    ./configure $configure_options
    make
    make install
}

set -x

build environment-modules

rm -rf $dst/include
