from . import GeneralBranch, Branch


class Fedora28Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora28,
                         cmd_args=["-f28", "--fedora28"],
                         help="working on Fedora 28",
                         version_script_params=["-f28", "-p"])
