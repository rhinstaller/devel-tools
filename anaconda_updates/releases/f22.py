from . import GeneralBranch, Branch

class Fedora22Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora22,
                         cmd_args=["-f22", "--fedora22"],
                         help="working on Fedora 22",
                         version="22.20.13")
