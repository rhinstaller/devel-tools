from . import GeneralBranch, Branch

class Fedora25Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora25,
                         cmd_args=["-f25", "--fedora25"],
                         help="working on Fedora 25",
                         version="25.20.9")
