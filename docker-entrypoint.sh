#!/bin/bash
sourcedir=rpmbuild/SOURCES
specdir=rpmbuild/SPECS
cp  src/gdal-1.9.0-java.patch $sourcedir
cp  src/gdal-cleaner.sh $sourcedir
cp  src/gdal-g2clib.patch $sourcedir
cp  src/gdal-jni.patch $sourcedir
cp  src/gdal.pom $sourcedir
cp  src/PROVENANCE.TXT-fedora $sourcedir

cp  src/gdal.spec $specdir

rpmbuild -ba $specdir/gdal.spec

cp -rfu rpmbuild/RPMS rpmbuild/SRPMS dest/
