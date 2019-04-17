#!/usr/bin/python3

import subprocess
import os
import shutil

from argparse import ArgumentParser
from tempfile import mkdtemp, TemporaryDirectory
from contextlib import contextmanager
from productmd.treeinfo import TreeInfo, Variant
from rpmfluff import SimpleRpmBuild, SourceFile


FEDORA_REPO_NAME = "Fedora"
ARCH = "x86_64"

TREE_INFO_FILE_NAME = ".treeinfo"
CUSTOM_REPO_NAME = "Custom"


# Sources:
#
# /usr/bin/genisoimage -untranslated-filenames -volid RHEL-8-0-0-BaseOS-x86_64 -J -joliet-long -rational-rock -translation-table -input-charset utf-8 -x ./lost+found -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -eltorito-alt-boot -e images/efiboot.img -no-emul-boot -o RHEL-8.0.0-20190404.2-x86_64-dvd1.iso -graft-points -path-list /mnt/redhat/rhel-8/devel/candidate-trees/RHEL-8/RHEL-8.0.0-20190404.2/work/x86_64/iso/RHEL-8.0.0-20190404.2-x86_64-dvd1.iso-graft-points
#
# /usr/bin/isohybrid --uefi RHEL-8.0.0-20190404.2-x86_64-dvd1.iso
# /usr/bin/implantisomd5 --supported-iso RHEL-8.0.0-20190404.2-x86_64-dvd1.iso

def _make_subprocess_call(command, env=None):
    print("------------------------")
    print("Running:\n'{}'".format(" ".join(command)))
    ret = subprocess.run(command, env=env)
    print("------------------------")

    ret.check_returncode()


@contextmanager
def mount_iso(image):
    with TemporaryDirectory(prefix='create-dvd-iso-mount-') as mount_dir:
        # use guestmount to mount the image, which doesn't require root privileges
        # LIBGUESTFS_BACKEND=direct: running qemu directly without libvirt
        env = {'LIBGUESTFS_BACKEND': 'direct'}
        cmd = ["guestmount", "-a", image, "-m", "/dev/sda", "--ro", mount_dir]
        _make_subprocess_call(cmd, env=env)

        try:
            yield mount_dir
        finally:
            _make_subprocess_call(['fusermount', '-u', mount_dir])


def create_custom_dvd(source_iso, graft_dir, output_iso):
    cmd = ["pungi-patch-iso"]

    cmd.append(output_iso)
    cmd.append(source_iso)
    cmd.append(graft_dir)

    _make_subprocess_call(cmd)


def obtain_existing_treeinfo_content(iso):
    with mount_iso(iso) as mount_dir:
        tree_info_path = os.path.join(mount_dir, ".treeinfo")
        if not os.path.exists(tree_info_path):
            raise RuntimeError("Can't find .treeinfo file on the source DVD ISO")

        with open(tree_info_path, "rt") as fd:
            return fd.read()


def append_custom_repo_to_treeinfo(treeinfo_content, path):
    ti = TreeInfo()
    ti.loads(treeinfo_content)

    variant = Variant(ti)

    variant.id = CUSTOM_REPO_NAME
    variant.uid = CUSTOM_REPO_NAME
    variant.name = CUSTOM_REPO_NAME
    variant.type = "variant"

    ti.variants.add(variant)

    ti.dump(path)


def create_custom_repo(temp_dir):
    rpm_file = _create_fake_rpm(temp_dir)
    repo_dir = os.path.join(temp_dir, CUSTOM_REPO_NAME)
    packages_dir = os.path.join(repo_dir, "Packages")

    os.mkdir(repo_dir)
    os.makedirs(packages_dir)
    shutil.copy2(rpm_file, packages_dir)

    _create_repo(repo_dir)

    return repo_dir


def _create_fake_rpm(temp_dir):
    rpm = SimpleRpmBuild(name="test-rpm", version="200", release="9000")
    rpm.add_installed_file(installPath="/usr/bin/TEST",
                           sourceFile=SourceFile(sourceName="TEST",
                                                 content="SO AWESOME APP!")
                           )
    with switch_workdir(temp_dir):
        rpm.make()

    rpm_rel_path = rpm.get_built_rpm(ARCH)
    return os.path.join(temp_dir, rpm_rel_path)


def _create_repo(repo_dir):
    _make_subprocess_call(["createrepo_c", repo_dir])


@contextmanager
def switch_workdir(dir):
    """This is a context manager to temporary switch the current directory.

    This function should be used with `with` keyword.
    """
    old_cwd = os.getcwd()
    os.chdir(dir)
    yield
    os.chdir(old_cwd)


def create_temp_dir():
    return mkdtemp(prefix="dvd_iso-")


def remove_temp_dir(temp_dir):
    shutil.rmtree(temp_dir)


def parse_args():
    parser = ArgumentParser(description="Tool to create testing DVD with multiple repositories.")

    parser.add_argument("source_iso", metavar="SOURCE_ISO",
                        help="""existing source ISO file which already contains repository
                        (e.g. Fedora-Server-DVD.iso)""")
    parser.add_argument("output_iso", metavar="OUTPUT_ISO",
                        help="""path to the output ISO file""")

    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_args()
    temp_dir = create_temp_dir()

    tree_info_path = os.path.join(temp_dir, TREE_INFO_FILE_NAME)
    orig_tree_info_content = obtain_existing_treeinfo_content(opt.source_iso)
    append_custom_repo_to_treeinfo(orig_tree_info_content, tree_info_path)
    create_custom_repo(temp_dir)
    create_custom_dvd(opt.source_iso, temp_dir, opt.output_iso)
