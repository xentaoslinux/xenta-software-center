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


class InfoBox(Gtk.VBox):
    def __init__(self):
        super(InfoBox, self).__init__()
        self.view = Gtk.Viewport()
        self.view.set_shadow_type(Gtk.ShadowType.NONE)
        self.view.set_name("lscviewport")
        self.frame = Gtk.ScrolledWindow()
        self.frame.set_shadow_type(Gtk.ShadowType.NONE)
        self.frame.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.frame_box = Gtk.VBox()
        self.bar_box = Gtk.HBox()
        self.bar_box.set_border_width(5)
        self.screendesc = ScreenDesc()
        self.details = self.screendesc.details
        self.infos = self.screendesc.infos
        self.bar = InfoBar()
        self.title = self.infos.title
        self.desc = self.infos.desc
        self.icon = self.infos.icon
        self.button = self.bar.button
        self.desctext = self.screendesc.text
        self.scrot = self.screendesc.screen
        self.scrot_button = self.screendesc.screen_box
        self.check_reviews = self.screendesc.check_reviews
        self.reviews_box = self.screendesc.revs_box
        self.view.add(self.screendesc)
        self.frame.add(self.view)
        self.pack_start(self.frame, True, True, 0)
        self.pack_start(Gtk.HSeparator(), False, False, 0)
        self.pack_start(self.bar_box, False, False, 0)
        self.bar_box.pack_end(self.bar, False, False, 0)


class Infos(Gtk.HBox):
    def __init__(self):
        super(Infos, self).__init__()
        self.set_spacing(5)
        self.icon = Gtk.Image()
        self.box2 = Gtk.VBox()
        self.title = Gtk.Label()
        self.title.props.xalign = 0
        self.desc = Gtk.Label()
        self.desc.props.xalign = 0
        self.box3 = Gtk.VBox()
        self.box2.pack_start(self.title, False, False, 0)
        self.box2.pack_start(self.desc, False, False, 0)
        self.box3.pack_start(self.box2, True, False, 0)
        self.pack_start(self.icon, False, False, 0)
        self.pack_start(self.box3, False, False, 0)


class InfoBar(Gtk.HBox):
    def __init__(self):
        super(InfoBar, self).__init__()
        self.button = Gtk.Button()
        self.pack_start(self.button, False, False, 0)


class ScreenDesc(Gtk.VBox):
    def add_icon_label(self, text, icon):
        self.label = Gtk.Label(text)
        self.label.set_use_markup(True)
        self.icon_box = Gtk.HBox()
        self.icon_box.set_spacing(2)
        self.icon = Gtk.Image()
        self.icon.set_from_icon_name(icon, Gtk.IconSize.MENU)
        self.icon_box.pack_start(self.icon, False, False, 0)
        self.icon_box.pack_start(self.label, False, False, 0)
        return self.icon_box

    def __init__(self):
        super(ScreenDesc, self).__init__()
        self.details = Details()
        self.infos = Infos()
        self.set_spacing(5)
        self.set_border_width(5)
        self.left_box = Gtk.VBox()
        self.left_box.set_spacing(5)
        self.screen_box = Gtk.EventBox()
        self.screen = Gtk.Image()
        self.screen_box.add(self.screen)
        self.screen_box.set_visible_window(False)
        self.screen_frame_box = Gtk.HBox()
        self.screen_frame = Gtk.Frame()
        self.screen_frame.add(self.screen_box)
        self.screen_frame_box.pack_start(self.screen_frame, True, False, 0)
        self.screenbutton_box = Gtk.VBox()
        self.screenbutton_box.pack_start(self.screen_frame_box,
                                         False, False, 0)
        self.screenbutton_box.pack_start(self.details, False, False, 0)
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_left_margin(5)
        self.textview.set_cursor_visible(False)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.desc_title = self.add_icon_label(
            "<b>" + _("Description") + "</b>", "ascii")
        self.check_reviews = Gtk.Button(_("Check for reviews"))
        self.second_box = Gtk.HBox()
        self.second_box.set_spacing(5)
        self.revs_main = Gtk.VBox()
        self.revs_box = Gtk.VBox()
        self.revs_box.set_spacing(5)
        self.revs_main.pack_start(self.check_reviews, False, False, 0)
        self.revs_main.pack_start(self.revs_box, False, False, 0)
        self.left_box.pack_start(self.desc_title, False, False, 0)
        self.left_box.pack_start(self.textview, True, True, 0)
        self.second_box.pack_start(self.left_box, True, True, 0)
        self.second_box.pack_start(self.screenbutton_box, False, False, 0)
        self.text = self.textview.get_buffer()
        self.pack_start(self.infos, False, False, 0)
        self.pack_start(Gtk.HSeparator(), False, False, 0)
        self.pack_start(self.second_box, False, False, 0)
        self.pack_start(Gtk.HSeparator(), False, False, 0)
        self.pack_end(self.revs_main, True, True, 0)


class Details(Gtk.VBox):
    def __init__(self):
        super(Details, self).__init__()
        self.version = Gtk.Label()
        self.to_download = Gtk.Label()
        self.installed = Gtk.Label()
        for items in (self.version, self.to_download, self.installed):
            items.set_ellipsize(Pango.EllipsizeMode.END)
            self.details_box = Gtk.HBox()
            # Keep the 2 methods, until we figure out why 1 method
            # crashes on a system, and not on another one.
            # Reproductible on 2 differnet precise installations.
            try:
                self.arrow = Gtk.Arrow(Gtk.ArrowType.RIGHT,
                                       Gtk.ShadowType.NONE)
            except TypeError:
                self.arrow = Gtk.Arrow()
                self.arrow.set(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE)
            self.details_box.pack_start(self.arrow, False, False, 0)
            self.details_box.pack_start(items, False, False, 0)
            self.pack_start(self.details_box, False, False, 0)
