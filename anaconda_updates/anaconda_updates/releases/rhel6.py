from . import GeneralBranch, Branch
from anaconda_updates.settings import GlobalSettings


class Rhel6Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel6,
                         cmd_args=["-rh6", "--rhel6"],
                         help="working on RHEL6",
                         version_script_params=["-rh6", "-p"],
                         img_name="rhel6_updates.img")

        GlobalSettings.use_blivet = False
        GlobalSettings.use_pykickstart = False
