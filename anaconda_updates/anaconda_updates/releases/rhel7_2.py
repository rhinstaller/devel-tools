
from . import GeneralBranch, Branch
from anaconda_updates.settings import GlobalSettings


class Rhel7_2Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel7_2,
                         cmd_args=["-rh7.2", "--rhel7.2"],
                         help="working on RHEL 7.2",
                         version="21.48.22.56",
                         img_name="rhel7.2_updates.img")

        GlobalSettings.use_blivet = False
        GlobalSettings.use_pykickstart = False
