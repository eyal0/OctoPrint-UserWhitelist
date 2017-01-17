# OctoPrint-UserWhitelist

Require filenames to be prefixed with a user name so that you can tell who started the print job on a shared octoprint.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/eyal0/OctoPrint-UserWhitelist/archive/master.zip

## Configuration

In the Settings, go to User Whitelist and add a list of names to be allowed to print.  For example, if you add: `larry, moe, curly` then only files that start with `larry_` or `moe_` or `curly_` will be allowed on octoprint.  This makes it easy to track who is printing.

## Operation Details

A username must consist of only letters and numbers.  Any separator can be used in the filename or the list of users.  So the whitelist can read `larry,moe,curly` or `larry moe curly` or each on a newline.  It doesn't matter.  The same goes for filenames.  The file can start with `larry_` or `curly.` or `moe-`.
