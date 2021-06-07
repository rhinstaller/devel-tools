# Tooling to help with installation image modifications

These scripts should help with debugging of Anaconda use-cases where we need an ISO but the ISO is not available in a shape which would help us. Please feel free to abuse the scripts as much as you need but don't expect they will do everything. However, as always patches are **welcome**.

## Prerequisites

You need to download existing DVD iso. You can obtain it on [get fedora site](https://getfedora.org).

Please make sure you have these tools:

```
guestmount
fusermount
pungi-patch-iso
```

And these python libraries:

```
rpmfluff
```

## What can be found here

Below you will find scripts which should help you with your tasks:

* [`create_dvd`](#create_dvd)
* [`modify_iso_bootloader`](#modify_iso_bootloader)

# create_dvd

## Reasoning

The unified ISO is a functionality when .treeinfo file will provide you multiple repositories. These repositories are then automatically loaded into the installation environment as additional repositories used for installation. This functionality is not yet used on Fedora. To be able to test this functionality this script was created.

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


# modify_iso_bootloader

## Reasoning

Modify bootloader configuration file in the ISO by this script. Avoid constant typing of inst.updates, inst.text... It can also help with common use-cases (injecting initrd to the boot.iso image).

## How to use

You can easily change the output ISO again and again if you want to get your ideal result. So in general you are free to combine use-cases below as you need.

### Adding kernel boot arguments

The most common use case will be to change bootloader defaults to avoid contant re-typing for each boot during debugging of the boot.iso. To do that please follow the steps below.

```
./modify_iso_bootloader.py -x *./isolinux.cfg* *path/to/source/iso*
vim ./isolinux.cfg # do required changes
./modify_iso_bootloader.py -i *./isolinux.cfg* -d *./output.iso* *path/to/source/iso*
```

You should be able to add any required boot option this way.

### Injecting initrd overlay

Another common use-case is to inject overlay to the image. This normally requires two steps. Inject initrd overlay to the ISO and change isolinux.cfg file. However, you can do that with just one command here.

```
./modify_iso_bootloader.py -o ./my-overlay-imag.img -d *./output.iso* *path/to/source/iso*
```

## Author:

Jiří Konečný <jkonecny@redhat.com>
