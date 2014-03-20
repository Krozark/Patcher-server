#!/bin/bash

gen-requirement.sh $1 /tmp/requirement.txt

read -e -p "User:" user
read -es -p "Password:" pass

url=$2

libs=`cat /tmp/requirement.txt | grep -E ^lib |sed 's/==/\.so\./g'`
version=`cat /tmp/requirement.txt |grep MyPackage== | tr -s '=' |cut -d= -f2`

major=`echo $version |cut -d. -f1`
minor=`echo $version |cut -d. -f2`
patch=`echo $version |cut -d. -f3`

os=`Monitoring-info | grep osName: |cut -d" " -f2`
bit=`Monitoring-info | grep osBit: |cut -d" " -f2`

#libs
for lib in $libs
do
    path=`ldconfig --print-cache |grep $lib | sed 's/=>/|/g' |cut -d"|" -f2 |head -n 1 | xargs readlink -m`
    curl -F "user=$user" -F "pass=$pass" -F "file=@$path" -F "filename=$lib" -F"soft=$1" -F"os=$os" -F "bit=$bit" -F "major=$major" -F "minor=$minor" -F "patch=$patch" -L "$2/patcher/push/" > "/dev/null"
done

#main
path=`readlink -m $1`
curl -F "user=$user" -F "pass=$pass" -F "file=@$path" -F "filename=$1" -F"soft=$1" -F"os=$os" -F "bit=$bit" -F "major=$major" -F "minor=$minor" -F "patch=$patch" -L "$2/patcher/push/" > "/dev/null"
