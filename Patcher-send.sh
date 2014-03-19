#!/bin/bash

gen-requirement.sh $1 /tmp/requirement.txt

url=$2

libs=`cat /tmp/requirement.txt | grep -E ^lib |sed 's/==/\.so\./g'`
version=`cat /tmp/requirement.txt |grep MyPackage== | tr -s '=' |cut -d= -f2`

major=`echo $version |cut -d. -f1`
minor=`echo $version |cut -d. -f2`
patch=`echo $version |cut -d. -f3`

for lib in $libs
do
    path=`ldconfig --print-cache |grep $lib | sed 's/=>/|/g' |cut -d"|" -f2 |head -n 1 | xargs readlink -m`
    echo "$lib : $path"
    curl -F "file=@$path" -F"soft=$1&os=Unix&bit=32&major=$major&minor=minor&patch=$patch" -L "$2/patcher/push/" > "out.html"
done
