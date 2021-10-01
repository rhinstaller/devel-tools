from . import GeneralBranch, Branch


class Fedora34Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora34,
                         cmd_args=["-f34", "--fedora34"],
                         help="working on Fedora 34",
                         version="34.24.9",
                         site_packages="./usr/lib/python3.9/site-packages/")
