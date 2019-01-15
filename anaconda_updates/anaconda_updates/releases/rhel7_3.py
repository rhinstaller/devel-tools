
from . import GeneralBranch, Branch
from anaconda_updates.settings import GlobalSettings


class Rhel7_3Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel7_3,
                         cmd_args=["-rh7.3", "--rhel7.3"],
                         help="working on RHEL 7.3",
                         version="21.48.22.93",
                         img_name="rhel7.3_updates.img",
                         blivet_args=[], pykickstart_args=[])

        GlobalSettings.use_blivet = False
        GlobalSettings.use_pykickstart = False
