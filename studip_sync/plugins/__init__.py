import os

from studip_sync.constants import CONFIG_FILENAME
from studip_sync.helpers import JSONConfig
from studip_sync.plugins.plugin_loader import PluginLoader


class PluginConfigError(Exception):
    pass


class PluginList(list):

    def __init__(self, plugins=[], config_path=""):
        super(PluginList, self).__init__()

        for plugin_name in plugins:
            plugin = PluginLoader.load_plugin(plugin_name, config_path)

            self.append(plugin)

    def hook(self, hook_name, *args, **kwargs):
        for plugin in self:
            getattr(plugin, hook_name)(*args, **kwargs)


class PluginBase(object):

    def __init__(self, plugin_name, config_path, config_class):
        super(PluginBase, self).__init__()
        self.plugin_name = plugin_name
        self.config_dir = os.path.join(config_path, plugin_name)
        self.config_filename = os.path.join(self.config_dir, CONFIG_FILENAME)
        self.config_class = config_class

    def hook_configure(self):
        os.makedirs(self.config_dir, exist_ok=True)

    def save_plugin_config(self, config):
        JSONConfig.save_config(self.config_filename, config)

    def hook_start(self):
        if not os.path.exists(self.config_dir):
            raise PluginConfigError(self.plugin_name + ": config file is missing at " + self.config_dir)

        self.config = self.config_class(self.config_filename)

    def hook_media_download_successful(self, filename, course_save_as):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
