
import os
import configparser

from update_image import DirectoryNotFoundError


class GlobalSettings(object):
    # Path to configuration file
    CONFIG_PATH = "~/.config/anaconda-updates/updates.cfg"

    #######################
    # Global configuration
    projects_path = ""    # Directory where anaconda blivet and pykickstart are
    anaconda_path = ""    # Name of the directory with anaconda source codes
    PXE_server = ""       # Server with PXE which you are using to test anaconda
    server_path = ""      # Server path for saving updates image
    show_version_script_path = ""

    #######################
    # Run specific configuration

    # target anaconda version
    # None means use branch specific
    target = None
    AddonDir = ""
    image_name = None

    add_RPM = []

    auto_fetch = True
    push_only = False

    use_blivet = False
    use_pykickstart = False
    use_simpleline = False

    @classmethod
    def read_configuration(cls):
        config = configparser.ConfigParser()
        with open(os.path.expanduser(cls.CONFIG_PATH)) as f_cfg:
            config.read_file(f_cfg)
            global_settings = config["GlobalSettings"]
            cls.projects_path = global_settings["ProjectsPath"] # must be specified in config file
            cls.show_version_script_path = global_settings["ShowVersionScriptPath"]
            cls.anaconda_path = global_settings.get("anaconda_pathName", "anaconda")

            cls.PXE_server = global_settings["Server"]
            cls.server_path = global_settings["ServerPath"]

            if not os.path.isdir(cls.projects_path):
                raise DirectoryNotFoundError("Can't find directory {}".format(cls.projects_path))
            if not os.path.isdir(os.path.join(cls.projects_path, cls.anaconda_path)):
                raise DirectoryNotFoundError("Can't find directory {}".format(
                        os.path.join(cls.projects_path, cls.anaconda_path)))
