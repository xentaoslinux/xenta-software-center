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
from gi.repository import Pango

import gettext
_ = gettext.gettext


class MainBox(Gtk.VBox):
    def __init__(self):
        super(MainBox, self).__init__()
        self.nofound = NoFoundBox()
        self.nofound2 = Gtk.Label(_("No Packages Found"))
        self.apps_box = Gtk.HBox()
        self.apps_cont = Gtk.ScrolledWindow()
        self.apps_cont.set_shadow_type(Gtk.ShadowType.NONE)
        self.apps_cont.set_policy(Gtk.PolicyType.AUTOMATIC,
                                  Gtk.PolicyType.AUTOMATIC)
        self.apps = AppsView()
        self.apps_cont.add(self.apps)
        self.apps_box.pack_start(self.apps_cont, True, True, 0)
        self.apps_box.pack_start(self.nofound, True, True, 0)
        self.apps_box.pack_start(self.nofound2, True, True, 0)
        self.details = DetailsBox()
        self.details_box = Gtk.VBox()
        self.details_box_second = Gtk.HBox()
        self.details_button = self.details.details_button
        self.label = Gtk.Label()
        self.label.props.xalign = 0
        self.details_box.pack_start(Gtk.HSeparator(), False, False, 0)
        self.details_box.pack_start(self.details_box_second, False, False, 0)
        self.details_box_second.set_border_width(5)
        self.details_box_second.pack_start(self.label, True, True, 0)
        self.details_box_second.pack_end(self.details, False, False, 0)
        self.details_box.details_button = self.details.details_button
        self.details_box.add_remove_button = self.details.add_remove_button
        self.details_box.package_name = self.label
        self.pack_start(self.apps_box, True, True, 0)
        self.pack_start(self.details_box, False, False, 0)


class DetailsBox(Gtk.HBox):
    def __init__(self):
        super(DetailsBox, self).__init__()
        self.set_spacing(5)
        self.details_button = Gtk.Button.new_from_stock(Gtk.STOCK_INFO)
        self.details_button.set_tooltip_text(_("Details on the package"))
        self.add_remove_button = Gtk.Button(label=_("Add/remove"))
        self.pack_start(self.details_button, False, False, 0)
        self.pack_start(self.add_remove_button, False, False, 0)


class AppsView(Gtk.TreeView):
    def __init__(self):
        super(AppsView, self).__init__()
        self.set_headers_visible(False)
        self.set_rules_hint(True)
        self.model = Gtk.ListStore(str, str, str, str)
        self.buffcell = Gtk.CellRendererPixbuf()
        self.buffcell.set_property("stock_size", Gtk.IconSize.DIALOG)
        self.buffcell.set_property("height", 58)
        self.buffcell.set_property("width", 58)
        self.textcell = Gtk.CellRendererText()
        self.textcell.set_property("ellipsize", Pango.EllipsizeMode.END)
        self.statuscell = Gtk.CellRendererPixbuf()
        self.statuscell.set_property("stock_size", Gtk.IconSize.BUTTON)
        self.maincolumn = Gtk.TreeViewColumn()
        self.maincolumn.pack_start(self.buffcell, False)
        self.maincolumn.pack_start(self.textcell, True)
        self.maincolumn.pack_start(self.statuscell, False)
        self.maincolumn.add_attribute(self.buffcell, "icon-name", 1)
        self.maincolumn.add_attribute(self.textcell, "text", 0)
        self.maincolumn.add_attribute(self.statuscell, "stock-id", 3)
        self.append_column(self.maincolumn)


class NoFoundBox(Gtk.HBox):
    def __init__(self):
        super(NoFoundBox, self).__init__()
        self.string1 = Gtk.Label(_("No Packages Found"))
        self.string2 = Gtk.Label(_("Search all categories instead"))
        self.nofound_box = Gtk.VBox()
        self.nofound_box.pack_start(self.string1, False, False, 0)
        self.nofound_box.pack_start(self.string2, False, False, 0)
        self.secondbox = Gtk.VBox()
        self.nofound = Gtk.Button()
        self.nofound.add(self.nofound_box)
        self.secondbox.pack_start(self.nofound, True, False, 0)
        self.pack_start(self.secondbox, True, False, 0)
