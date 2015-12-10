#!/bin/bash
this=$(readlink -f $0)
workdir=$(dirname "$this")
echo WORKDIR is $workdir
docker build --force-rm -t gdal-rpm .
docker run -it --rm -v $workdir/src:/root/src -v $workdir/dest:/root/dest gdal-rpm
docker rmi gdal-rpm
