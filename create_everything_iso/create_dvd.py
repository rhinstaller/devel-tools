#!/usr/bin/python3

import subprocess
import os
import time
import shutil

from tempfile import mkdtemp
from productmd.treeinfo import TreeInfo, Variant


FEDORA_REPO_NAME = "Fedora"
ARCH = "x86_64"

TREE_INFO_FILE_NAME = "treeinfo"


# Sources:
#
# /usr/bin/genisoimage -untranslated-filenames -volid RHEL-8-0-0-BaseOS-x86_64 -J -joliet-long -rational-rock -translation-table -input-charset utf-8 -x ./lost+found -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -eltorito-alt-boot -e images/efiboot.img -no-emul-boot -o RHEL-8.0.0-20190404.2-x86_64-dvd1.iso -graft-points -path-list /mnt/redhat/rhel-8/devel/candidate-trees/RHEL-8/RHEL-8.0.0-20190404.2/work/x86_64/iso/RHEL-8.0.0-20190404.2-x86_64-dvd1.iso-graft-points
#
# /usr/bin/isohybrid --uefi RHEL-8.0.0-20190404.2-x86_64-dvd1.iso
# /usr/bin/implantisomd5 --supported-iso RHEL-8.0.0-20190404.2-x86_64-dvd1.iso

def make_subprocess_call(command):
    print("Running:\n'{}'".format(command))
    ret = subprocess.run(command)

    ret.check_returncode()


def create_treeinfo(path):
    ti = TreeInfo()

    ti.release.name = "Fedora"
    ti.release.short = "Fedora"
    ti.release.version = "31"

    ti.tree.arch = ARCH
    ti.tree.build_timestamp = time.time()
    ti.tree.platforms.add(ARCH)

    images = {"efiboot.img": "images/efiboot.img",
              "initrd": "images/pxeboot/initrd.img",
              "kernel": "images/pxeboot/vmlinuz"
              }
    ti.images.images[ARCH] = images

    variant = Variant(ti)
    variant.id = "Server"
    variant.uid = "Server"
    variant.name = "Server"
    variant.type = "variant"

    variant.paths.repository = FEDORA_REPO_NAME
    variant.paths.packages = "{}/Packages".format(FEDORA_REPO_NAME)

    ti.variants.add(variant)

    _create_custom_variant(ti)

    ti.dump(path)


def _create_custom_variant(tree_info):
    variant = Variant(tree_info)

    variant.id = "Custom"
    variant.uid = "Custom"
    variant.name = "Custom"
    variant.type = "variant"

    tree_info.variants.add(variant)


def create_custom_repo(temp_dir):
    pass


def create_temp_dir():
    return mkdtemp(prefix="dvd_iso-")


def remove_temp_dir(temp_dir):
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    temp_dir = create_temp_dir()

    tree_info_path = os.path.join(temp_dir, TREE_INFO_FILE_NAME)
    create_treeinfo(tree_info_path)

    print("Everything created in", temp_dir)
