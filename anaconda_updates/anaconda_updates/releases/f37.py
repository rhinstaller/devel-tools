from . import GeneralBranch, Branch


class Fedora37Branch(GeneralBranch):

    def __init__(self):
        super().__init__(branch_type=Branch.fedora37,
                         cmd_args=["-f37", "--fedora37"],
                         help="working on Fedora 37",
                         version_script_params=["-f37", "-p"],
                         site_packages="./usr/lib/python3.11/site-packages/")
