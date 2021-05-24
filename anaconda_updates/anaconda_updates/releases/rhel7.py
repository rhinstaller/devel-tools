from . import GeneralBranch, Branch


class Rhel7Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel7,
                         cmd_args=["-rh7", "--rhel7"],
                         help="working on RHEL7",
                         version_script_params=["-rh7", "-p"],
                         img_name="rhel7_updates.img")

