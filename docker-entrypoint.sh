#!/bin/bash
sourcedir=rpmbuild/SOURCES
specdir=rpmbuild/SPECS
cp -v src/gdal-1.9.0-java.patch $sourcedir
cp -v src/gdal-cleaner.sh $sourcedir
cp -v src/gdal-g2clib.patch $sourcedir
cp -v src/gdal-jni.patch $sourcedir
cp -v src/gdal.pom $sourcedir
cp -v src/PROVENANCE.TXT-fedora $sourcedir

cp -v src/gdal.spec $specdir

rpmbuild -ba $specdir/gdal.spec

cp -rfvu rpmbuild/RPMS rpmbuild/SRPMS dest/
