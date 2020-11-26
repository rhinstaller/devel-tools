#!/usr/bin/python3
#
# Modify iso bootloader configuration by this tool. It's pretty valuable when you need to boot the
# iso with some specific arguments (inst.ks, inst.text, overlay...).
#
# TODO: Support not also UEFI bootloader configuration change.
#

import stat
import os

from argparse import ArgumentParser
from shutil import copy2
from tempfile import TemporaryDirectory

from lib import mount_iso, create_custom_dvd


ISOLINUX_PATH = "isolinux/isolinux.cfg"
INITRD_NAME = "overlay.img"


def parse_args():
    """Parse arguments for this tool."""
    parser = ArgumentParser(description="Tool to create testing DVD with multiple repositories.")

    parser.add_argument("iso", metavar="ISO",
                        help="""existing ISO file which already contains repository
                        (e.g. Fedora-Server-DVD.iso)""")
    parser.add_argument("-d", "--dest_iso", metavar="ISO", dest="dest_iso",
                        help="""destination ISO file with modified isolinux file""")
    parser.add_argument("-x", "--extract", action="store", dest="extract_path", metavar="DEST/PATH",
                        default=None,
                        help="""extract isolinux.cfg from the iso image on the given directory""")
    parser.add_argument("-i", "--import", action="store", dest="import_path",
                        metavar="ISOLINUX/PATH", default=None,
                        help="""import isolinux.cfg into the iso image""")
    parser.add_argument("-o", "--initrd_overlay", action="store", dest="initrd_overlay",
                        metavar="INITRD_OVERLAY/PATH", default=None,
                        help="""inject initrd overlay inside the image""")

    opt_args = parser.parse_args()

    if opt_args.import_path and not opt_args.dest_iso:
        raise ValueError("The -d/--dest_iso have to be specified when --import/-i is used.")

    if opt_args.initrd_overlay and not opt_args.dest_iso:
        raise ValueError("The -d/--dest_iso have to be specified when --initrd_overlay/-o is used.")

    return opt_args


def extract_isolinux_from_iso(iso, dest):
    """Extract isolinux.cfg from the given iso image.

    :param str iso: iso image for extraction
    :param str dest: where we should extract isolinux.cfg file
    """
    with mount_iso(iso) as mount_dir:
        copy2(f"{mount_dir}/isolinux/isolinux.cfg", dest)


def import_isolinux_to_iso(iso, dest_iso, isolinux_path):
    """Import isolinux.cfg into the give iso image.

    :param str iso: iso image
    :param str dest_iso: destination path for the output ISO image
    :param str isolinux_path: path to the modified isolinux config file
    """
    if not os.path.isfile(isolinux_path):
        raise ValueError("Provided isolinux.cfg path does not exists!")

    with TemporaryDirectory(prefix='graft-dir-') as temp_dir:
        _copy_isolinux_to_graftdir(isolinux_path, ISOLINUX_PATH, temp_dir)
        create_custom_dvd(iso, dest_iso, temp_dir)


def _copy_isolinux_to_graftdir(source_path, dest_path, graft_dir):
    if not os.path.isdir(graft_dir):
        raise ValueError(f"Graft directory {graft_dir} does not exists!")

    _make_graft_dirs(graft_dir, dest_path)

    dest_isolinux_path = f"{graft_dir}/{dest_path}"

    _copy_file(source_path, dest_isolinux_path)


def _copy_file(source_file, dest_path):
    """Copy file to with correct permissions for bootloader ISO.

    :param str source_file: file we want to copy
    :param str dest_path: destination path
    """
    copy2(source_file, dest_path)
    # set 444 mod
    os.chmod(dest_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def _make_graft_dirs(graft_dir, dest_file_path):
    """Create directories in the graft directory.

    :param str graft_dir: path to the graft directory
    :param str dest_file_path: path to the file inside of graft directory (relative from graft_dir)
    """
    directories, _ = os.path.split(dest_file_path)
    os.makedirs(f"{graft_dir}/{directories}", exist_ok=True)


def inject_initrd_overlay_to_iso(iso, dest_iso, initrd_overlay_path):
    """Inject initrd overlay to the iso image and change bootloader configuration properly.

    :param str iso: source iso image
    :param str dest_iso: destination path for the output ISO image
    :param str initrd_overlay_path: path to the initrd overlay we want to inject
    """
    if not os.path.isfile(initrd_overlay_path):
        raise ValueError("Initrd overlay file does not exists!")

    with TemporaryDirectory(prefix='inject-initrd-graft-dir') as graft_dir:
        _make_graft_dirs(graft_dir, ISOLINUX_PATH)
        dest_path = f"{graft_dir}/{ISOLINUX_PATH}"
        extract_isolinux_from_iso(iso, dest_path)
        _copy_file(initrd_overlay_path, f"{graft_dir}/isolinux/{INITRD_NAME}")

        _add_overlay_to_isolinux_config(dest_path, INITRD_NAME)

        create_custom_dvd(iso, dest_iso, graft_dir)


def _add_overlay_to_isolinux_config(isolinux_path, bootloader_initrd_path):
    """Inject initrd to the isolinux configuration file."""
    content = ""

    with open(isolinux_path, 'rt') as f:
        content = f.read()

    content = content.replace("append initrd=initrd.img",
                              f"append initrd=initrd.img,{bootloader_initrd_path}")

    with open(isolinux_path, 'wt') as f:
        f.write(content)


if __name__ == "__main__":
    opt = parse_args()

    if opt.extract_path:
        extract_isolinux_from_iso(opt.iso, opt.extract_path)
    if opt.import_path and opt.dest_iso:
        import_isolinux_to_iso(opt.iso, opt.dest_iso, opt.import_path)
    if opt.initrd_overlay:
        inject_initrd_overlay_to_iso(opt.iso, opt.dest_iso, opt.initrd_overlay)
