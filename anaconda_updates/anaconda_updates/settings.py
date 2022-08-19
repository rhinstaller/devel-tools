
import os
import configparser


class GlobalSettings(object):
    # Path to configuration file
    CONFIG_PATH = "~/.config/anaconda-updates/updates.cfg"

    #######################
    # Global configuration
    projects_path = ""    # Directory where anaconda blivet and pykickstart are
    anaconda_path = ""    # Directory with anaconda source codes
    server = None         # Server with PXE which you are using to test anaconda; could be None
    server_path = "~"     # Server path for saving updates image; default '~'
    local_path = "/tmp"   # Local path to the image; default "/tmp"
    show_version_script_path = None

    #######################
    # Run specific configuration

    # target anaconda version
    # None means use branch specific
    target = None
    add_addon = []
    add_image = []
    image_name = None

    add_RPM = []

    push_only = False

    use_blivet = False
    use_pykickstart = False
    use_simpleline = False
    use_dasbus = False
    use_meh = False

    @classmethod
    def read_configuration(cls):
        config = configparser.ConfigParser()
        with open(os.path.expanduser(cls.CONFIG_PATH)) as f_cfg:
            config.read_file(f_cfg)
            global_settings = config["GlobalSettings"]
            cls.projects_path = global_settings["ProjectsPath"] # must be specified in config file
            cls.show_version_script_path = global_settings.get("ShowVersionScriptPath", None)
            cls.anaconda_path = os.path.join(
                cls.projects_path, global_settings.get("anaconda_pathName", "anaconda")
            )
            cls.server = global_settings.get("Server", None)
            cls.server_path = global_settings.get("ServerPath", "~")
            cls.local_path = os.path.expanduser(global_settings.get("LocalPath", "/tmp"))
