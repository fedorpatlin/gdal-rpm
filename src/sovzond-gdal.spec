AutoReqProv: no
%global glob_prefix /opt/sovzond.center
%global _prefix	%{glob_prefix}
%global srcname gdal

## path to libjvm
%global libjvm_path /usr/lib/jvm/java/jre/lib/amd64/server/

# Enable/disable generating refmans
%global build_refman 1
# We have multilib triage
%if "%{_lib}" == "lib"
  %global cpuarch 32
%else
  %global cpuarch 64
%endif


Name:		gdal-szc
Version:	1.11.3
Release:	3%{?dist}
Summary:	GDAL library

Group:		System Environment/Libraries
License:	MIT
URL:		http://www.gdal.org
Source0:	%{srcname}-%{version}.tar.xz
Source1:	gdalautotest-%{version}.tar.gz
Patch1: gdal-1.9.0-java.patch

BuildRequires: ant
BuildRequires: armadillo-devel
BuildRequires: cfitsio-devel
BuildRequires: CharLS-devel
BuildRequires: chrpath
BuildRequires: curl-devel
BuildRequires: doxygen
BuildRequires: expat-devel
BuildRequires: fontconfig-devel
BuildRequires: freexl-devel
BuildRequires: g2clib-static
BuildRequires: geos-devel
BuildRequires: ghostscript
BuildRequires: hdf-devel
BuildRequires: hdf-static
BuildRequires: hdf5-devel
BuildRequires: jasper-devel
BuildRequires: jpackage-utils
BuildRequires: libgeotiff-devel
BuildRequires: libgta-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libspatialite-devel
BuildRequires: libtiff-devel
BuildRequires: libwebp-devel
BuildRequires: libtool
BuildRequires: giflib-devel
BuildRequires: netcdf-devel
BuildRequires: libdap-devel
BuildRequires: librx-devel
BuildRequires: mysql-devel
BuildRequires: numpy
BuildRequires: pcre-devel
BuildRequires: ogdi-devel
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: pkgconfig
BuildRequires: poppler-devel
BuildRequires: postgresql-devel
BuildRequires: proj-devel
BuildRequires: python27-szc-devel
BuildRequires: python27-numpy-szc
BuildRequires: sqlite-devel
BuildRequires: swig
BuildRequires: unixODBC-devel
BuildRequires: xerces-c-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel
BuildRequires: java-1.8.0-openjdk-devel

Requires: armadillo
Requires: freexl
Requires: expat
Requires: xerces-c
Requires: jasper
Requires: hdf
Requires: ogdi
Requires: giflib
Requires: libgta
Requires: cfitsio
Requires: pcre
Requires: libxml2
Requires: python27-szc


%description
Some description here

%package devel
Summary: Development files for GDAL library packaged by sovzond.center
Requires: %{name} >= %{version}-%{release}
Requires: armadillo-devel
Requires: freexl-devel
Requires: expat-devel
Requires: xerces-c-devel
Requires: jasper-devel
Requires: hdf-devel
Requires: ogdi-devel
Requires: giflib-devel
Requires: libgta-devel
Requires: cfitsio-devel
Requires: g2clib-devel
Requires: pcre-devel
Requires: java-1.8.0-openjdk-devel
Requires: libxml2-devel
Requires: python27-szc-devel
Requires: gpsbabel

%description devel
Development files for GDAL library packaged by sovzond.center

%package python
Summary: Python libraries for GDAL library packaged by sovzond.center
Group:   Development/Libraries
Requires: %{name} >= %{version}-%{release}
Requires: python27-numpy-szc
%description python
Python libraries for GDAL library packaged by sovzond.center

%package java
Summary: Java libraries for GDAL library packaged by sovzond.center
Requires: %{name} >= %{version}-%{release}
Requires: java-1.7.0-openjdk-devel
Requires: jpackage-utils

%description java
Java libraries for GDAL library packaged by sovzond.center

%package doc
Summary: Documentation for GDAL library packaged by sovzond.center
Requires: %{name} >= %{version}-%{release}
Group:   Documentation
BuildArch: noarch
%description doc
Documentation for GDAL library packaged by sovzond.center

