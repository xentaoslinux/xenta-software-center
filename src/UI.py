#!/usr/bin/python
# -*- coding:UTF-8 -*-
#       Copyright (c)   Dindin Hernawan <root@dev.xentaos.org>
#                       Stephen Smally <stephen.smally@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#

from gi.repository import Gtk
from gi.repository import Gdk
from widgets import toolbar
from widgets import statusbox
from widgets import pages
from widgets import screenshot
import control
import gettext

_ = gettext.gettext

version = "Version %s" % control.version

global license
license = '''Xenta Software Center

Copyright © 2017 Xenta OS
            2011-12 Lubuntu Team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import os
import sys
from . import LOG


class Gui(Gtk.Window):
    def __init__(self, categories_func, categories_dict):
        '''Setting up the UI'''
        super(Gui, self).__init__()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title(_("Xenta Software Center"))
        self.set_icon_name("xenta-software-center")
        self.set_default_size(750, 400)
        self.connect("destroy", self.close_app)
        control.__init__()
        self.cssstyle = """
        GtkViewport#lscviewport {
            background-color: @base_color;
        }
        """
        self.screen = Gdk.Screen.get_default()
        self.providestyle = Gtk.CssProvider()
        self.providestyle.load_from_data(self.cssstyle)
        Gtk.StyleContext.add_provider_for_screen(
            self.screen, self.providestyle, 600)
        self.pages = pages.Pages(categories_func)
        self.sections = [
            ("stock_down", _("Get Software"), "get"),
            ("gtk-harddisk", _("Installed Software"), "inst"),
            ("applications-other", _("Apps Basket"), "basket")
        ]

        if os.environ.get('XDG_CURRENT_DESKTOP') == 'GNOME':
            self.toolbar = toolbar.Headerbar()
            self.set_titlebar(self.toolbar)
        else:
            self.toolbar = toolbar.Toolbar()

        self.pages.sections = self.toolbar.add_sections(
            self.sections, True, self.pages.change_section)
        self.categories_button_dict = self.pages.categories.append_sections(
            categories_dict)
        self.categories_dict = categories_dict
        self.statusbox = statusbox.MainBox()
        self.progressbar = Gtk.ProgressBar()
        self.progressbar_cont = self.progressbar
        self.pkgs_count = self.statusbox.pkgs
        self.categorie_icon = self.statusbox.icon
        self.categorie_label = self.statusbox.sectionlabel
        self.search_pkg = self.toolbar.entry
        self.vbox = Gtk.VBox()
        self.vbox1 = Gtk.VBox()

        if os.environ.get('XDG_CURRENT_DESKTOP') != 'GNOME':
            self.vbox.pack_start(self.toolbar, False, False, 0)
        else:
            self.vbox.pack_start(self.toolbar.searchbar, False, False, 0)
        self.vbox.pack_start(self.vbox1, True, True, 0)
        self.vbox1.pack_start(self.statusbox, False, False, 0)
        self.vbox1.pack_start(self.pages, True, True, 0)
        self.vbox.pack_start(self.progressbar_cont, False, False, 0)
        #-Aliases for main.py-----------------------------
        self.basket_radio = self.toolbar.basket_radio
        self.remove_mai_button = self.pages.basket.remove_button
        self.appsinfo = self.pages.appsinfo
        self.apps_message = self.pages.apps_all.details_box
        self.installed_message = self.pages.apps_installed.details_box
        self.apps_all = self.pages.apps_all.apps
        self.apps_installed = self.pages.apps_installed.apps
        self.apps_basket = self.pages.basket.basketview
        self.no_found_box = self.pages.apps_all.nofound
        self.no_found_button = self.no_found_box.nofound
        self.no_found_labelbox = self.pages.apps_all.nofound2
        self.no_installed_found = self.pages.apps_installed.nofound2
        self.apps_scrolled = self.pages.apps_all.apps_cont
        self.installed_scrolled = self.pages.apps_installed.apps_cont
        self.riepilogue_label = self.pages.basket.riepilogue_label
        self.install_pkgs = self.pages.basket.riepilogue_bar.button
        self.scrot_dialog = screenshot.Dialog
        #-------------------------------------------------
        self.about = Gtk.AboutDialog()
        self.about.set_program_name(_("Xenta Software Center"))
        self.about.set_logo_icon_name("xenta-software-center")
        self.about.set_copyright("Copyright © 2017 Xenta OS")
        self.about.set_authors([
            "Dindin Hernawan <root@dev.xentaos.org> [Packaing]",
            "Julien Lavergne <gilir@ubuntu.com> [Packaging]",
            "Michael Rawson <michaelrawson76@gmail.com> [Code, Bug Fixing]",
            "Stephen Smally <eco.stefi@fastwebnet.it> [Code, Bug Fixing, UI]"])
        self.about.set_comments(_(
            "Light but user-friendly Software Center for Xenta OS"))
        self.about.set_website(
            "http://www.xentaos.com/")
        self.about.set_version(version)
        self.about.set_license(license)
        #-------------------------------------------------
        self.add(self.vbox)
        self.show_all()
        self.toolbar.settings.set_can_focus(True)
        #-------------------------------------------------
        self.toolbar.get_style_context().add_class("primary-toolbar")
        #-Some hides or will look orrible-----------------
        self.progressbar_cont.set_visible(False)
        self.no_found_box.set_visible(False)
        self.no_found_labelbox.set_visible(False)
        self.no_installed_found.set_visible(False)
        self.pages.apps_installed.nofound.set_visible(False)
        self.statusbox.combo.set_visible(False)
        #-------------------------------------------------
        self.statusbox.combo_model.append([_("Show at least 20 results")])
        self.statusbox.combo_model.append([_("Show all results")])

    def close_app(self, widget):
        """ close the app
        """
        if Gtk.main_level() == 0:
            LOG.info("closing before the regular main loop was run")
            sys.exit(0)
        self.destroy()
        try:
            Gtk.main_quit()
        except:
            LOG.exception("Gtk.main_quit failed")
        sys.exit(0)
