from . import GeneralBranch, Branch


class Fedora33Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora33,
                         cmd_args=["-f33", "--fedora33"],
                         help="working on Fedora 33",
                         version="33.25.4")
