from . import GeneralBranch, Branch


class Fedora30Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora30,
                         cmd_args=["-f30", "--fedora30"],
                         help="working on Fedora 30",
                         version="30.25.6")
