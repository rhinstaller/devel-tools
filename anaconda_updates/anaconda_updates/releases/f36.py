from . import GeneralBranch, Branch


class Fedora36Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora36,
                         cmd_args=["-f36", "--fedora36"],
                         help="working on Fedora 36",
                         version="36.16.6",
                         site_packages="./usr/lib/python3.10/site-packages/")
