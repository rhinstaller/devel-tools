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
    if verbose:
        print("------------------------")
        print("Running:\n'{}'".format(" ".join(command)))

        ret = subprocess.run(command, env=env)

        print("------------------------")
    else:
        ret = subprocess.run(command, env=env, capture_output=True)

    ret.check_returncode()


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
