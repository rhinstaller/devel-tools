from . import GeneralBranch, Branch


class Fedora29Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora29,
                         cmd_args=["-f29", "--fedora29"],
                         help="working on Fedora 29",
                         version_script_params=["-f29", "-p"])
