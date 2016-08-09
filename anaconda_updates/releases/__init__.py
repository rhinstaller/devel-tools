__all__ = ["Branch", "GeneralBranch", "master", "rhel7", "f22", "f23", "f24"]

import subprocess
import os

from enum import Enum
from anaconda_updates.settings import GlobalSettings

class Branch(Enum):
    Nothing=0,

    master=1,
    fedora22=2,
    fedora23=3,
    fedora24=4,

    rhel6=10,

    rhel7=20,
    rhel7_1=21,
    rhel7_2=22


class GeneralBranch(object):
    def __init__(self, branch_type,
                 cmd_args, help,
                 version="", version_script_params=[], img_name="master_updates.img",
                 mkupdates_args=[],
                 blivet_args=["-i", "blivet"], pykickstart_args=["-i", "pykickstart"]):

        self.type = branch_type
        self.cmd_args = cmd_args
        self.help = help
        self.version = version
        self.img_name = img_name
        self.input_args = mkupdates_args
        self.blivet_args = blivet_args
        self.pykickstart_args = pykickstart_args
        self.show_version_params = version_script_params

        if not self.version:
            self.version = self.get_version()
            if not self.version:
                print(self.version)
                raise ValueError("Anaconda version is not set")


    def add_argument(self, parse_args):
        parse_args.add_branch_param(*self.cmd_args, const_val=self.type,
                                    help=self.help)

    def get_version(self):
        path = os.path.expanduser(GlobalSettings.show_version_script_path)
        return subprocess.check_output([path, *self.show_version_params]).decode()[:-1]

