#!/usr/bin/python3
#
# Modify iso bootloader configuration by this tool. It's pretty valuable when you need to boot the
# iso with some specific arguments (inst.ks, inst.text, overlay...).
#

from argparse import ArgumentParser
from shutil import copy2

from lib import mount_iso


def parse_args():
    """Parse arguments for this tool."""
    parser = ArgumentParser(description="Tool to create testing DVD with multiple repositories.")

    parser.add_argument("iso", metavar="ISO",
                        help="""existing ISO file which already contains repository
                        (e.g. Fedora-Server-DVD.iso)""")
    parser.add_argument("-x", "--extract", action="store", dest="extract_path", metavar="DEST/PATH",
                        default=None,
                        help="""extract isolinux.cfg from the iso image on the given directory""")

    return parser.parse_args()


def extract_isolinux_from_iso(iso, dest):
    """Extract isolinux.cfg from the given iso image.

    :param str iso: iso image for extraction
    :param str dest: where we should extract isolinux.cfg file
    """
    with mount_iso(iso) as mount_dir:
        copy2(f"{mount_dir}/isolinux/isolinux.cfg", dest)


if __name__ == "__main__":
    opt = parse_args()

    if opt.extract_path:
        extract_isolinux_from_iso(opt.iso, opt.extract_path)
