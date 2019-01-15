__all__ = ["Branch", "GeneralBranch", "master",
           "f22", "f23", "f24", "f25", "f26", "f27", "f28", "f29",
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

    rhel6    = 10,
    rhel6_8  = 11,

    rhel7    = 20,
    rhel7_1  = 21,
    rhel7_2  = 22,
    rhel7_3  = 23,
    rhel7_4  = 24,
    rhel7_5  = 25,
    rhel7_6  = 26,

    rhel8    = 30,


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
