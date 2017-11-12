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


class MainBox(Gtk.VBox):
    def __init__(self):
        super(MainBox, self).__init__()
        self.hbox = Gtk.HBox()
        self.hbox.set_border_width(5)
        self.hbox.set_spacing(5)
        self.icon = Gtk.Image()
        self.sectionlabel = Gtk.Label()
        self.pkgs = Gtk.Label()
        self.combo_model = Gtk.ListStore(str)
        self.cell = Gtk.CellRendererText()
        self.combo = Gtk.ComboBox.new_with_model(self.combo_model)
        self.combo.pack_start(self.cell, False)
        self.combo.add_attribute(self.cell, "text", 0)
        self.installed = Gtk.Image()
        self.separator = Gtk.HSeparator()
        self.hbox.pack_start(self.icon, False, False, 0)
        self.hbox.pack_start(self.sectionlabel, False, False, 0)
        self.hbox.pack_end(self.combo, False, False, 0)
        self.hbox.pack_end(self.installed, False, False, 0)
        self.pack_start(self.hbox, False, False, 0)
        self.pack_start(self.separator, False, False, 0)
