FROM centos:6
RUN yum install -y rpm-build\
	make\
	tar\
	gcc\
	gcc-c++\
	epel-release\
        http://tmn.sovzond.center/yum/RPMS/noarch/sovzond-center-repo-1.0.0-1.el6.noarch.rpm\
  && yum clean all
RUN yum install -y ant armadillo-devel cfitsio-devel CharLS-devel chrpath curl-devel doxygen expat-devel fontconfig-devel freexl-devel g2clib-static geos-devel ghostscript hdf-devel hdf-static hdf5-devel jasper-devel jpackage-utils libgeotiff-devel libgta-devel libjpeg-devel libpng-devel libspatialite-devel libtiff-devel libwebp-devel libtool giflib-devel netcdf-devel libdap-devel librx-devel mysql-devel numpy pcre-devel ogdi-devel perl-ExtUtils-MakeMaker pkgconfig poppler-devel postgresql-devel proj-devel python27-szc-devel python27-numpy-szc sqlite-devel swig unixODBC-devel xerces-c-devel xz-devel zlib-devel java-1.8.0-openjdk-devel && yum clean all && echo  > /var/log/yum.log
WORKDIR /root 
COPY docker-entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh
ENTRYPOINT ["/bin/entrypoint.sh"]
