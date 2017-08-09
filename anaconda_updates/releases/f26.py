from . import GeneralBranch, Branch

class Fedora26Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora26,
                         cmd_args=["-f26", "--fedora26"],
                         help="working on Fedora 26",
                         version="26.21.11")
