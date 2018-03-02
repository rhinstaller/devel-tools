from . import GeneralBranch, Branch


class Fedora23Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora23,
                         cmd_args=["-f23", "--fedora23"],
                         help="working on Fedora 23",
                         version="23.19.10")
