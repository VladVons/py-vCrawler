#!/bin/bash


Downloads()
{
    url="https://as-it.ua/bu-noutbuk-122-lenovo-miix-510-12ikb-core-i5-7200u-25-ggc-8gb-ddr4-intel-hd-620-256gb-lte/"

    for ((i=1; i<=5; i++)) do 
      wget --user-agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)" -O "_util.wget.html" $url
      echo "try: $i"
      sleep 3
    done
}

PrettyHtml()
{
    file="itbox.ua.html"
    #tidy -indent -wrap 120 -o output.html $file
    #xmllint --format $file > output.html
}

# xmllint --format --output output.xml sitemap.xml
# cat sitemap.xml | grep -o '<loc>[^<]*</loc>' | sed 's/<loc>\(.*\)<\/loc>/\1/' > output.xml


Downloads
#PrettyHtml
