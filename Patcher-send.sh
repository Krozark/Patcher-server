#!/bin/bash

gen-requirement.sh $1 /tmp/requirement.txt

url=$2

libs=`cat /tmp/requirement.txt | grep -E ^lib |sed 's/==/\.so\./g'`
version=`cat /tmp/requirement.txt |grep MyPackage== | tr -s '=' |cut -d= -f2`

major=`echo $version |cut -d. -f1`
minor=`echo $version |cut -d. -f2`
patch=`echo $version |cut -d. -f3`

os=`Monitoring-info | grep osName: |cut -d" " -f2`
bit=`Monitoring-info | grep osBit: |cut -d" " -f2`

for lib in $libs
do
    path=`ldconfig --print-cache |grep $lib | sed 's/=>/|/g' |cut -d"|" -f2 |head -n 1 | xargs readlink -m`
    echo "$lib : $path"
    curl -F "file=@$path" -F"soft=$1" -F"os=$os" -F "bit=$bit" -F "major=$major" -F "minor=$minor" -F "patch=$patch" -L "$2/patcher/push/" > "/dev/null"
done
