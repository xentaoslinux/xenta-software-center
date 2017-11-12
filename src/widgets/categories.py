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

import gettext
_ = gettext.gettext


class CategoriesView(Gtk.ScrolledWindow):
    def __init__(self):
        super(CategoriesView, self).__init__()
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.categories_func = None
        self.theme = Gtk.IconTheme.get_default()
        self.secondary_box = Gtk.HBox()
        self.third_box = Gtk.VBox()
        self.third_box.set_homogeneous(True)
        self.third_box.set_spacing(5)
        self.view = Gtk.Viewport()
        self.view.set_name("lscviewport")
        self.add(self.view)
        self.view.add(self.secondary_box)
        self.secondary_box.pack_start(self.third_box, True, False, 0)
        self.boxes = [Gtk.HBox()]
        for items in self.boxes:
            items.set_homogeneous(True)
            items.set_spacing(5)
            self.third_box.pack_start(items, False, False, 0)
        self.x = 0

    def append_sections(self, sections={}):
        button_dict = {}
        for (section, [icon, name, showboth]) in sorted(
                sections.items(), key=lambda i: i[1][1]):
            if len(self.boxes[self.x].get_children()) == 3:
                self.other_box = Gtk.HBox()
                self.other_box.set_homogeneous(True)
                self.other_box.set_spacing(5)
                self.third_box.pack_start(self.other_box, False, False, 0)
                self.boxes.append(self.other_box)
                self.x += 1
            self.secbox = Gtk.HBox()
            if not self.theme.has_icon(icon):
                self.secimage = Gtk.Image.new_from_icon_name(
                    "applications-other", 5)
            else:
                self.secimage = Gtk.Image.new_from_icon_name(icon, 5)
            self.seclabel = Gtk.Label(name)
            self.secbox.pack_start(self.secimage, False, False, 0)
            self.secbox.pack_start(self.seclabel, False, True, 0)
            self.secbox.set_spacing(2)
            self.secbutt = Gtk.Button()
            self.secbutt.set_relief(Gtk.ReliefStyle.NONE)
            self.secbutt.add(self.secbox)
            self.secbutt.set_can_focus(False)
            self.secbutt.connect("clicked", self.categories_func)
            button_dict[self.secbutt] = section
            self.boxes[self.x].pack_start(self.secbutt, True, True, 0)
        for missing in xrange(3 - len(self.boxes[self.x].get_children())):
            # Add an unclickable widget which
            # shows nothing by default as placeholder
            self.boxes[self.x].pack_start(Gtk.Image(), True, True, 0)
        return button_dict
