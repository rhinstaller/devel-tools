# Create unified DVD

## Reasoning

The unified ISO is a functionality when .treeinfo file will provide you multiple repositories. These repositories are then automatically loaded into the installation environment as additional repositories used for installation. This functionality is not yet used on Fedora. To be able to test this functionality this script was created.

## Prerequisites

You need to download existing DVD iso. You can obtain it on [get fedora site](https://getfedora.org).

Please make sure you have these tools:

```
guestmount
fusermount
pungi-patch-iso
```

## How to run

This tool is pretty simple to use.

```
./create_dvd.py *path/to/the/source/iso* *path/to/the/output/iso*
```

You can also use `-v` option to enable verbose output.

## Author:

Jiří Konečný <jkonecny@redhat.com>
