#!/bin/bash
#Hostip="$(ip -4 -o a| grep docker0 | awk '{print $4}' | cut -d/ -f1)"
app="ifttt-bridge" 
docker run -d -p 5001:5000 --name=${app} -v $PWD:/app ${app} 
