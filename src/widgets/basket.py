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


class BasketBox(Gtk.VBox):
    def __init__(self):
        super(BasketBox, self).__init__()
        self.basketview_cont = Gtk.ScrolledWindow()
        self.basketview_cont.set_shadow_type(Gtk.ShadowType.NONE)
        self.basketview_cont.set_policy(Gtk.PolicyType.AUTOMATIC,
                                        Gtk.PolicyType.AUTOMATIC)
        self.basketview = PackagesView()
        self.basketview.set_model(self.basketview.model)
        self.basketview_cont.add(self.basketview)
        self.riepilogue_box = Gtk.HBox()
        self.riepilogue_box.set_border_width(5)
        self.riepilogue_label = Gtk.Label()
        self.riepilogue_bar = Riepilogue()
        self.riepilogue_box.pack_start(self.riepilogue_label, False, False, 0)
        self.riepilogue_box.pack_end(self.riepilogue_bar, False, False, 0)
        self.remove_button = self.riepilogue_bar.clear
        self.install_button = self.riepilogue_bar.button
        self.pack_start(self.basketview_cont, True, True, 0)
        self.pack_start(Gtk.HSeparator(), False, False, 0)
        self.pack_start(self.riepilogue_box, False, False, 0)


class Riepilogue(Gtk.HBox):
    def __init__(self):
        super(Riepilogue, self).__init__()
        self.set_spacing(5)
        self.button = Gtk.Button(label=_("Install Packages"))
        self.clear = Gtk.Button(label=_("Discard"))
        self.pack_start(self.clear, False, False, 0)
        self.pack_start(self.button, False, False, 0)


class PackagesView(Gtk.TreeView):
    def __init__(self):
        super(PackagesView, self).__init__()
        self.model = Gtk.ListStore(str, str, str, str)
        self.namecell = Gtk.CellRendererText()
        self.sizecell = Gtk.CellRendererText()
        self.instcell = Gtk.CellRendererText()
        self.vercell = Gtk.CellRendererText()
        self.namecolumn = Gtk.TreeViewColumn(_("Package"))
        self.sizecolumn = Gtk.TreeViewColumn(_("To Download"))
        self.instcolumn = Gtk.TreeViewColumn(_("To Install"))
        self.vercolumn = Gtk.TreeViewColumn(_("Version"))
        self.namecolumn.pack_start(self.namecell, True)
        self.sizecolumn.pack_start(self.sizecell, False)
        self.instcolumn.pack_start(self.instcell, False)
        self.vercolumn.pack_start(self.vercell, False)
        self.namecolumn.add_attribute(self.namecell, "text", 0)
        self.sizecolumn.add_attribute(self.sizecell, "text", 1)
        self.instcolumn.add_attribute(self.instcell, "text", 2)
        self.vercolumn.add_attribute(self.vercell, "text", 3)
        self.append_column(self.namecolumn)
        self.append_column(self.sizecolumn)
        self.append_column(self.instcolumn)
        self.append_column(self.vercolumn)
