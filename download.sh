#!/bin/bash


Downloads()
{
    url="https://exe.ua/ua"

    loops=3
    for ((i=1; i<=$loops; i++)) do 
      #wget --user-agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)" -O "_util.wget.html" $url
      #wget --header="Cookie: PHPSESSID=a0ad7a215a73117700948f3bf8cfe664" --user-agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)" -O "_util.wget.html" $url
      wget --header="Cookie: PHPSESSID=8d86cbd6b2c0f1a9c501d4169d716b0b" --user-agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)" -O "_util.wget.html" $url
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
