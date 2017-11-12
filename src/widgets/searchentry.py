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

from gi.repository import Gtk, GLib
import gettext

_ = gettext.gettext


class Entry(Gtk.ToolItem):
    def __init__(self):
        super(Entry, self).__init__()
        self.search_function = None
        self.search_entry = Gtk.Entry()
        self.search_entry.set_width_chars(30)
        self.search_entry.set_placeholder_text(_("Search a package..."))
        self.search_entry.set_icon_from_stock(0, Gtk.STOCK_FIND)
        self.search_entry.set_icon_activatable(0, True)
        self.search_string = _("Search a package...")
        self.add(self.search_entry)
        self.search_entry.connect("key-release-event", self.on_inserting_text)
        self.search_entry.connect("icon-press", self.on_press_icon)
        self.timeout_id = 0

    def clean_text(self):
        '''Clean the text in the entry'''
        self.search_entry.set_placeholder_text(self.search_string)

    def emit_search(self):
        self.search_function(self.search_entry.get_text(), 20)
        return False

    def set_searching_text(self, string):
        '''Set the default search string'''
        self.search_entry.set_text(string)

    def on_inserting_text(self, widget, event):
        if widget.get_text() != "":
            widget.set_icon_from_stock(1, Gtk.STOCK_CLEAR)
        else:
            widget.set_icon_from_stock(1, None)
        if self.timeout_id != 0:
            GLib.source_remove(self.timeout_id)
        self.timeout_id = GLib.timeout_add(300, self.emit_search)

    def on_press_icon(self, widget, position, event):
        '''Handle the press-icon event'''
        if position == 1:
            widget.set_text("")
            widget.set_icon_from_stock(1, None)
            self.search_function("", 0)
            #print("research")
