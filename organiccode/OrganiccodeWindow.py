# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Bryan M. Allred <bryan.allred@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
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

        self.toolbar = self.builder.get_object("toolbar")
        self.generateButton = self.builder.get_object("generateButton")
        self.exitButton = self.builder.get_object("exitButton")
        self.aboutButton = self.builder.get_object("aboutButton")
        self.mnu_about = self.builder.get_object("mnu_about")

        self.key = self.builder.get_object("key")
        self.highlightUsers = self.builder.get_object("highlightUsers")
        self.highlightDirs = self.builder.get_object("highlightDirs")
        self.transparent = self.builder.get_object("transparent")

        self.hideBloom = self.builder.get_object("hideBloom")
        self.hideDate = self.builder.get_object("hideDate")
        self.hideDirnames = self.builder.get_object("hideDirnames")
        self.hideFiles = self.builder.get_object("hideFiles")
        self.hideFilenames = self.builder.get_object("hideFilenames")
        self.hideMouse = self.builder.get_object("hideMouse")
        self.hideProgress = self.builder.get_object("hideProgress")
        self.hideRoot = self.builder.get_object("hideRoot")
        self.hideTree = self.builder.get_object("hideTree")
        self.hideUsers = self.builder.get_object("hideUsers")
        self.hideUsernames = self.builder.get_object("hideUsernames")

        # Style the toolbar.
        context = self.toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

    def on_openMenu_clicked(self, widget):
        self.projectFolder.click()

    def on_exitButton_clicked(self, widget):
        exit()

    def on_aboutButton_clicked(self, widget):
        self.mnu_about.activate()

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

        if (self.key.get_active()):
            args.append("--key")

        if (self.highlightUsers.get_active()):
            args.append("--highlight-users")

        if (self.highlightDirs.get_active()):
            args.append("--highlight-dirs")

        if (self.transparent.get_active()):
            args.append("--transparent")

        hiddenElements = self.getHiddenElements()
        if (len(hiddenElements) > 0):
            args.append("--hide")
            args.append(hiddenElements)

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

    def getHiddenElements(self):
        elements = []

        if (self.hideBloom.get_active()):
            elements.append("bloom")

        if (self.hideDate.get_active()):
            elements.append("date")

        if (self.hideDirnames.get_active()):
            elements.append("dirnames")

        if (self.hideFiles.get_active()):
            elements.append("files")

        if (self.hideFilenames.get_active()):
            elements.append("filenames")

        if (self.hideMouse.get_active()):
            elements.append("mouse")

        if (self.hideProgress.get_active()):
            elements.append("progress")

        if (self.hideRoot.get_active()):
            elements.append("root")

        if (self.hideTree.get_active()):
            elements.append("tree")

        if (self.hideUsers.get_active()):
            elements.append("users")

        if (self.hideUsernames.get_active()):
            elements.append("usernames")

        return ",".join(elements)