%prep
%setup -n %{srcname}-%{version}

%patch1 -p1 -b .java~

# Delete bundled libraries
# rm -rf frmts/zlib
# rm -rf frmts/png/libpng
# rm -rf frmts/gif/giflib
# rm -rf frmts/jpeg/libjpeg \
#     frmts/jpeg/libjpeg12
# rm -rf frmts/gtiff/libgeotiff \
#     frmts/gtiff/libtiff
# rm -r frmts/grib/degrib18/g2clib-1.0.4
# from official GDAL-spec
set +x
for f in `find . -type f` ; do
  if file $f | grep -q ISO-8859 ; then
    set -x
    iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
      mv -f ${f}.tmp $f
    set +x
  fi
  if file $f | grep -q CRLF ; then
    set -x
    sed -i -e 's|\r||g' $f
    set +x
  fi
done
set -x

# Solved for 2.0
for f in ogr/ogrsf_frmts/gpsbabel ogr/ogrsf_frmts/pgdump port apps; do
pushd $f
  chmod 644 *.cpp *.h
popd
done

# Fix build order with parallel make
# http://trac.osgeo.org/gdal/ticket/5346
#sed -i '/^swig-modules:/s/lib-target/apps-target/' GNUmakefile

# Workaround about wrong result in configure
# armadillo returns a warning about gcc versions 4.7.0 or 4.7.1
# due to http://gcc.gnu.org/bugzilla/show_bug.cgi?id=53549
# configure interprets the result as an error so ignore it
# this patch can/should be removed after gcc 4.7.2 is released
#sed -i 's|if test -z "`${CXX} testarmadillo.cpp -o testarmadillo -larmadillo 2>&1`"|if true|' configure

# Replace hard-coded library- and include paths
#sed -i 's|-L\$with_cfitsio -L\$with_cfitsio/lib -lcfitsio|-lcfitsio|g' configure
#sed -i 's|-I\$with_cfitsio -I\$with_cfitsio/include|-I\$with_cfitsio/include/cfitsio|g' configure
#sed -i 's|-L\$with_netcdf -L\$with_netcdf/lib -lnetcdf|-lnetcdf|g' configure
#sed -i 's|-L\$DODS_LIB -ldap++|-ldap++|g' configure
#sed -i 's|-L\$with_ogdi -L\$with_ogdi/lib -logdi|-logdi|g' configure
#sed -i 's|-L\$with_jpeg -L\$with_jpeg/lib -ljpeg|-ljpeg|g' configure
#sed -i 's|-L\$with_libtiff\/lib -ltiff|-ltiff|g' configure
#sed -i 's|-lgeotiff -L$with_geotiff $LIBS|-lgeotiff $LIBS|g' configure
#sed -i 's|-L\$with_geotiff\/lib -lgeotiff $LIBS|-lgeotiff $LIBS|g' configure

# libproj is dlopened; upstream sources point to .so, which is usually not present
# http://trac.osgeo.org/gdal/ticket/3602
sed -i 's|libproj.so|libproj.so.0|g' ogr/ogrct.cpp

# Fix Python installation path
#sed -i 's|setup.py install|setup.py install --root=%{buildroot}|' swig/python/GNUmakefile

# Must be corrected for 64 bit architectures other than Intel
# http://trac.osgeo.org/gdal/ticket/4544
# Should be gone in 2.0
sed -i 's|test \"$ARCH\" = \"x86_64\"|test \"$libdir\" = \"/usr/lib64\"|g' configure

# Adjust check for LibDAP version
# http://trac.osgeo.org/gdal/ticket/4545
%if %cpuarch == 64
  sed -i 's|with_dods_root/lib|with_dods_root/lib64|' configure
%endif

# Fix mandir
sed -i "s|^mandir=.*|mandir='\${prefix}/share/man'|" configure

