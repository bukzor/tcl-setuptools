#!/bin/bash
set -eu
package="$1"
url="$2"
tar=sdist/$package.tar.gz
dst=sdist/$package

set -x
if [ -d $dst ]; then
    echo $package already downloaded
else
    mkdir -p "$(dirname $tar)"
    wget $url -O $tar
fi


mkdir -p $dst.tmp
tar xf $tar -C $dst.tmp --strip-components 1

rm -rf $dst
mv -T $dst.tmp $dst
