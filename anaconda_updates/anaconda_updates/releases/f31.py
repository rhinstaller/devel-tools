from . import GeneralBranch, Branch


class Fedora31Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora31,
                         cmd_args=["-f31", "--fedora31"],
                         help="working on Fedora 31",
                         version_script_params=["-f31", "-p"])
