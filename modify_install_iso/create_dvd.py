#!/usr/bin/python3
#
# This tool will add additional repository to an existing DVD to create
# an unified dvd for testing purposes.
#

import os
import shutil

from argparse import ArgumentParser
from tempfile import mkdtemp
from contextlib import contextmanager
from productmd.treeinfo import TreeInfo, Variant
from rpmfluff import SimpleRpmBuild, SourceFile

from lib import mount_iso, subprocess_call, create_custom_dvd


FEDORA_REPO_NAME = "Fedora"
ARCH = "x86_64"

TREE_INFO_FILE_NAME = ".treeinfo"
CUSTOM_REPO_NAME = "Custom"
PACKAGES_DIR = "Packages"

VERBOSE = False


def obtain_existing_treeinfo_content(iso):
    with mount_iso(iso) as mount_dir:
        tree_info_path = os.path.join(mount_dir, ".treeinfo")
        if not os.path.exists(tree_info_path):
            raise RuntimeError("Can't find .treeinfo file on the source DVD ISO")

        with open(tree_info_path, "rt") as fd:
            return fd.read()


def append_custom_repo_to_treeinfo(treeinfo_content, path):
    ti = TreeInfo()
    ti.loads(treeinfo_content)

    variant = Variant(ti)

    variant.id = CUSTOM_REPO_NAME
    variant.uid = CUSTOM_REPO_NAME
    variant.name = CUSTOM_REPO_NAME
    variant.paths.repository = os.path.join(".", CUSTOM_REPO_NAME)
    variant.paths.packages = os.path.join(".", CUSTOM_REPO_NAME, PACKAGES_DIR)
    variant.type = "variant"

    ti.variants.add(variant)

    ti.dump(path)


def create_custom_repo(temp_dir):
    rpm_file = _create_fake_rpm(temp_dir)
    repo_dir = os.path.join(temp_dir, CUSTOM_REPO_NAME)
    packages_dir = os.path.join(repo_dir, PACKAGES_DIR)

    os.mkdir(repo_dir)
    os.makedirs(packages_dir)
    shutil.copy2(rpm_file, packages_dir)

    _create_repo(repo_dir)

    return repo_dir


def _create_fake_rpm(temp_dir):
    rpm = SimpleRpmBuild(name="test-rpm", version="200", release="9000")
    rpm.add_installed_file(installPath="/usr/bin/TEST",
                           sourceFile=SourceFile(sourceName="TEST",
                                                 content="SO AWESOME APP!")
                           )
    with switch_workdir(temp_dir):
        rpm.make()

    rpm_rel_path = rpm.get_built_rpm(ARCH)
    return os.path.join(temp_dir, rpm_rel_path)


def _create_repo(repo_dir):
    subprocess_call(["createrepo_c", repo_dir], verbose=VERBOSE)


@contextmanager
def switch_workdir(dir):
    """This is a context manager to temporary switch the current directory.

    This function should be used with `with` keyword.
    """
    old_cwd = os.getcwd()
    os.chdir(dir)
    yield
    os.chdir(old_cwd)


def create_temp_dir():
    return mkdtemp(prefix="dvd_iso-")


def remove_temp_dir(temp_dir):
    shutil.rmtree(temp_dir)


def parse_args():
    parser = ArgumentParser(description="Tool to create testing DVD with multiple repositories.")

    parser.add_argument("source_iso", metavar="SOURCE_ISO",
                        help="""existing source ISO file which already contains repository
                        (e.g. Fedora-Server-DVD.iso)""")
    parser.add_argument("output_iso", metavar="OUTPUT_ISO",
                        help="""path to the output ISO file""")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                        help="""enable verbose output""")

    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_args()
    if opt.verbose:
        VERBOSE = True

    temp_dir = create_temp_dir()

    tree_info_path = os.path.join(temp_dir, TREE_INFO_FILE_NAME)
    orig_tree_info_content = obtain_existing_treeinfo_content(opt.source_iso)
    append_custom_repo_to_treeinfo(orig_tree_info_content, tree_info_path)
    create_custom_repo(temp_dir)
    create_custom_dvd(opt.source_iso, temp_dir, opt.output_iso, verbose=VERBOSE)

    # clean-up
    remove_temp_dir(temp_dir)
