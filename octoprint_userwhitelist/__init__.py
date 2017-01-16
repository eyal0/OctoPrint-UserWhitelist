# coding=utf-8
from __future__ import absolute_import

import re

import octoprint.plugin
import os.path

class UserWhitelistPlugin(octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.TemplatePlugin,
                          octoprint.plugin.StartupPlugin):
  def _whitelisting_add_file(self, destination, path, file_object,
                            links=None, allow_overwrite=False, printer_profile=None, analysis=None):
    usernames = self._settings.get(["usernames"])
    if not isinstance(usernames, str):
      return self._old_add_file(destination, path, file_object, links, allow_overwrite, printer_profile, analysis)
    username_list = re.split("[^a-zA-Z0-9]+", usernames)
    m = re.search("^[^a-zA-Z0-9]*([a-zA-Z0-9]+)[^a-zA-Z0-9]", os.path.splitext(file_object.filename)[0])
    if m and m.group(1) in username_list:
      return self._old_add_file(destination, path, file_object, links, allow_overwrite, printer_profile, analysis)
    if m:
      file_object.filename += (
        r''' because "''' +
        m.group(1) +
        r'''" is not on the username whitelist.  ''' +
        r'''<script type="text/javascript">alert("Whitelist failed, add \"''' +
        m.group(1) +
        r'''\" to Settings->User Whitelist");</script>Add "''' +
        m.group(1) +
        r'''" to Settings->User Whitelist''')
      raise octoprint.filemanager.storage.StorageError(
        "Invalid username, failed whitelist",
        code=octoprint.filemanager.storage.StorageError.UNKNOWN)

    file_object.filename += (
      r''' because it doesn't start with a whitelisted username followed by an underscore.  ''' +
      r'''<script type="text/javascript">alert("Whitelist failed, rename your file to \"YOURUSERNAME_''' +
      file_object.filename +
      r'''\"");</script>Rename your file to "YOURUSERNAME_''' +
      file_object.filename)
    raise octoprint.filemanager.storage.StorageError(
      "Invalid username, failed whitelist",
      code=octoprint.filemanager.storage.StorageError.UNKNOWN)

  def on_after_startup(self):
    self._old_add_file = self._file_manager.add_file
    self._file_manager.add_file = self._whitelisting_add_file

  def get_template_configs(self):
    return [
      dict(type="settings", custom_bindings=False)
    ]
  
  ##~~ SettingsPlugin mixin

  def get_settings_defaults(self):
    return dict(
      usernames=[]
    )

  ##~~ Softwareupdate hook

  def get_update_information(self):
    # Define the configuration for your plugin to use with the Software Update
    # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
    # for details.
    return dict(
      userwhitelist=dict(
        displayName="Userwhitelist Plugin",
        displayVersion=self._plugin_version,

        # version check: github repository
        type="github_release",
        user="eyal0",
        repo="OctoPrint-UserWhitelist",
        current=self._plugin_version,

        # update method: pip
        pip="https://github.com/eyal0/OctoPrint-UserWhitelist/archive/{target_version}.zip"
      )
    )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "User Whitelist"

def __plugin_load__():
        global __plugin_implementation__
	__plugin_implementation__ = UserWhitelistPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
