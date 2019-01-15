
from . import GeneralBranch, Branch
from anaconda_updates.settings import GlobalSettings


class Rhel7_4Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel7_4,
                         cmd_args=["-rh7.4", "--rhel7.4"],
                         help="working on RHEL 7.4",
                         version="21.48.22.121",
                         img_name="rhel7.4_updates.img",
                         blivet_args=[], pykickstart_args=[])

        GlobalSettings.use_blivet = False
        GlobalSettings.use_pykickstart = False
