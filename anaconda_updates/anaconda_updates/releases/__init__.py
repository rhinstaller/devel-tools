__all__ = ["Branch", "GeneralBranch", "master",
           "f22", "f23", "f24", "f25", "f26", "f27", "f28", "f29", "f30", "f31", "f32", "f33",
           "f34", "f35",
           "rhel6", "rhel6_8",
           "rhel7", "rhel7_1", "rhel7_2", "rhel7_3", "rhel7_4", "rhel7_5", "rhel7_6",
           "rhel8", "rhel9"]

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
    fedora32 = 12,
    fedora33 = 13,
    fedora34 = 14,
    fedora35 = 15,
    fedora36 = 16,
    fedora37 = 17,

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

    rhel9    = 300,


class GeneralBranch(object):
    def __init__(self, branch_type,
                 cmd_args, help,
                 version="", version_script_params=[], img_name="master_updates.img",
                 mkupdates_args=[],
                 site_packages="./run/install/updates/"):

        self.type = branch_type
        self.cmd_args = cmd_args
        self.help = help
        self._version = version
        self.img_name = img_name
        self.input_args = mkupdates_args
        self.show_version_params = version_script_params
        self.site_packages = site_packages

    @property
    def version(self):
        if self._version:
            return self._version

        return self._get_version()

    def add_argument(self, parse_args):
        parse_args.add_branch_param(*self.cmd_args, const_val=self.type,
                                    help=self.help)

    def _get_version(self):
        if not GlobalSettings.show_version_script_path:
            print("There is no script for detection of the Anaconda version.")
            return None

        path = os.path.expanduser(GlobalSettings.show_version_script_path)
        version = subprocess.check_output([path, *self.show_version_params]).decode()[:-1]
        return version
