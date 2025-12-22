#!/bin/bash

# Use Atriarch-Systems LinuxGSM fork (atriarch branch) for serverlist
curl -O "https://raw.githubusercontent.com/Atriarch-Systems/LinuxGSM/atriarch/lgsm/data/serverlist.csv"

echo -n "{" >"shortnamearray.json"
echo -n "\"include\":[" >>"shortnamearray.json"

while read line; do
  export shortname=$(echo "$line" | awk -F, '{ print $1 }')
  export servername=$(echo "$line" | awk -F, '{ print $2 }')
  export gamename=$(echo "$line" | awk -F, '{ print $3 }')
  export distro=$(echo "$line" | awk -F, '{ print $4 }')
  touch "dockerfiles/Dockerfile.${shortname}"
  echo "Generating Dockerfile.${shortname} (${gamename})"
  jinjanate Dockerfile.j2 >"dockerfiles/Dockerfile.${shortname}"
  echo -n "{" >>"shortnamearray.json"
  echo -n "\"shortname\":" >>"shortnamearray.json"
  echo -n "\"${shortname}\"" >>"shortnamearray.json"
  echo -n "}," >>"shortnamearray.json"
done < <(tail -n +2 serverlist.csv)
sed -i '$ s/.$//' "shortnamearray.json"
echo -n "]" >>"shortnamearray.json"
echo -n "}" >>"shortnamearray.json"
rm serverlist.csv