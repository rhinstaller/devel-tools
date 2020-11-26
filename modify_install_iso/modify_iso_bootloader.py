#!/usr/bin/python3
#
# Modify iso bootloader configuration by this tool. It's pretty valuable when you need to boot the
# iso with some specific arguments (inst.ks, inst.text, overlay...).
#

import stat
import os

from argparse import ArgumentParser
from shutil import copy2
from tempfile import TemporaryDirectory

from lib import mount_iso, create_custom_dvd


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

    opt_args = parser.parse_args()

    if opt_args.import_path and not opt_args.dest_iso:
        raise ValueError("The -d/--dest_iso have to be specified when --import/-i is used.")

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

    file_name = os.path.basename(isolinux_path)

    with TemporaryDirectory(prefix='graft-dir-') as temp_dir:
        dest_isolinux_path = f"{temp_dir}/isolinux/isolinux.cfg"
        os.mkdir(f"{temp_dir}/isolinux")
        copy2(file_name, dest_isolinux_path)
        # set 444 mod
        os.chmod(dest_isolinux_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        create_custom_dvd(iso, dest_iso, temp_dir)

if __name__ == "__main__":
    opt = parse_args()

    if opt.extract_path:
        extract_isolinux_from_iso(opt.iso, opt.extract_path)
    if opt.import_path and opt.dest_iso:
        import_isolinux_to_iso(opt.iso, opt.dest_iso, opt.import_path)
