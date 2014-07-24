#!/bin/bash

echo "Usage : Patcher-send.sh soft base/url/patcher/push [requirement.txt]"

out="out.txt"
in="/tmp/requirement.txt"
if [[ -z $3 ]]
then
    gen-requirement.sh $1 /tmp/requirement.txt
else
    cat $3 > $in
fi

read -e -p "User:" user
read -es -p "Password:" pass

echo "Connect to $2 using user: $user" > $out

url=$2

libs=`cat $in | grep -E ^lib |sed 's/==/\.so\./g'`
version=`cat $in |grep MyPackage== | tr -s '=' |cut -d= -f2`

major=`echo $version |cut -d. -f1`
minor=`echo $version |cut -d. -f2`
patch=`echo $version |cut -d. -f3`

os=`Monitoring-info | grep osName: |cut -d" " -f2`
bit=`Monitoring-info | grep osBit: |cut -d" " -f2`

#libs
for lib in $libs
do
    path=`ldconfig --print-cache |grep $lib | sed 's/=>/|/g' |cut -d"|" -f2 |head -n 1 | xargs readlink -m`
    echo "== send file $lib (path=$path) ==" >> $out
    echo "response : ">> $out
    curl -F "user=$user" -F "pass=$pass" -F "file=@$path" -F "filename=$lib" -F"soft=$1" -F"os=$os" -F "bit=$bit" -F "major=$major" -F "minor=$minor" -F "patch=$patch" -L "$2/patcher/push/" >> $out
    echo "">> $out
done

#main
path=`readlink -m $1`
echo "== send exe file $1 (path=$path) ==" >> $out
echo "response : ">> $out
curl -F "user=$user" -F "pass=$pass" -F "file=@$path" -F "filename=$1" -F"soft=$1" -F"os=$os" -F "bit=$bit" -F "major=$major" -F "minor=$minor" -F "patch=$patch" -L "$2/patcher/push/" >> $out
