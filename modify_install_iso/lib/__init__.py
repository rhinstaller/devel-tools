#
# Functions shared between the tools here.
#
import subprocess

from tempfile import TemporaryDirectory
from contextlib import contextmanager


def subprocess_call(command, env=None, verbose=False):
    """Do a subprocess call of some tool from the system.

    If the call wasn't succeeded raise an exception.

    :param [str] command: list of [command, arg1, arg2,...] to be executed
    :param {string: string} env: add environment variable for the call
    :param bool verbose: should the call print verbose information
    """
    try:
        if verbose:
            print("------------------------")
            print("Running:\n'{}'".format(" ".join(command)))

            subprocess.run(command, env=env, check=True)

            print("------------------------")
        else:
            subprocess.run(command, env=env, capture_output=True, check=True)
    except subprocess.CalledProcessError as ex:
        print(f"System call failed with return code {ex.returncode}")
        if ex.output:
            print(f"Captured output:\n{ex.output.decode('utf-8')}")
            print("----------------------------")
        if ex.stderr:
            print(f"Captured stderr:\n{ex.stderr.decode('utf-8')}")
            print("----------------------------")
        if ex.stdout:
            print(f"Captured stdout:\n{ex.stdout.decode('utf-8')}")
            print("----------------------------")

        raise ex


@contextmanager
def mount_iso(image):
    """Mount an image to temp directory.

    We do not need root privileges for this call because it's done by guestmount tool.

    This function should be used as contextmanager by using `with` keyword.

    :param str image: path to the image to be mounted
    """
    with TemporaryDirectory(prefix='create-dvd-iso-mount-') as mount_dir:
        # use guestmount to mount the image, which doesn't require root privileges
        # LIBGUESTFS_BACKEND=direct: running qemu directly without libvirt
        env = {'LIBGUESTFS_BACKEND': 'direct'}
        cmd = ["guestmount", "-a", image, "-m", "/dev/sda", "--ro", mount_dir]
        subprocess_call(cmd, env=env)

        try:
            yield mount_dir
        finally:
            subprocess_call(['fusermount', '-u', mount_dir])


def create_custom_dvd(source_iso, output_iso, graft_dir, verbose=False):
    """Call pungi-patch-iso tool to modify source iso and add graft dir content.

    :param str source_iso: source for modification
    :param str output_iso: output modified iso
    :param str graft_dir: path to the directory with content we want to modify
    :param bool verbose: should the call to pungi be verbose to people
    """
    cmd = ["pungi-patch-iso", output_iso, source_iso, graft_dir]

    subprocess_call(cmd, verbose=verbose)
