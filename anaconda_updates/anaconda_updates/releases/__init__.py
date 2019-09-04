__all__ = ["Branch", "GeneralBranch", "master",
           "f22", "f23", "f24", "f25", "f26", "f27", "f28", "f29", "f30", "f31",
           "rhel6", "rhel6_8",
           "rhel7", "rhel7_1", "rhel7_2", "rhel7_3", "rhel7_4", "rhel7_5", "rhel7_6",
           "rhel8"]

import subprocess
import os

from enum import Enum
from anaconda_updates.settings import GlobalSettings


class Branch(Enum):
    Nothing  = 0,

    master   = 1,
    fedora22 = 2,
    fedora23 = 3,
    fedora24 = 4,
    fedora25 = 5,
    fedora26 = 6,
    fedora27 = 7,
    fedora28 = 8,
    fedora29 = 9,
    fedora30 = 10,
    fedora31 = 11,

    rhel6    = 50,
    rhel6_8  = 51,

    rhel7    = 100,
    rhel7_1  = 101,
    rhel7_2  = 102,
    rhel7_3  = 103,
    rhel7_4  = 104,
    rhel7_5  = 105,
    rhel7_6  = 106,

    rhel8    = 200,


class GeneralBranch(object):
    def __init__(self, branch_type,
                 cmd_args, help,
                 version="", version_script_params=[], img_name="master_updates.img",
                 mkupdates_args=[],
                 blivet_args=["-i", "blivet"],
                 pykickstart_args=["-i", "pykickstart"],
                 simpleline_args=["-i", "simpleline"]):

        self.type = branch_type
        self.cmd_args = cmd_args
        self.help = help
        self.version = version
        self.img_name = img_name
        self.input_args = mkupdates_args
        self.blivet_args = blivet_args
        self.pykickstart_args = pykickstart_args
        self.simpleline_args = simpleline_args
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
