# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class UserWhitelistPlugin(octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.TemplatePlugin,
                          octoprint.plugin.StartupPlugin):
  def _whitelisting_add_file(self, destination, path, file_object,
                            links=None, allow_overwrite=False, printer_profile=None, analysis=None):
    print self._settings
    print dir(self._settings.settings)
    file_object.filename += (
      r"""" because it doesn't start with a whitelisted LDAP followed by an underscore.  """ +
      r"""<script type="text/javascript">alert("Whitelist failed, rename your file to \"YOURLDAP_""" +
      file_object.filename +
      r"""\"");</script>Please rename your file to "YOURLDAP_""" +
      file_object.filename)
    raise octoprint.filemanager.storage.StorageError(
      "Invalid LDAP, failed whitelist",
      code=octoprint.filemanager.storage.StorageError.UNKNOWN)

  def on_after_startup(self):
    print self._settings.get()
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
