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

#pip3 install --upgrade pip
#pip3 install playwright
#playwright install chromium

#pip3 install jsonfix
