from . import GeneralBranch, Branch


class Fedora32Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora32,
                         cmd_args=["-f32", "--fedora32"],
                         help="working on Fedora 32",
                         version="32.24.7")
