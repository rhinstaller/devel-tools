#!/usr/bin/python3

import subprocess
import os
import sys
import shutil

from argparse import ArgumentParser

from anaconda_updates.releases import *
from anaconda_updates.settings import GlobalSettings


## Exceptions ##
class DirectoryNotFoundError(Exception):
    pass


## Logic code ##
class ParseArgs(ArgumentParser):
    def __init__(self):
        super().__init__()

        self._branch_group = self.add_mutually_exclusive_group(required=True)
        self.add_argument("-d", dest="directory", action="store",
                          help="use the specified path to the anaconda folder")
        self.add_argument("-a", dest="alternative_dir", action="store_true",
                          help="use alternative anaconda-2 folder")
        self.add_argument("-p", dest="push_only", action="store_true",
                          help=("create image from existing contents in the update folder."
                                "Must be used with some branch target."))
        self.add_argument("-k", "--keep", dest="keep", action="store_true",
                          help="keep content of folder after image creation")
        self.add_argument("-c", "--compile", dest="compile", action="store_true",
                          help="compile anaconda before push")
        self.add_argument("-t", "--target", dest="target_version", nargs=1, action="store",
                          metavar="version",
                          help=("set target version from command line. Use in git format"
                                "If not set, use branch specific."))
        self.add_argument("-n", "--name", dest="image_name", action="store",
                          help=("set the name of the image"))
        self.add_argument("--blivet", dest="use_blivet", action="store_true",
                          help=("copy blivet to updates image."))
        self.add_argument("--pykickstart", dest="use_pykickstart", action="store_true",
                          help=("copy pykickstart to updates image."))
        self.add_argument("--simpleline", dest="use_simpleline", action="store_true",
                          help=("copy simpleline to updates image."))
        self.add_argument("--dasbus", dest="use_dasbus", action="store_true",
                          help=("copy dasbus to updates image."))
        self.add_argument("--add-addon", dest="add_addon", nargs=1, action="append",
                          default=[], metavar="path",
                          help=("add addon to the updates image structure. "
                                "Can be combined with -p to only update addon."))
        self.add_argument("--add-rpm", dest="add_rpm", nargs='+', action="store",
                          metavar="paths",
                          help=("add RPM packages to updates image. "
                                "You can use blob in later make_updates"))
        self.add_argument("--add-image", dest="add_image", nargs=1, action="append",
                          default=[], metavar="images",
                          help=("add contents of another image to the updates image. "
                                "Can be used to upload addons etc."))

    def add_branch_param(self, *args, const_val, help):
        self._branch_group.add_argument(*args, dest="branch",
                                        action="store_const", const=const_val,
                                        help=help)

    def parse_args(self, **kwargs):
        self.nm = super().parse_args()

        if self.nm.push_only:
            GlobalSettings.push_only = True
        if self.nm.alternative_dir:
            GlobalSettings.anaconda_path = os.path.join(
                GlobalSettings.projects_path, "anaconda-2"
            )
        if self.nm.directory:
            GlobalSettings.anaconda_path = self.nm.directory
        for addon in self.nm.add_addon:
            expanded = os.path.expanduser(addon[0])
            GlobalSettings.add_addon.append(os.path.normpath(expanded))
        for image in self.nm.add_image:
            expanded = os.path.expanduser(image[0])
            GlobalSettings.add_image.append(os.path.normpath(expanded))
        if self.nm.add_rpm:
            GlobalSettings.add_RPM.extend(self.nm.add_rpm)
        if self.nm.target_version:
            GlobalSettings.target = self.nm.target_version[0]
        if self.nm.use_blivet:
            GlobalSettings.use_blivet = True
        if self.nm.use_pykickstart:
            GlobalSettings.use_pykickstart = True
        if self.nm.use_simpleline:
            GlobalSettings.use_simpleline = True
        if self.nm.use_dasbus:
            GlobalSettings.use_dasbus = True
        if self.nm.image_name:
            GlobalSettings.image_name = self.nm.image_name

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
            input_args = self._branch_obj.input_args

            if compile:
                cmd.append("-c")

            if GlobalSettings.use_blivet:
                input_args.extend(self._branch_obj.blivet_args)
            if GlobalSettings.use_pykickstart:
                input_args.extend(self._branch_obj.pykickstart_args)
            if GlobalSettings.use_simpleline:
                input_args.extend(self._branch_obj.simpleline_args)
            if GlobalSettings.use_dasbus:
                input_args.extend(self._branch_obj.dasbus_args)

            for rpm in GlobalSettings.add_RPM:
                input_args.extend(["-a", rpm])

            if GlobalSettings.target:
                commit_version = GlobalSettings.target
            else:
                version = self._branch_obj.version
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
            os.makedirs(os.path.join(
                GlobalSettings.anaconda_path,
                "updates/run/install/updates"
            ))
        except os.error as e:
            print("Updates directory exists already")

        image_img_path = os.path.join(
            GlobalSettings.anaconda_path,
            "updates"
        )

        if GlobalSettings.add_image:
            try:
                os.makedirs(image_img_path)
            except os.error as e:
                print("Can't create image directory!")

        for image in GlobalSettings.add_image:
            print("Add image", image)
            cmd = "gunzip < {} | cpio --quiet -iduD {}".format(image, image_img_path)
            proc = subprocess.run(cmd, shell=True)
            if proc.returncode != 0:
                print("Can't unpack the image")

        addon_img_path = os.path.join(
            GlobalSettings.anaconda_path,
            "updates/usr/share/anaconda/addons/"
        )

        if GlobalSettings.add_addon:
            try:
                os.makedirs(addon_img_path)
            except os.error as e:
                print("Can't create addon directory!")

        for addon in GlobalSettings.add_addon:
            try:
                print("Copy addon", addon)
                shutil.rmtree(addon_img_path)
                dst=os.path.join(addon_img_path, os.path.split(addon)[1])
                shutil.copytree(addon, dst)
            except FileExistsError as e:
                print("Can't copy addon")

        if GlobalSettings.use_blivet:
            print("Copy blivet...")
            source = os.path.join(GlobalSettings.projects_path, "blivet/blivet")
            dest = os.path.join(GlobalSettings.anaconda_path, "updates/run/install/updates/blivet")
            try:
                shutil.copytree(source, dest)
            except FileExistsError as e:
                print("Skipping blivet copy:", str(e))

        if GlobalSettings.use_pykickstart:
            print("Copy pykickstart...")
            source = os.path.join(GlobalSettings.projects_path, "pykickstart/pykickstart")
            dest = os.path.join(GlobalSettings.anaconda_path, "updates/run/install/updates/pykickstart")
            try:
                shutil.copytree(source, dest)
            except FileExistsError as e:
                print("Skipping pykickstart copy:", str(e))

        if GlobalSettings.use_simpleline:
            print("Copy simpleline...")
            source = os.path.join(GlobalSettings.projects_path, "simpleline/simpleline")
            dest = os.path.join(GlobalSettings.anaconda_path, "updates/run/install/updates/simpleline")
            try:
                shutil.copytree(source, dest)
            except FileExistsError as e:
                print("Skipping dasbus copy:", str(e))

        if GlobalSettings.use_dasbus:
            print("Copy dasbus...")
            source = os.path.join(GlobalSettings.projects_path, "dasbus/dasbus")
            dest = os.path.join(GlobalSettings.anaconda_path, "updates/run/install/updates/dasbus")
            try:
                shutil.copytree(source, dest)
            except FileExistsError as e:
                print("Skipping simpleline copy:", str(e))

    def create_updates_img(self, command):
        os.chdir(GlobalSettings.anaconda_path)
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
        img_name = GlobalSettings.image_name if GlobalSettings.image_name is not None else self._branch_obj.img_name
        src = os.path.join(GlobalSettings.anaconda_path, "updates.img")
        dst_local = os.path.join(GlobalSettings.local_path, img_name)

        if GlobalSettings.server:
            dst_srv = os.path.join(GlobalSettings.server + ":" + GlobalSettings.server_path, img_name)
            print("Uploading image to server")
            out = subprocess.check_output(["scp", src, dst_srv], stderr=subprocess.STDOUT).decode()
            print(out)

        shutil.move(src, dst_local)
        print("Creating backup", dst_local)


if __name__ == "__main__":
    try:
        GlobalSettings.read_configuration()
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
        inst = cls()
        inst.add_argument(parser)
        instances.append(inst)

    nm = parser.parse_args()

    if not os.path.isdir(GlobalSettings.projects_path):
        raise DirectoryNotFoundError(
            "Can't find directory {}".format(GlobalSettings.projects_path)
        )

    if not os.path.isdir(os.path.join(GlobalSettings.anaconda_path)):
        raise DirectoryNotFoundError(
            "Can't find directory {}".format(GlobalSettings.anaconda_path)
        )

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
