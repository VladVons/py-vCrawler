#!/bin/bash


py=python3.12
Dir=~/virt/$py
source $Dir/bin/activate


#$py -B vCrawler.py --conf Server
#
#$py -B vCrawler.py --conf Dev
#$py -B vCrawler.py --conf Client
$py -B vCrawler.py --conf Service
