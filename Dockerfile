FROM centos:6

WORKDIR /root
RUN rm -f /var/cache/yum/timedhosts.txt\
  && echo "timeout=1" >> /etc/yum.conf\
  && yum clean all\
  && yum --verbose --noplugins install -y epel-release\
  && yum install -y tar\
	gcc\
	gcc-c++\
	make\
	rpm-build\
	java-1.8.0-openjdk-devel\
	g2clib-static\
	armadillo-devel\
	libxml2-devel\
	sqlite-devel\
	python-devel\
	ant\
	cfitsio-devel\
	CharLS-devel\
	chrpath\
	curl-devel\
	doxygen\
	expat-devel\
	fontconfig-devel\
	freexl-devel\
	geos-devel\
	ghostscript\
	hdf-devel\
	hdf-static\
	java-devel\
	jasper-devel\
	libgeotiff-devel\
	libgta-devel\
	libjpeg-devel\
	libpng-devel\
	libspatialite-devel\
	libtiff-devel\
	libwebp-devel\
	libtool\
	giflib-devel\
	netcdf-devel\
	libdap-devel\
	librx-devel\
	mysql-devel\
	numpy\
	pcre-devel\
	ogdi-devel\
	perl-ExtUtils-MakeMaker\
	poppler-devel\
	postgresql-devel\
	proj-devel\
	swig\
	texlive-latex\
	unixODBC-devel\
	xerces-c-devel\
	xz-devel\
   && yum clean all 
RUN mkdir -p rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}\
  && curl http://download.osgeo.org/gdal/1.11.3/gdal-1.11.3.tar.xz > rpmbuild/SOURCES/gdal-1.11.3.tar.xz\
  && curl http://download.osgeo.org/gdal/1.11.3/gdalautotest-1.11.3.tar.gz > rpmbuild/SOURCES/gdalautotest-1.11.3.tar.gz
COPY docker-entrypoint.sh /bin/entrypoint.sh
RUN chown +x /bin/entrypoint.sh
ENTRYPOINT ["/bin/entrypoint.sh"]


