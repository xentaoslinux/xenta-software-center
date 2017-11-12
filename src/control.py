#!/usr/bin/python
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

from ConfigParser import RawConfigParser
from gi.repository import Gtk
from . import LOG

import os
import gettext

_ = gettext.gettext


version = "1.3"

default_conf_file = '''
[General]
app_install_directory = /usr/share/app-install/desktop/
expert_mode = FALSE
render_icons = TRUE
show_scrot = TRUE
db_path = /var/cache
categories_file = data/categories
check_internet=FALSE
'''


class Controller:
    def __init__(self):
        LOG.debug("Opening config file")
        self.toolbar_styles = [
            Gtk.ToolbarStyle.ICONS,
            Gtk.ToolbarStyle.TEXT,
            Gtk.ToolbarStyle.BOTH,
            Gtk.ToolbarStyle.BOTH_HORIZ
        ]
        self.home = os.getenv("HOME")
        self.config_dir = "/".join([self.home, ".config/lsc"])
        self.file_path = "/".join([self.config_dir, "LSC.ini"])
        self.default_path = "/".join([self.config_dir, "default_LSC.ini"])
        self.screenshots_path = "/".join([self.config_dir, "screenshots"])
        self.reviews_path = "/".join([self.config_dir, "reviews"])
        self.data_system_path = "/usr/share/LSC/"
        if not os.path.exists(self.file_path):
            LOG.debug("Creating new conf file in %s" % "/".join(
                [self.config_dir, "LSC.ini"]))
            try:
                os.mkdir(self.config_dir)
                os.mkdir(self.screenshots_path)
                os.mkdir(self.reviews_path)
            except OSError:
                pass
            self.clean_conf_file(self.file_path)
        if not os.path.exists(self.screenshots_path):
            os.mkdir(self.screenshots_path)
        if not os.path.exists(self.reviews_path):
            os.mkdir(self.reviews_path)
        self.conf_file = open(self.file_path, "r+w")
        self.default_file = open(self.default_path, "w")
        self.default_file.write(default_conf_file)
        self.default_file.close()
        self.default_file = open(self.default_path, "r")
        self.parser = RawConfigParser()
        self.parser.readfp(self.conf_file)
        self.parser1 = RawConfigParser()
        self.parser1.readfp(self.default_file)
        self.options = []
        self.options1 = []
        for items in self.parser.sections():
            self.options += self.parser.options(items)
        for items in self.parser1.sections():
            self.options1 += self.parser1.options(items)
        if sorted(self.options) != sorted(self.options1):
            LOG.debug("updating config file")
            self.clean_conf_file(self.file_path)
        del self.parser
        self.parser = RawConfigParser()
        self.conf_file = open(self.file_path, "r+w")
        self.parser.readfp(self.conf_file)
        del self.parser1

        if os.path.exists(self.parser.get(
                "General", "app_install_directory")):
            self.app_install_directory = self.parser.get(
                "General", "app_install_directory")
        else:
            LOG.warn(_("Please install the package app-install-data, lubuntu \
                software center will not work in beginner mode without it"))
            self.app_install_directory = None
            self.app_install_directory = None

        self.expert_mode = self.parser.getboolean(
            "General", "expert_mode")

        self.render_icons = self.parser.getboolean(
            "General", "render_icons")

        self.show_scrot = self.parser.getboolean(
            "General", "show_scrot")

        self.check_internet = self.parser.getboolean(
            "General", "check_internet")

        self.db_path = self.parser.get("General", "db_path") + "/"

        '''
        if os.path.isfile(self.parser.get("General", "categories_file")):
            self.categories_file = open(self.parser.get(
                "General", "categories_file"), "r")
        else:
            self.categories_file = open(os.path.join(
                self.data_system_path,"categories"), "r")
        '''

    def clean_conf_file(self, file_path):
        self.conffile = open(file_path, "w")
        self.conffile.write("")
        self.conffile.close()
        self.conffile = open(file_path, "w")
        self.conffile.write(default_conf_file)
        self.conffile.close()

    def append_categories(self, ui, model):
        '''Append the categories to the given model'''
        ### THIS IS NOT OK, WE SHOULD CHECK FOR TABLES IN THE DB,
        ### WHICH CONTAIN THE CATEGORIES - FIX ME!!!
        model.clear()
        ui.categories_dict = {}
        if not self.expert_mode:
            for items in ui.categories_dict:
                if items != "All":
                    model.append([items, ui.categories_dict[items][0],
                                  ui.categories_dict[items][1], 5])
        else:
            for lines in self.categories_file:
                string = lines.rstrip()
                self.string = string.split("||")
                ui.categories_dict[self.string[0]] = [self.string[1],
                                                      self.string[3]]
            for items in ui.categories_dict:
                if items != "All":
                    model.append([items, ui.categories_dict[items][0],
                                  ui.categories_dict[items][1], 5])
        model.append(["All", "distributor-logo", "allpkgs", 5])
        self.categories_file.close()


def __init__():
    '''Initialize the controller'''
    global controller
    controller = Controller()
