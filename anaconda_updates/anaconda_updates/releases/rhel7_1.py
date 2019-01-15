from . import GeneralBranch, Branch
from anaconda_updates.settings import GlobalSettings


class Rhel7_1Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel7_1,
                         cmd_args=["-rh7.1", "--rhel7.1"],
                         help="working on RHEL7",
                         version="19.31.123",
                         img_name="rhel7.1_updates.img",
                         blivet_args=[], pykickstart_args=[])

        GlobalSettings.use_blivet = False
        GlobalSettings.use_pykickstart = False
