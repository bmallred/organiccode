# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import logging
from locale import gettext as _
from organiccode_lib.AboutDialog import AboutDialog

logger = logging.getLogger('organiccode')


class AboutOrganiccodeDialog(AboutDialog):
    # See organiccode_lib.AboutDialog.py for more details about how this class works.
    __gtype_name__ = "AboutOrganiccodeDialog"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutOrganiccodeDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.
