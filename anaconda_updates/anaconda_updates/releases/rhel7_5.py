
from . import GeneralBranch, Branch
from anaconda_updates.settings import GlobalSettings


class Rhel7_5Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel7_5,
                         cmd_args=["-rh7.5", "--rhel7.5"],
                         help="working on RHEL 7.5",
                         version="21.48.22.134",
                         img_name="rhel7.5_updates.img",
                         blivet_args=[], pykickstart_args=[])

        GlobalSettings.use_blivet = False
        GlobalSettings.use_pykickstart = False
