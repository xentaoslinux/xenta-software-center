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


class Dialog(Gtk.Dialog):
    def __init__(self, image, title):
        super(Dialog, self).__init__()
        self.set_title(title)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        self.box = self.get_children()[0]
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_shadow_type(Gtk.ShadowType.IN)
        self.image = Gtk.Image()
        self.image.set_from_file(image)
        self.scroll.add_with_viewport(self.image)
        self.submit = Gtk.LinkButton(
            uri="http://screenshots.ubuntu.com/upload",
            label=_("Submit a screenshot"))
        self.box.pack_start(self.scroll, True, True, 0)
        self.box.pack_start(self.submit, False, False, 0)
        self.box.show_all()
        self.set_size_request(600, 500)
        self.run()
        self.destroy()
