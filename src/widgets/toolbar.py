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
import searchentry
class ToolbarBase(object):
    def refresh_back_forward(self, can_home):
        self.back.set_sensitive(can_home)

    def add_sections(self, seclist=[], important=True, func=None):
        sectionslist = {}

        self.box = self.button_box()

        self.group = None
        for (icon, name, action) in seclist:
            choose = Gtk.RadioButton(group=self.group)
            
            choose.set_can_focus(False)
            choose_box = Gtk.HBox()
            choose_box.set_spacing(2)
            choose.label = Gtk.Label()
            choose.label.set_text(name)

            if self.show_choose_icon:
                choose.set_relief(Gtk.ReliefStyle.NONE)
                choose_icon = Gtk.Image()
                choose_icon.set_from_icon_name(icon, Gtk.IconSize.SMALL_TOOLBAR)
                choose_box.pack_start(choose_icon, False, False, 0)
                choose_box.pack_start(choose.label, False, False, 0)
                choose.add(choose_box)
            else:
                choose.add(choose.label)

            choose.connect("toggled", func, self)
            choose.set_property("draw-indicator", False)
            self.box.pack_start(choose, False, False, 0)
            sectionslist[choose] = action
            if action == "basket":
                self.basket_radio = choose
            elif action == "get":
                self.group = choose

        self.build_toolbar()

        return sectionslist

class Toolbar(Gtk.Toolbar, ToolbarBase):
    def __init__(self):
        super(Toolbar, self).__init__()
        self.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)
        self.set_icon_size(Gtk.IconSize.SMALL_TOOLBAR)
        self.show_choose_icon = True

    def add_search(self):
        self.expander = Gtk.ToolItem()
        self.expander.set_expand(True)
        self.entry = searchentry.Entry()
        self.insert(self.expander, -1)
        self.insert(self.entry, -1)

    def add_settings(self):
        self.settings = Gtk.ToolButton()
        self.settings.set_stock_id(Gtk.STOCK_PREFERENCES)
        self.insert(self.settings, -1)

    def back_forwards(self):
        self.back = Gtk.ToolButton()
        self.back.set_stock_id(Gtk.STOCK_GO_BACK)
        self.back.set_is_important(False)
        self.back.set_sensitive(False)
        self.insert(self.back, -1)

    def button_box(self):
        box = Gtk.HBox()
        box.set_spacing(5)
        return box

    def build_toolbar(self):
        self.back_forwards()
        self.vbox = Gtk.VBox()
        self.vbox.pack_start(self.box, True, False, 0)
        self.box_tool = Gtk.ToolItem()
        self.box_tool.add(self.vbox)
        self.insert(self.box_tool, -1)
        self.add_search()
        self.add_settings()

class Headerbar(Gtk.HeaderBar, ToolbarBase):
    def __init__(self):
        super(Headerbar, self).__init__()
        self.set_show_close_button(True)
        self.show_choose_icon = False

    def insert(self, item, index):
        if index == -1:
            self.pack_start(item)

    def add_search(self):
        self.entry = searchentry.Entry()

        self.searchbar = Gtk.SearchBar()
        self.searchbar.add(self.entry)
        self.searchbar.props.hexpand = False

        icon = Gtk.Image()
        icon.set_from_icon_name("edit-find-symbolic",Gtk.IconSize.MENU)
        self.search = Gtk.ToggleButton()
        self.search.add(icon)
        self.search.connect("toggled", self._on_find_toggled)
        self.pack_end(self.search)

    def _on_find_toggled(self, btn):
        if self.searchbar.get_search_mode():
            self.searchbar.set_search_mode(False)
        else:
            self.searchbar.set_search_mode(True)
            self.entry.grab_focus()

    def add_settings(self):
        self.settings = Gtk.Button()
        icon = Gtk.Image()
        icon.set_from_icon_name("open-menu-symbolic",Gtk.IconSize.MENU)
        self.settings.add(icon)
        self.pack_end(self.settings)

    def back_forwards(self):
        self.back = Gtk.Button()
        self.back.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.back.set_sensitive(False)
        self.insert(self.back, -1)

    def button_box(self):
        box = Gtk.ButtonBox()
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        return box

    def build_toolbar(self):
        self.back_forwards()
        self.pack_start(self.box)       
        self.add_settings()
        self.add_search()