# Activate support for JPEGLS
#sed -i 's|^#HAVE_CHARLS|HAVE_CHARLS|' GDALmake.opt.in
#sed -i 's|#CHARLS_INC = -I/path/to/charls_include|CHARLS_INC = -I%{_includedir}/CharLS|' GDALmake.opt.in
#sed -i 's|#CHARLS_LIB = -L/path/to/charls_lib -lCharLS|CHARLS_LIB = -lCharLS|' GDALmake.opt.in

# Replace default plug-in dir
# Solved in 2.0
# http://trac.osgeo.org/gdal/ticket/4444
%if %cpuarch == 64
  sed -i 's|GDAL_PREFIX "/lib/gdalplugins"|GDAL_PREFIX "/lib64/gdalplugins"|' \
    gcore/gdaldrivermanager.cpp \
    ogr/ogrsf_frmts/generic/ogrsfdriverregistrar.cpp
%endif

# Remove man dir, as it blocks a build target.
# It obviously slipped into the tarball and is not in Trunk (April 17th, 2011)
#rm -rf man

#--with-cfitsio=/usr \
#--with-dods-root=/usr \
#--with-geotiff=external   \
#--with-libtiff=yes        \

# --without-bsb \
# --with-armadillo          \
# --with-curl               \
# --with-expat              \
# --with-freexl             \
# --with-geos               \
# --with-geotiff=yes       \
# --with-gif                \
# --with-gta                \
# --with-hdf4               \
# --with-hdf5               \
# --with-jasper             \
# --with-java               \
# --with-jpeg               \
# --without-jpeg12          \
# --with-liblzma            \
# --with-libz               \
# --without-mdb             \
# --with-mysql              \
# --with-netcdf             \
# --with-odbc               \
# --with-ogdi               \
# --without-msg             \
# --without-openjpeg        \
# --with-pcraster           \
# --with-pg                 \
# --with-png                \
# --with-poppler            \
# --with-spatialite         \
# --with-sqlite3            \
# --with-threads            \
# --with-webp               \
# --with-xerces             \
# --enable-shared           \
# --with-perl               \
# --with-python

%build
%configure \
LIBS=-lgrib2c \
--with-autoload=%{_libdir}/%{srcname}plugins \
--datadir=%{_datadir}/%{srcname}/ \
--includedir=%{_includedir}/%{srcname} \
--prefix=%{_prefix} \
--with-java=/usr/lib/jvm/java/ \
--with-jasper \
--with-odbc \
--with-armadillo          \
--with-python=%{glob_prefix}/bin/python

make %{?_smp_mflags}
make man
make docs
pushd swig/java
  make
  ./make_doc.sh
popd

# --------- Documentation ----------

# No useful documentation in swig
%global docdirs apps doc doc/br doc/ru ogr ogr/ogrsf_frmts frmts/gxf frmts/iso8211 frmts/pcidsk frmts/sdts frmts/vrt ogr/ogrsf_frmts/dgn/
for docdir in %{docdirs}; do
  # CreateHTML and PDF documentation, if specified
  pushd $docdir
    if [ ! -f Doxyfile ]; then
      doxygen -g
    else
      doxygen -u
    fi
    sed -i -e 's|^GENERATE_LATEX|GENERATE_LATEX = YES\n#GENERATE_LATEX |' Doxyfile
    sed -i -e 's|^GENERATE_HTML|GENERATE_HTML = YES\n#GENERATE_HTML |' Doxyfile
    sed -i -e 's|^USE_PDFLATEX|USE_PDFLATEX = YES\n#USE_PDFLATEX |' Doxyfile

    if [ $docdir == "doc/ru" ]; then
      sed -i -e 's|^OUTPUT_LANGUAGE|OUTPUT_LANGUAGE = Russian\n#OUTPUT_LANGUAGE |' Doxyfile
    fi
    rm -rf latex html
    doxygen

    %if %{build_refman}
      pushd latex
        sed -i -e '/rfoot\[/d' -e '/lfoot\[/d' doxygen.sty
        sed -i -e '/small/d' -e '/large/d' refman.tex
        sed -i -e 's|pdflatex|pdflatex -interaction nonstopmode |g' Makefile
        make refman.pdf || true
      popd
    %endif
  popd
