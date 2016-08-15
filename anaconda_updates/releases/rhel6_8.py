from . import GeneralBranch, Branch
from anaconda_updates.settings import GlobalSettings

class Rhel6_8Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel6_8,
                         cmd_args=["-rh6.8", "--rhel6.8"],
                         help="working on RHEL6",
                         version="13.21.254",
                         img_name="rhel6_updates.img")

        GlobalSettings.use_blivet=False
        GlobalSettings.use_pykickstart=False
        GlobalSettings.auto_fetch=False
