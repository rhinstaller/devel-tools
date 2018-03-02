from . import GeneralBranch, Branch

class Fedora27Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora27,
                         cmd_args=["-f27", "--fedora27"],
                         help="working on Fedora 27",
                         version="27.20.4")
