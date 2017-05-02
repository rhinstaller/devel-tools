#!/bin/bash

# Set url of your repository server
BASE_URL="http://server.example.com"


PACKAGES_URL="rawhide/Packages/a"

VERSION_ONLY=false

for i in $@
do
    case $i in
        -m)
         shift
         ;;
        -rh7)
         PACKAGES_URL="rhel7/Packages"
         shift
         ;;
        -f23)
         PACKAGES_URL="fedora23/Packages/a"
         shift
         ;;
        -f24)
         PACKAGES_URL="fedora24/Packages/a"
         shift
         ;;
        -f25)
         PACKAGES_URL="fedora25/Packages/a"
         shift
         ;;
        -f26)
         PACKAGES_URL="fedora26/Packages/a"
         shift
         ;;
        -p)
         VERSION_ONLY=true
         shift
         ;;
    esac
done

if [[ $VERSION_ONLY = true ]]; then
    wget -qO- "$BASE_URL/$PACKAGES_URL" | grep -o -e "\"anaconda-.*.rpm\"" | sed "s/\"//g" | head -n 1 | sed 's/anaconda-\([0-9.]*\)-[0-9]*.*/\1/'
else
    echo "checking anaconda version: $PACKAGES_URL"
    wget -qO- "$BASE_URL/$PACKAGES_URL" | grep -o -e "\"anaconda-.*.rpm\"" | sed "s/\"//g" | head -n 1
fi
