#!/bin/bash


py=python3
Dir=~/virt/python3
Src=$Dir/bin/activate
echo "env: $Src"
source $Src

#$py -B vCrawler.py --conf Server
#
#$py -B vCrawler.py --conf Dev
#$py -B vCrawler.py --conf Client
python3 -B vCrawler.py --conf Service
