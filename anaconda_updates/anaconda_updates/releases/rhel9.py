from . import GeneralBranch, Branch


class Rhel9Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.rhel9,
                         cmd_args=["-rh9", "--rhel9"],
                         help="working on RHEL 9",
                         img_name="rhel9_updates.img",
                         version_script_params=["-rh9", "-p"],
                         site_packages="./usr/lib/python3.9/site-packages/")
