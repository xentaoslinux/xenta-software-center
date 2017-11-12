#!/usr/bin/env python
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
import categories
import appsview
import basket
import appsinfo

import gettext
_ = gettext.gettext


class Pages(Gtk.Notebook):
    def __init__(self, func):
        super(Pages, self).__init__()
        self.basket_function = None
        self.last_page = None
        self.get_function = None
        self.installed_function = None
        self.sections = {}
        self.set_show_border(False)
        self.set_show_tabs(False)
        self.apps_all = appsview.MainBox()
        self.apps_installed = appsview.MainBox()
        self.categories = categories.CategoriesView()
        self.basket = basket.BasketBox()
        self.appsinfo = appsinfo.InfoBox()
        self.categories.categories_func = func
        self.append_page(self.categories, None)
        self.append_page(self.apps_all, None)
        self.append_page(self.apps_installed, None)
        self.append_page(self.basket, None)
        self.append_page(self.appsinfo, None)
        self.last_action = "get"

    def change_section(self, widget, toolbar):
        self.action = self.sections[widget]
        #print self.last_action, "=>", self.action
        if not self.last_action == self.action:
            if self.action == "get":
                #print "going to get"
                self.change_page(1)
                self.can_home = True
                self.get_function()
            elif self.action == "inst":
                self.change_page(2, False)
                self.can_home = False
                self.installed_function()
            elif self.action == "basket":
                self.change_page(3, False)
                self.can_home = False
                self.basket_function()
            self.last_action = self.action
            toolbar.refresh_back_forward(self.can_home)

    def change_page(self, page=int, last=True):
        self.set_current_page(page)

    def get_page(self):
        return self.get_current_page()

    def back(self, widget, toolbar):
        self.change_page(0)
        self.can_home = False
        toolbar.refresh_back_forward(self.can_home)
