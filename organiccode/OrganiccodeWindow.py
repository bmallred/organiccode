# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import logging
from subprocess import call
from locale import gettext as _
from gi.repository import Gtk  # pylint: disable=E0611
from organiccode_lib import Window
from organiccode.AboutOrganiccodeDialog import AboutOrganiccodeDialog
from organiccode.PreferencesOrganiccodeDialog import PreferencesOrganiccodeDialog

logger = logging.getLogger('organiccode')


class OrganiccodeWindow(Window):
    # See organiccode_lib.Window.py for more details about how this class works
    __gtype_name__ = "OrganiccodeWindow"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the main window"""
        super(OrganiccodeWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutOrganiccodeDialog
        self.PreferencesDialog = PreferencesOrganiccodeDialog

        # Code for other initialization actions should be added here.
        self.openMenu = self.builder.get_object("mnu_open")
        self.projectFolder = self.builder.get_object("projectFolder")
        self.generateButton = self.builder.get_object("generateButton")
        self.fullScreen = self.builder.get_object("fullScreen")
        self.multiSampling = self.builder.get_object("multiSampling")
        self.noVsync = self.builder.get_object("noVsync")
        self.height = self.builder.get_object("height")
        self.width = self.builder.get_object("width")
        self.startPosition = self.builder.get_object("startPosition")
        self.stopPosition = self.builder.get_object("stopPosition")
        self.startScale = self.builder.get_object("startScale")
        self.stopScale = self.builder.get_object("stopScale")
        self.loop = self.builder.get_object("loop")
        self.status = self.builder.get_object("status")

    def on_openMenu_clicked(self, widget):
        self.projectFolder.click()

    def on_generateButton_clicked(self, widget):
        self.status.set_label("Building parameters...")

        args = []
        args.append("gource")

        # Retrieve, or formulate, the options.
        if (self.fullScreen.get_active()):
            args.append("--fullscreen")
        else:
            args.append("-{:.0f}x{:.0f}".format(self.width.get_value(), self.height.get_value()))

        if (self.multiSampling.get_active()):
            args.append("--multi-sampling")

        if (self.noVsync.get_active()):
            args.append("--no-vsync")

        if (self.startPosition.get_active()):
            args.append("--start-position")
            args.append("{:.1f}".format(self.startScale.get_value()))

        if (self.stopPosition.get_active()):
            args.append("--stop-position")
            args.append("{:.1f}".format(self.stopScale.get_value()))

        if (self.loop.get_active()):
            args.append("--loop")

        # Append the path of the project
        args.append(self.projectFolder.get_current_folder())

        # Execute the shell command
        try:
            self.status.set_label("Rendering source control visualization...")
            retvalue = call(args)

            if (retvalue < 0):
                self.status.set_label("Rendering cancelled by user")
            else:
                self.status.set_label("Rendering complete")
        except Exception:
            self.status.set_label("Rendering failed")

    def on_fullScreen_toggled(self, widget):
        isActive = widget.get_active()
        self.height.set_sensitive(not isActive)
        self.width.set_sensitive(not isActive)

    def on_startPosition_toggled(self, widget):
        isActive = widget.get_active()
        self.startScale.set_sensitive(isActive)

    def on_stopPosition_toggled(self, widget):
        isActive = widget.get_active()
        self.stopScale.set_sensitive(isActive)

    def on_loop_toggled(self, widget):
        isActive = widget.get_active()

        if (isActive):
            self.startPosition.set_active(not isActive)
            self.stopPosition.set_active(not isActive)
