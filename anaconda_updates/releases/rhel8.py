from . import GeneralBranch, Branch


class Rhel8Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel8,
                         cmd_args=["-rh8", "--rhel8"],
                         help="working on RHEL 8",
                         img_name="rhel8_updates.img",
                         version_script_params=["-rh8", "-p"])
