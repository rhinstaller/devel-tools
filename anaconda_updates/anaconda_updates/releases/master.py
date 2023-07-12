from . import GeneralBranch, Branch


class MasterBranch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.master,
                         cmd_args=["-m", "--master"], help="working on Rawhide",
                         version_script_params=["-m", "-p"],
                         site_packages="./usr/lib/python3.12/site-packages/")
