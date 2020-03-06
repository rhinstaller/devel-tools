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
        -rh8)
         PACKAGES_URL="rhel8/Packages"
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
        -f27)
         PACKAGES_URL="fedora27/Packages/a"
         shift
         ;;
        -f28)
         PACKAGES_URL="fedora28/Packages/a"
         shift
         ;;
        -f29)
         PACKAGES_URL="fedora29/Packages/a"
         shift
         ;;
        -f30)
         PACKAGES_URL="fedora30/Packages/a"
         shift
         ;;
        -f31)
         PACKAGES_URL="fedora31/Packages/a"
         shift
         ;;
        -f32)
         PACKAGES_URL="fedora32/Packages/a"
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
