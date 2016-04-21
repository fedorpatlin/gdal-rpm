#!/bin/bash

sourcedir=/root/rpmbuild/SOURCES
specdir=/root/rpmbuild/SPECS
srpmdir=/root/rpmbuild/SRPMS
rpmdir=/root/rpmbuild/RPMS

specfile=$1
if [[ -z "$specfile" ]]; then
  echo "Spec file is missing"
  exit 1
fi

mkdir -p /root/rpmbuild/{RPMS,SRPMS,SOURCES,SPECS,BUILD,BUILDROOT}

ls -l /root/rpmbuild
cp -v /root/src/* $sourcedir
cp -v /root/src/$1 $specdir
rpmbuild -ba $specdir/$1
cp -rfvu $srpmdir $rpmdir /root/dest/
