from . import GeneralBranch, Branch


class Fedora35Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora35,
                         cmd_args=["-f35", "--fedora35"],
                         help="working on Fedora 35",
                         version="35.22.2",
                         site_packages="./usr/lib/python3.10/site-packages/")
