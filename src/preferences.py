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

from gi.repository import Gtk
import control
import gettext

_ = gettext.gettext


class Preferences_UI(Gtk.Window):
    def __init__(self, app):
        super(Preferences_UI, self).__init__()
        control.__init__()
        self.set_size_request(400, -1)
        self.set_resizable(False)
        self.set_icon_name("gtk-preferences")
        self.connect("destroy", self.hide_window)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title(_("Xenta Software Center Preferences"))
        self.box = Gtk.VBox()
        self.box.set_spacing(5)
        self.box.set_border_width(5)
        self.bbox = Gtk.HBox()
        self.bbox.set_spacing(5)
        self.bbox2 = Gtk.HButtonBox()
        self.bbox2.set_spacing(5)
        self.bbox2.set_layout(Gtk.ButtonBoxStyle.END)
        self.app = app
        self.combo = Gtk.Switch()
        self.toggle = Gtk.Switch()
        self.scrot = Gtk.Switch()
        self.internet = Gtk.Switch()
        self.cancel = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        self.cancel.connect("clicked", self.hide_window)
        self.apply = Gtk.Button.new_from_stock(Gtk.STOCK_APPLY)
        self.apply.connect("clicked", self.apply_preferences)
        self.software_source = Gtk.Button(_("Open Software Properties"))
        self.software_source.connect(
            "clicked", self.app.open_software_properties)
        self.about = Gtk.Button.new_from_stock(Gtk.STOCK_ABOUT)
        self.about.connect("clicked", self.app.on_show_about)
        self.refresh_func = None
        self.combo.set_active(control.controller.expert_mode)
        self.toggle.set_active(control.controller.render_icons)
        self.scrot.set_active(control.controller.show_scrot)
        self.internet.set_active(control.controller.check_internet)
        self.bbox2.pack_start(self.apply, False, False, 0)
        self.bbox2.pack_start(self.cancel, False, False, 0)
        self.bbox.pack_start(self.software_source, False, False, 0)
        self.bbox.pack_end(self.about, False, False, 0)
        #----------------------------------------------
        lab = Gtk.Label("<b>" + _("General") + "</b>")
        lab.props.xalign = 0.0
        lab.set_use_markup(True)
        self.box.pack_start(lab, False, False, 0)
        self.box2 = Gtk.HBox()
        self.box2.set_border_width(5)
        self.box2.pack_start(Gtk.Label(_("Expert Mode")), False, False, 0)
        self.box2.pack_end(self.combo, False, False, 0)
        self.box.pack_start(self.box2, False, False, 0)
        lab = Gtk.Label("<b>" + _("Performance") + "</b>")
        lab.props.xalign = 0.0
        lab.set_use_markup(True)
        self.box.pack_start(lab, False, False, 0)
        self.box2 = Gtk.HBox()
        self.box2.set_border_width(5)
        self.box2.pack_start(Gtk.Label(_(
            "Render Icons")), False, False, 0)
        self.box2.pack_end(self.toggle, False, False, 0)
        self.box.pack_start(self.box2, False, False, 0)
        self.box2 = Gtk.HBox()
        self.box2.set_border_width(5)
        self.box2.pack_start(Gtk.Label(_(
            "Download Screenshots")), False, False, 0)
        self.box2.pack_end(self.scrot, False, False, 0)
        self.box.pack_start(self.box2, False, False, 0)
        self.box2 = Gtk.HBox()
        self.box2.set_border_width(5)
        self.box2.pack_start(Gtk.Label(_(
            "Check connection at startup")), False, False, 0)
        self.box2.pack_end(self.internet, False, False, 0)
        self.box.pack_start(self.box2, False, False, 0)
        #----------------------------------------------
        self.box.pack_start(self.bbox, False, False, 0)
        self.box.pack_start(self.bbox2, False, False, 0)
        self.add(self.box)

    def hide_window(self, widget):
        '''Hide the dialog'''
        self.hide()
        self.app.ui.set_sensitive(True)

    def show(self):
        '''Show the dialog'''
        self.show_all()

    def apply_preferences(self, widget):
        '''Apply the changes'''
        control.controller.conf_file.write("")
        control.controller.conf_file.close()
        control.controller.conf_file = open(control.controller.file_path, "w")
        control.controller.parser.set(
            "General", "app_install_directory",
            "/usr/share/app-install/desktop/")
        control.controller.parser.set(
            "General", "expert_mode", self.combo.get_active())
        control.controller.parser.set(
            "General", "render_icons", self.toggle.get_active())
        control.controller.parser.set(
            "General", "show_scrot", self.scrot.get_active())
        control.controller.parser.set(
            "General", "check_internet", self.internet.get_active())
        control.controller.parser.set(
            "General", "db_path", "/var/cache")
        control.controller.parser.set(
            "General", "categories_file", "data/categories")
        control.controller.parser.write(control.controller.conf_file)
        control.controller.conf_file.close()
        self.hide_window(None)
        self.refresh_func()
