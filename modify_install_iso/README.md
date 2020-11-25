# Tooling to help with installation image modifications

These scripts should help with debugging of Anaconda use-cases where we need an ISO but the ISO is not available in a shape which would help us. Please feel free to abuse the scripts as much as you need but don't expect they will do everything. However, as always patches are **welcome**.

Below you will find scripts which should help you with your tasks:

* [`create_dvd`](#create_dvd)

# create_dvd

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

## How to use

This tool is specifically designed to help testing of unified functionality which is not used on Fedora but pretty important in RHEL-8. To solve this issue the tool will create DVD.iso pretty similar to RHEL one but with Fedora and fake repository.

### Booting locally

Just use the DVD.iso to boot the system and see logs if the second repository was loaded or look into the Source Spoke.

### Test remote installation

Run HTTP/FTP/NFS (based on what needs to be tested) server and mount the DVD.iso there. This is recommended way even for RHEL so it is just using the same steps with our adjusted dvd.iso.

For how to run HTTP server with custom certificate please look [here](https://docs.fedoraproject.org/en-US/quick-docs/getting-started-with-apache-http-server/).

## Author:

Jiří Konečný <jkonecny@redhat.com>
