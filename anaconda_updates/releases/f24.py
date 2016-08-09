from . import GeneralBranch, Branch

class Fedora24Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora24,
                         cmd_args=["-f24", "--fedora24"],
                         help="working on Fedora 24",
                         version="24.13.7")
