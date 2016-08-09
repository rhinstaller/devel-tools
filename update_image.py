#!/usr/bin/python3

import subprocess
import os
import sys
import shutil

from argparse import ArgumentParser

from anaconda_updates import *
from anaconda_updates.settings import GlobalSettings

class DirectoryNotFoundError(Exception):
    pass


#class Fedora22Branch(GeneralBranch):
#    type = Branch.fedora22
#    cmd_args = ["-f22", "--fedora22"]
#    help = "working on Fedora 22"
#    img_name = "master_updates.img"
#    input_args = []
#    version = "22.20.13"
#
#
#class Fedora23Branch(GeneralBranch):
#    type = Branch.fedora23
#    cmd_args = ["-f23", "--fedora23"]
#    help = "working on Fedora 23"
#    img_name = "master_updates.img"
#    input_args = []
#    version = "23.19.10"
#
#
#class Fedora24Branch(GeneralBranch):
#    type = Branch.fedora24
#    cmd_args = ["-f24", "--fedora24"]
#    help = "working on Fedora 24"
#    img_name = "master_updates.img"
#    input_args = []
#    version = "24.13.7"


#class Rhel7Branch(GeneralBranch):
#
#    def __init__(self):
#        super().__init__(branch_type=Branch.rhel7, img_name="rhel7_updates.img",
#                         cmd_args=["-rh7", "--rhel7"], help="working on RHEL7",
#                         version_script_params=["-rh7", "-p"])


#class Rhel6Branch(GeneralBranch):
#    type = Branch.rhel6
#    cmd_args = ["-rh6", "--rhel6"]
#    help = "working on RHEL6"
#    img_name = "rhel6_updates.img"
#    #input_args = ["-i", "blivet*", "-i", "pykickstart*", "-f", "x86_64"]
#    input_args = []
#    version = ""
#
#    def prepare_params(self):
#        self.__class__.version = subprocess.check_output(["./show_version.sh", "-rh6", "-p"]).decode()[:-1]
#        GlobalSettings.use_blivet=False
#        GlobalSettings.use_pykickstart=False
#        super().prepare_params()
#
#class Rhel7_1Branch(GeneralBranch):
#    type = Branch.rhel7_1
#    cmd_args = ["-rh7.1", "--rhel7.1"]
#    help = "working on RHEL7.1"
#    img_name = "rhel7.1_updates.img"
#    #input_args = ["-i", "blivet*", "-i", "pykickstart*", "-f", "x86_64"]
#    input_args = []
#    version = "19.31.123"
#
#    def prepare_params(self):
#        GlobalSettings.use_blivet=False
#        GlobalSettings.use_pykickstart=False
#        super().prepare_params()
#
#class Rhel7_2Branch(GeneralBranch):
#    type = Branch.rhel7_2
#    cmd_args = ["-rh7.2", "--rhel7.2"]
#    help = "working on RHEL7.2"
#    img_name = "rhel7.2_updates.img"
#    #input_args = ["-i", "blivet*", "-i", "pykickstart*", "-f", "x86_64"]
#    input_args = []
#    version = "21.48.22.56"
#
#    def prepare_params(self):
#        GlobalSettings.use_blivet=False
#        GlobalSettings.use_pykickstart=False
#        super().prepare_params()

## Logic code ##

class ParseArgs(ArgumentParser):
    def __init__(self):
        super().__init__()

        self._branch_group = self.add_mutually_exclusive_group(required=True)

        self.add_argument("-a", dest="alternative_dir", action="store_true",
                          help="use alternative anaconda-2 folder")
        self.add_argument("-p", dest="push_only", action="store_true",
                          help=("create image from existing contents in the update folder."
                                "Must be used with some branch target."))
        self.add_argument("-k", "--keep", dest="keep", action="store_true",
                          help="keep content of folder after image creation")
        self.add_argument("-c", "--compile", dest="compile", action="store_true",
                          help="compile anaconda before push")
        self.add_argument("-f", dest="no_fetch", action="store_true",
                          help="turn off autofetch dependencies for x86_64")
        self.add_argument("-t", "--target", dest="target_version", nargs=1, action="store",
                          metavar="version",
                          help=("set target version from command line. Use in git format"
                                "If not set, use branch specific."))
        self.add_argument("--blivet", dest="use_blivet", action="store_true",
                          help=("copy blivet to updates image."))
        self.add_argument("--pykickstart", dest="use_pykickstart", action="store_true",
                          help=("copy pykickstart to updates image."))
        self.add_argument("--add-addon", dest="add_addon", nargs=1, action="store",
                          metavar="path",
                          help=("add addon to the updates image structure. "
                                "Can be combined with -p to only update addon."))
        self.add_argument("--add-rpm", dest="add_rpm", nargs='+', action="store",
                          metavar="paths",
                          help=("add RPM packages to updates image. "
                                "You can use blob in later make_updates"))


    def add_branch_param(self, *args, const_val, help):
        self._branch_group.add_argument(*args, dest="branch",
                                        action="store_const", const=const_val,
                                        help=help)

    def parse_args(self):
        self.nm = super().parse_args()

        if self.nm.push_only:
            GlobalSettings.push_only = True
        if self.nm.alternative_dir:
            GlobalSettings.anaconda_path="anaconda-2"
        if self.nm.add_addon:
            expanded = os.path.expanduser(self.nm.add_addon[0])
            GlobalSettings.AddonDir=os.path.normpath(expanded)
        if self.nm.no_fetch:
            GlobalSettings.auto_fetch=False
        if self.nm.add_rpm:
            GlobalSettings.add_RPM.extend(self.nm.add_rpm)
        if self.nm.target_version:
            GlobalSettings.target=self.nm.target_version[0]
        if self.nm.use_blivet:
            GlobalSettings.use_blivet=True
        if self.nm.use_pykickstart:
            GlobalSettings.use_pykickstart=True

        return self.nm


