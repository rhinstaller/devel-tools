
from . import GeneralBranch, Branch
from anaconda_updates.settings import GlobalSettings


class Rhel7_6Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel7_6,
                         cmd_args=["-rh7.6", "--rhel7.6"],
                         help="working on RHEL 7.6",
                         version="21.48.22.147",
                         img_name="rhel7.6_updates.img")

        GlobalSettings.use_blivet = False
        GlobalSettings.use_pykickstart = False
