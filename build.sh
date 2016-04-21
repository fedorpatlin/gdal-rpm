#!/bin/bash
this=$(readlink -f $0)
workdir=$(dirname "$this")
projectname=$(echo $workdir | rev | cut -d/ -f1 | rev)
echo WORKDIR is $workdir
YUM_PACKAGES=$(grep "^BuildRequires" src/*.spec | awk '{print $2}' | xargs echo)
    echo "Dependencies will be installed: $YUM_PACKAGES"
if [ ! -z "$YUM_PACKAGES" ]; then
    YUM_COMMAND="RUN yum install -y $YUM_PACKAGES \&\& yum clean all \&\& echo  > /var/log/yum.log"
    echo "Docker file command is: $YUM_COMMAND"
else
    YUM_COMMAND=""
fi
sed -e "s+\$YUM_COMMAND_TEMPLATE+$YUM_COMMAND+" docker/Dockerfile.template > docker/Dockerfile
docker build --force-rm -t $projectname docker/ 
docker run -it --rm -v $workdir/src:/root/src -v $workdir/dest:/root/dest $projectname $projectname.spec