class CreateCommand(object):
    def __init__(self, branch):
        super().__init__()
        self._branch_obj = branch

    def create_command(self, keep, compile):
        cmd = ["./scripts/makeupdates"]

        if keep:
            cmd.append("-k")

        if GlobalSettings.push_only:
            # create only from top so from top
            cmd.append("-t")
            cmd.append("HEAD")
        else:
            version = self._branch_obj.version
            input_args = self._branch_obj.input_args

            if compile:
                cmd.append("-c")

            if GlobalSettings.use_blivet:
                input_args.extend(self._branch_obj.blivet_args)
            if GlobalSettings.use_pykickstart:
                input_args.extend(self._branch_obj.pykickstart_args)
            if GlobalSettings.auto_fetch:
                input_args.extend(["-f", "x86_64"])

            for rpm in GlobalSettings.add_RPM:
                input_args.extend(["-a", rpm])

            if GlobalSettings.target:
                commit_version = GlobalSettings.target
            else:
                commit_version = "anaconda-" + version + "-1"

            cmd.append("-t")
            cmd.append(commit_version)
            cmd.extend(input_args)

        return cmd

class Executor(object):
    def __init__(self, branch):
        super().__init__()
        self._branch_obj = branch

    def prepare(self):
        try:
            os.makedirs(os.path.join(GlobalSettings.projects_path, GlobalSettings.anaconda_path, "updates/run/install/updates"))
        except os.error as e:
            print("Updates directory exists already")

        if GlobalSettings.AddonDir:
            addon_img_path=os.path.join(GlobalSettings.projects_path, GlobalSettings.anaconda_path, "updates/usr/share/anaconda/addons/")
            try:
                os.makedirs(addon_img_path)
            except os.error as e:
                print("Can't create addon directory!")
            try:
                print("Copy addon", GlobalSettings.AddonDir)
                shutil.rmtree(addon_img_path)
                dst=os.path.join(addon_img_path, os.path.split(GlobalSettings.AddonDir)[1])
                shutil.copytree(GlobalSettings.AddonDir, dst)
            except FileExistsError as e:
                print("Can't copy addon")

        if GlobalSettings.use_blivet:
            print("Copy blivet...")
            source = os.path.join(GlobalSettings.projects_path, "blivet/blivet")
            dest = os.path.join(GlobalSettings.projects_path, GlobalSettings.anaconda_path, "updates/run/install/updates/blivet")
            try:
                shutil.copytree(source, dest)
            except FileExistsError as e:
                print("Skipping blivet copy:", str(e))

        if GlobalSettings.use_pykickstart:
            print("Copy pykickstart...")
            source = os.path.join(GlobalSettings.projects_path, "pykickstart/pykickstart")
            dest = os.path.join(GlobalSettings.projects_path, GlobalSettings.anaconda_path, "updates/run/install/updates/pykickstart")
            try:
                shutil.copytree(source, dest)
            except FileExistsError as e:
                print("Skipping pykickstart copy:", str(e))

    def create_updates_img(self, command):
        os.chdir(os.path.join(GlobalSettings.projects_path, GlobalSettings.anaconda_path))
        print("Calling command:", command)

        popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = popen.communicate()
        if popen.returncode != 0:
            print("Error calling makeupdates script")
            print(out.decode())
            sys.exit(1)
        else:
            print(out.decode())

    def upload_image(self):
        src = os.path.join(GlobalSettings.projects_path, GlobalSettings.anaconda_path, "updates.img")
        dst_local = os.path.join("../images/", self._branch_obj.img_name)
        dst_srv = os.path.join(GlobalSettings.PXE_server + ":" + GlobalSettings.server_path,
                               self._branch_obj.img_name)

        print("Uploading image to server")
        out = subprocess.check_output(["scp", src, dst_srv], stderr=subprocess.STDOUT).decode()
        print(out)
        shutil.move(src, dst_local)
        print("Creating backup", dst_local)

if __name__ == "__main__":
    try:
        GlobalSettings.readConfiguration()
    except FileNotFoundError as e:
        msg = "Can't open configuration file {}".format(GlobalSettings.CONFIG_PATH)
        print(msg, file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        msg = "Can't read configuration {} from {}".format(e, GlobalSettings.CONFIG_PATH)
        print(msg, file=sys.stderr)
        sys.exit(2)
    except DirectoryNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(3)

    # parse input arguments
    parser = ParseArgs()
    branch = None
    instances = []

    # setup arg parse
    for cls in GeneralBranch.__subclasses__():
        #cls.add_argument(parser)
        inst = cls()
        inst.add_argument(parser)
        instances.append(inst)

    nm = parser.parse_args()

    for branch_inst in instances:
        if branch_inst.type == nm.branch:
            branch = branch_inst
            break

    create_cmd = CreateCommand(branch)
    cmd = create_cmd.create_command(keep=nm.keep, compile=nm.compile)

    executor = Executor(branch)
    executor.prepare()
    executor.create_updates_img(cmd)
    executor.upload_image()