done

%install
rm -rf %{buildroot}

make    DESTDIR=%{buildroot} \
        install \
        install-man

# Directory for auto-loading plugins
mkdir -p %{buildroot}%{_libdir}/%{srcname}plugins

#TODO: JAR files that require JNI shared objects MUST be installed in %{_libdir}/%{name}. The JNI shared objects themselves must also be installed in %{_libdir}/%{name}.
#Java programs that wish to make calls into native libraries do so via the Java Native Interface (JNI). A Java package uses JNI if it contains a .so
#If the JNI-using code calls System.loadLibrary you'll have to patch it to use System.load, passing it the full path to the dynamic shared object. If the package installs a wrapper script you'll need to manually add %{_libdir}/%{name}/<jar filename> to CLASSPATH. If you are depending on a JNI-using JAR file, you'll need to add it manually -- build-classpath will not find it.
touch -r NEWS swig/java/gdal.jar
mkdir -p %{buildroot}%{_javadir}
cp -p swig/java/gdal.jar  \
    %{buildroot}%{_javadir}/%{srcname}.jar

mkdir -p %{buildroot}%{_jnidir}/%{srcname}
cp -pl swig/java/.libs/*.so*  \
    %{buildroot}%{_jnidir}/%{srcname}/
chrpath --delete %{buildroot}%{_jnidir}/%{srcname}/*jni.so*

# Install Java API documentation in the designated place
mkdir -p %{buildroot}%{_javadocdir}/%{srcname}
cp -pr swig/java/java/org %{buildroot}%{_javadocdir}/%{srcname}

# Install refmans
for docdir in %{docdirs}; do
  pushd $docdir
    path=%{_builddir}/%{srcname}-%{version}/refman
    mkdir -p $path/html/$docdir
    cp -r html $path/html/$docdir

    # Install all Refmans
    %if %{build_refman}
        if [ -f latex/refman.pdf ]; then
          mkdir -p $path/pdf/$docdir
          cp latex/refman.pdf $path/pdf/$docdir
        fi
    %endif
  popd
done

# Install formats documentation
for dir in gdal_frmts ogrsf_frmts; do
  mkdir -p $dir
  find frmts -name "*.html" -exec install -p -m 644 '{}' $dir \;
done

## Install ldconfig
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo %{_libdir} > %{buildroot}%{_sysconfdir}/ld.so.conf.d/gdal-szc.conf
echo %{libjvm_path} > %{buildroot}%{_sysconfdir}/ld.so.conf.d/libjvm.conf
%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files devel
%{_includedir}/%{srcname}/*.h
%{_libdir}/pkgconfig/*
%{_libdir}/libgdal.a
%{_libdir}/libgdal.la

%files python
%{_bindir}/*.py
%{_bindir}/*.dox
%{_prefix}/lib/python2.7/site-packages/*

%files java
%{_prefix}/lib/java/%{srcname}/*
%{_prefix}/share/java/gdal.jar

%files doc
%{_prefix}/share/javadoc/%{srcname}/*
%{_prefix}/share/man/*

%files
%doc
%exclude %{_bindir}/*.py
%exclude %{_bindir}/*.dox
%{_bindir}/*
%{_libdir}/libgdal.so*
%{_prefix}/share/gdal/*
%{_sysconfdir}/ld.so.conf.d/gdal-szc.conf
%{_sysconfdir}/ld.so.conf.d/libjvm.conf


%changelog
* Thu Apr 21 2016 Fyodor Patlin <patlin.f@sovzond.center> 1.11.3-3
- исправлены скрипты %pre и %postun
* Thu Mar 24 2016 Fyodor Patlin <patlin.f@sovzond.center> 1.11.3-2
- Убрано --enable-shared
* Tue Mar 22 2016 Fyodor Patlin <patlin.f@sovzond.center> 1.11.3-1
- Первый пробный выпуск библиотеки, устанавливаемой в /opt/sovzond.center
