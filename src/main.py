#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
#  main.py
#
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
import apt_pkg
import os
#----LSC MODULES----
import UI
import control
import preferences
import threadingops
from testnet import testnet
from notify import notify

from . import LOG

import subprocess
import gettext

_ = gettext.gettext

gettext.install("xenta-software-center", "/usr/share/locale", unicode=1)
gettext.bindtextdomain("xenta-software-center", "/usr/share/locale")
gettext.textdomain("xenta-software-center")


class LscControl:
    '''The class that control the program'''
    def __init__(self):
        self.ui = UI.Gui(
            self.on_selected_category, threadingops.get_categories())
        self.apps_model_search = Gtk.ListStore(str, str, str, str)
        self.installed_model_search = Gtk.ListStore(str, str, str, str)
        #-------------------------------------------------------
        self.choosed_page = 0
        self.last_page = 0
        self.actual_category = "packages"
        self.was_searching = False
        self.startup = True
        self.active_for_search = True
        #-------------------------------------------------------
        self.action_group = None
        self.refresh_system_call()
        #-------------------------------------------------------
        self.ui.pages.get_function = self.get_func
        self.ui.pages.installed_function = self.installed_func
        self.ui.search_pkg.search_function = self.search
        #-------------------------------------------------------
        self.ui.pages.basket_function = self.refresh_app_basket
        self.ui.install_pkgs.connect("clicked", self.on_install_pkgs)
        self.ui.remove_mai_button.connect("clicked", self.on_clear_basket)
        #-------------------------------------------------------
        self.ui.toolbar.back.connect("clicked", self.back_to_last_page)
        self.ui.toolbar.settings.connect("clicked", self.on_show_preferences)
        #-------------------------------------------------------
        self.ui.apps_all.connect("cursor-changed", self.on_selected_available)
        self.ui.apps_installed.connect("cursor-changed",
                                       self.on_selected_available)
        self.ui.apps_all.connect("row-activated", self.on_more_info_row, 0)
        self.ui.apps_installed.connect("row-activated",
                                       self.on_more_info_row, 1)
        self.ui.statusbox.combo.connect("changed",
                                        self.statusbox_combo_changed)
        #-------------------------------------------------------
        self.ui.apps_message.add_remove_button.connect(
            "clicked", self.on_install_or_remove, None)
        self.ui.installed_message.add_remove_button.connect(
            "clicked", self.on_install_or_remove, self.ui.apps_installed)
        self.ui.apps_message.details_button.connect(
            "clicked", self.on_more_info, 0)
        self.ui.installed_message.details_button.connect(
            "clicked", self.on_more_info, 1)
        #-------------------------------------------------------
        self.ui.appsinfo.button.connect(
            "clicked", self.on_install_or_remove, self.ui.apps_installed)
        self.ui.appsinfo.scrot_button.connect(
            "button-press-event", self.maximize_screenshot)
        self.ui.appsinfo.check_reviews.connect("clicked", self.download_review)
        #-------------------------------------------------------
        self.ui.no_found_button.connect("clicked", self.search_in_all)
        #-------------------------------------------------------
        self.depends = []
        #-------------------------------------------------------

    #check internet via testnet.py
    def check_internet(self):
        reposavailable = testnet()
        if(reposavailable != 0):
            notify("no-connection")
            control.controller.show_scrot = False
            control.controller.show_reviews = False

    def back_to_last_page(self, widget):
        self.ui.statusbox.installed.set_from_stock('', 1)
        if self.last_page == 0:
            self.was_searching = False
            self.ui.toolbar.back.set_sensitive(False)
            self.back_home(widget)
        elif self.last_page == 2:
            self.ui.statusbox.combo.set_visible(self.was_searching)
            self.ui.toolbar.back.set_sensitive(False)
            self.ui.pages.change_page(self.last_page)
            self.ui.search_pkg.set_sensitive(True)
            self.ui.categorie_label.set_text(self.last_page_label)
            self.ui.categorie_icon.set_from_icon_name(
                self.last_page_icon, Gtk.IconSize.LARGE_TOOLBAR)
        elif self.ui.pages.get_current_page() == 1:
            self.last_page = 0
            self.back_home(widget)
        else:
            self.ui.statusbox.combo.set_visible(self.was_searching)
            self.ui.pages.change_page(self.last_page)
            self.ui.search_pkg.set_sensitive(True)
            self.ui.categorie_label.set_text(self.last_page_label)
            self.ui.categorie_icon.set_from_icon_name(
                self.last_page_icon, Gtk.IconSize.LARGE_TOOLBAR)

    def on_more_info_row(self, widget, view, path, num):
        self.on_more_info(None, num)

    def get_func(self):
        if len(self.ui.apps_all.model) == 0:
            self.back_home(None)
        else:
            self.ui.pages.change_page(1)
            self.category_infos = self.ui.categories_dict[
                self.choosed_category]
            self.ui.categorie_icon.set_from_icon_name(
                self.category_infos[0], Gtk.IconSize.LARGE_TOOLBAR)
            self.ui.categorie_label.set_text(self.category_infos[1])
            self.ui.pkgs_count.set_text("%s " % len(self.ui.apps_all.model) +
                                        _("packages listed"))
            self.ui.search_pkg.set_sensitive(True)
        self.ui.installed_message.set_visible(False)
        self.ui.apps_message.set_visible(False)

    def installed_func(self):
        self.append_packages_call("packages", [
            apt_pkg.CURSTATE_NOT_INSTALLED,
            apt_pkg.CURSTATE_CONFIG_FILES,
            apt_pkg.CURSTATE_HALF_CONFIGURED,
            apt_pkg.CURSTATE_HALF_INSTALLED,
            apt_pkg.CURSTATE_UNPACKED
            ], self.ui.apps_installed.model, False)
        self.ui.categorie_icon.set_from_icon_name("harddrive",
                                                  Gtk.IconSize.LARGE_TOOLBAR)
        self.ui.categorie_label.set_text(_("Installed"))
        self.actual_category = "packages"
        self.ui.pkgs_count.set_text("%s " % len(self.ui.apps_installed.model) +
                                    _("packages listed"))
        self.ui.installed_message.set_visible(False)
        self.ui.apps_message.set_visible(False)
        self.ui.search_pkg.set_sensitive(True)

    def on_selected_category(self, widget):
        '''Handle the change of section'''
        #print self.ui.categories_button_dict[widget]
        self.ui.pages.can_home = True
        self.ui.toolbar.refresh_back_forward(self.ui.pages.can_home)
        self.choosed_category = self.ui.categories_button_dict[widget]
        self.category_infos = self.ui.categories_dict[self.choosed_category]
        self.ui.pages.change_page(1)
        self.ui.categorie_icon.set_from_icon_name(
            self.category_infos[0], Gtk.IconSize.LARGE_TOOLBAR)
        self.ui.categorie_label.set_text(self.choosed_category)
        self.actual_category = self.ui.categories_button_dict[widget]
        self.append_packages_call(self.choosed_category, [],
                                  self.ui.apps_all.model,
                                  self.category_infos[2])

    def statusbox_combo_changed(self, widget):
        if self.active_for_search:
            if widget.get_active() == 0:
                self.search(self.ui.search_pkg.search_entry.get_text(), 20)
            else:
                self.search(self.ui.search_pkg.search_entry.get_text(), False)

    ###########################################################
    # Functions related to the "Available" section
    #
    def search_in_all(self, widget):
        '''Search in all the sections'''

        LOG.debug("search in all")
        self.ui.no_found_box.set_visible(False)
        self.ui.apps_scrolled.set_visible(True)
        self.ui.apps_all.set_model(self.ui.apps_all.model)
        self.actual_category = "packages"
        self.section = self.ui.categories_dict[self.actual_category]
        self.searched = self.ui.search_pkg.search_entry.get_text()
        self.ui.search_pkg.clean_text()
        self.append_packages_call("packages", [], self.ui.apps_all.model,
                                  self.section[2])
        self.ui.search_pkg.set_searching_text(self.searched)
        self.search(self.searched, 20)
        self.choosed_category = self.ui.categorie_label.get_text()

    def on_selected_category2(self, widget, path):
        '''Handle the change of section'''
        self.choosed_category = self.ui.categories_model[path[0]]
        self.ui.pages.change_page(1)
        self.ui.categorie_icon.set_from_icon_name(self.choosed_category[1],
                                                  Gtk.IconSize.LARGE_TOOLBAR)
        self.ui.categorie_label.set_text(self.choosed_category[0])
        self.actual_category = self.choosed_category[0]
        self.append_packages_call(self.choosed_category[2], [],
                                  self.ui.apps_all.model,
                                  self.choosed_category[2])

    def on_selected_available(self, widget):
        '''Show the bottom box with the message'''
        if widget is None:
            widget = self.ui.apps_all.model
        if widget.get_cursor()[0] is not None:
            self.pkg = widget.get_model()[widget.get_cursor()[0]]
            self.pkg_selected = (
                self.pkg[2],
                self.pkg[0],
                self.pkg[1],
                self.pkg[3]
            )
            self.ui.apps_message.package_name.set_text(_(
                "Selected package ") + "'%s' " % self.pkg_selected[0])
            self.ui.installed_message.package_name.set_text(_(
                "Selected package ") + "'%s' " % self.pkg_selected[0])
            if not self.pkg_selected[3] == Gtk.STOCK_YES:
                if self.pkg_selected[0] in self.marked_as_install:
                    LOG.info("this app is marked as install")
                    self.ui.apps_message.add_remove_button.set_label(_(
                        "Added to the Apps Basket"))
                    self.ui.apps_message.add_remove_button.set_sensitive(False)
                    self.ui.appsinfo.button.set_label(_(
                        "Added to the Apps Basket"))
                    self.ui.appsinfo.button.set_sensitive(False)
                else:
                    LOG.info("this app is available")
                    self.ui.apps_message.add_remove_button.set_label(_(
                        "Add to the Apps Basket"))
                    self.ui.apps_message.add_remove_button.set_sensitive(True)
                    self.ui.appsinfo.button.set_label(_(
                        "Add to the Apps Basket"))
                    self.ui.appsinfo.button.set_sensitive(True)
            else:
                LOG.info("this app is installed")
                self.ui.apps_message.add_remove_button.set_label(_(
                    "Remove from the system"))
                self.ui.apps_message.add_remove_button.set_sensitive(True)
                self.ui.installed_message.add_remove_button.set_label(_(
                    "Remove from the system"))
                self.ui.installed_message.add_remove_button.set_sensitive(True)
                self.ui.appsinfo.button.set_label(_("Remove from the system"))
                self.ui.appsinfo.button.set_sensitive(True)
            self.ui.apps_message.set_visible(True)
            self.ui.installed_message.set_visible(True)

    def on_install_or_remove(self, widget, dialog):
        '''Handle the remove/install button'''
        #print widget.get_label()
        if widget.get_label() == _("Add to the Apps Basket"):
            if dialog:
                self.on_add_tbi_from_dialog(None)
            else:
                self.on_add_tbi(None)
        elif widget.get_label() == _("Remove from the system"):
            self.remove_package(None)

    ###########################################################
    # Functions related to the "Installed" section
    #
    def search_installed(self, string):
        '''Search in installed'''
        self.search(string, 20)

    def remove_package(self, widget):
        '''Remove a package'''
        threadingops.remove_package([self.pkg_selected[0]], self)

    ###########################################################
    # Functions related to "Available" and "Installed" section
    #
    def define_icon(self, pkg):
        '''Return the icon of the package'''
        if not control.controller.render_icons:
            return None
        if pkg is not None:
            if self.theme.has_icon(pkg):
                return pkg
        return "deb"

    def append_packages_call(self, category=[], status=[
            apt_pkg.CURSTATE_NOT_INSTALLED], model=None, showboth=False):
        '''Append the packages in the given section to the given model, \
        default non-installed'''
        model.clear()
        self.call = threadingops.append_packages(
            self, category, status, model, showboth)
        self.call.run()

    def search(self, string, show_few_results):
        '''Search the string in the model of the given page'''
        self.smart_mode = False  # false by default
        self.was_searching = True
        self.current_page = self.ui.pages.get_page()
        self.ui.no_found_box.set_visible(False)
        self.ui.no_found_labelbox.set_visible(False)
        self.ui.apps_scrolled.set_visible(True)
        self.ui.installed_scrolled.set_visible(True)
        self.ui.no_installed_found.set_visible(False)
        for items in string:
            # If there is at least one character uppercase
            # the research is case-sensitive
            if items.isupper():
                self.smart_mode = True
        if self.current_page == 0:
            self.ui.pages.can_home = True
            self.ui.toolbar.refresh_back_forward(self.ui.pages.can_home)
            self.ui.pages.change_page(1)
            if len(self.ui.apps_all.model) == 0:
                self.actual_category = "packages"
                self.choosed_category = "packages"
                self.append_packages_call(
                    "packages", [], self.ui.apps_all.model, False)
            self.search(string, show_few_results)
        else:
            if string != "":
                if self.current_page == 2:
                    self.installed_model_search.clear()
                    if not type(show_few_results) == int:
                        show_few_results = len(self.ui.apps_installed.model)
                    else:
                        self.ui.statusbox.combo.set_visible(True)
                        self.active_for_search = False
                        self.ui.statusbox.combo.set_active(0)
                        self.active_for_search = True
                    x = 0
                    y = 0
                    while (x != show_few_results) and \
                            (y < len(self.ui.apps_installed.model)):
                        path = Gtk.TreePath.new_from_string("%s" % y)
                        items = self.ui.apps_installed.model[path]
                        if self.smart_mode:
                            if string in items[0] + items[3]:
                                self.installed_model_search.append(list(items))
                                x += 1
                        else:
                            if string.lower() in items[0].lower() + \
                                    items[3].lower():
                                # lower() => no case-sensitive
                                self.installed_model_search.append(list(items))
                                x += 1
                        y += 1
                    self.ui.apps_installed.set_model(
                        self.installed_model_search)
                    self.ui.categorie_label.set_text(_(
                        "Searching in Installed"))
                    self.current_installed_model = self.installed_model_search
                    if len(self.current_installed_model) == 0:
                        self.ui.installed_scrolled.set_visible(False)
                        self.ui.no_installed_found.set_visible(True)
                    else:
                        self.ui.installed_scrolled.set_visible(True)
                        self.ui.no_installed_found.set_visible(False)
                else:
                    self.section = self.ui.categories_dict[
                        self.actual_category]
                    self.apps_model_search.clear()
                    if not type(show_few_results) == int:
                        show_few_results = len(self.ui.apps_all.model)
                    else:
                        self.ui.statusbox.combo.set_visible(True)
                        self.active_for_search = False
                        self.ui.statusbox.combo.set_active(0)
                        self.active_for_search = True
                    x = 0
                    y = 0
                    while (x != show_few_results) and \
                            (y < len(self.ui.apps_all.model)):
                        path = Gtk.TreePath.new_from_string("%s" % y)
                        items = self.ui.apps_all.model[path]
                        if self.smart_mode:
                            if string in items[0] + items[3]:
                                self.apps_model_search.append(list(items))
                                x += 1
                        else:
                            if string.lower() in items[0].lower() + \
                                    items[3].lower():
                                # lower() => no case-sensitive
                                self.apps_model_search.append(list(items))
                                x += 1
                        y += 1
                    self.ui.apps_all.set_model(self.apps_model_search)
                    self.ui.categorie_icon.set_from_icon_name(
                        self.section[0], Gtk.IconSize.LARGE_TOOLBAR)
                    self.ui.categorie_label.set_text(_("Searching in") +
                                                     " %s" % self.section[1])
                    self.current_apps_model = self.apps_model_search
                    if len(self.current_apps_model) == 0:
                        if self.actual_category != "packages":
                            self.ui.apps_scrolled.set_visible(False)
                            self.ui.no_found_box.set_visible(True)
                        else:
                            self.ui.apps_scrolled.set_visible(False)
                            self.ui.no_found_box.set_visible(False)
                            self.ui.no_found_labelbox.set_visible(True)
                    else:
                        self.ui.apps_scrolled.set_visible(True)
                        self.ui.no_found_box.set_visible(False)
            else:
                if self.current_page == 2:
                    self.ui.apps_installed.set_model(
                        self.ui.apps_installed.model)
                    self.ui.categorie_label.set_text(_("Installed"))
                    self.ui.pkgs_count.set_text("%s " % len(
                        self.ui.apps_installed.model) + _("packages listed"))
                    self.current_installed_model = self.ui.apps_installed.model
                else:
                    self.section = self.ui.categories_dict[
                        self.actual_category]
                    self.ui.apps_all.set_model(self.ui.apps_all.model)
                    self.ui.categorie_icon.set_from_icon_name(
                        self.section[0], Gtk.IconSize.LARGE_TOOLBAR)
                    self.ui.categorie_label.set_text(self.section[1])
                    self.ui.pkgs_count.set_text("%s " % len(
                        self.ui.apps_all.model) + _("packages listed"))
                    self.current_apps_model = self.ui.apps_all.model
                self.was_searching = False
                self.ui.statusbox.combo.set_visible(False)

    ###########################################################
    # Functions related to the "Apps Basket"
    #
    def value_in_model(self, value, model):
        for items in model:
            if items[0].split("(")[0].split()[0] == value:
                return True

    def refresh_app_basket(self):
        '''Refresh the apps basket'''
        self.ui.search_pkg.set_sensitive(False)
        self.ui.apps_basket.model.clear()
        self.total_download = 0
        self.total_install = 0
        self.depends = []
        for items in sorted(self.marked_as_install):
            self.get_pkg_depends(items)
            self.info = self.depcache.get_candidate_ver(self.cache[items])
            self.total_download += self.info.size
            self.total_install += self.info.installed_size
            self.ui.apps_basket.model.append([
                items.capitalize(), apt_pkg.size_to_str(self.info.size),
                apt_pkg.size_to_str(self.info.installed_size),
                self.info.ver_str])
            for item in sorted(self.depends):
                item = item.encode('ascii', 'ignore')
                if not self.cache[item].current_state == \
                        apt_pkg.CURSTATE_INSTALLED:
                    if not self.value_in_model(
                            item, self.ui.apps_basket.model):
                        self.info = self.depcache.get_candidate_ver(
                            self.cache[item])
                        if self.info is None:
                            self.ui.apps_basket.model.append([
                                " " * 4 + item +
                                _(" (requested by ") + items + ")",
                                _("unknown"), _("unknown"), _("unknown")])
                        else:
                            self.total_download += self.info.size
                            self.total_install += self.info.installed_size
                            self.ui.apps_basket.model.append([
                                " " * 4 + item + _(" (requested by ") + items +
                                ")", apt_pkg.size_to_str(self.info.size),
                                apt_pkg.size_to_str(self.info.installed_size),
                                self.info.ver_str])
        if len(self.ui.apps_basket.model) == 0:
            self.ui.riepilogue_label.set_text(_(
                "Put some apps in the basket to install them"))
            self.ui.install_pkgs.set_sensitive(False)
            self.ui.remove_mai_button.set_sensitive(False)
            self.ui.basket_radio.label.set_text(_("Apps Basket"))
        else:
            self.ui.riepilogue_label.set_text("%s %s, %s %s, %s %s" % (len(
                self.marked_as_install), _("package marked"),
                apt_pkg.size_to_str(self.total_download), _("to download"),
                apt_pkg.size_to_str(self.total_install), _("to install")))
            self.ui.install_pkgs.set_sensitive(True)
            self.ui.remove_mai_button.set_sensitive(True)
            self.ui.basket_radio.label.set_text(_("Apps Basket") + " (%s)" %
                                                len(self.marked_as_install))
        self.on_selected_available(self.ui.apps_all)
        self.ui.categorie_icon.set_from_icon_name("applications-other",
                                                  Gtk.IconSize.LARGE_TOOLBAR)
        self.ui.categorie_label.set_text(_("Apps Basket"))
        self.ui.pkgs_count.set_text("%s " % len(self.ui.apps_basket.model) +
                                    _("packages"))
        self.ui.statusbox.combo.set_visible(False)

    def on_clear_basket(self, widget):
        '''Remove the selection from the marked list'''
        self.marked_as_install = []
        self.refresh_app_basket()

    #-------------------------------------------------

    def get_pkg_depends(self, pkgname):
        '''Get the provided version of the given package'''
        self.list2 = []
        self.depends_list = threadingops.getdeps(pkgname)
        if self.depends_list == [u'']:
            self.depends_list = []
        for items in self.depends_list:
            if not items in self.depends:
                if self.cache[items].current_state != 6:
                    self.list2.append(items)
                    self.depends.append(items)
        for items in self.list2:
            # Recursive ;-)
            self.get_pkg_depends(items)

    def if_is_to_replace(self, item, list):
        for items in item:
            if not items in list:
                list.append(items[0])

    def on_install_pkgs(self, widget):
        '''Install the marked packages'''
        threadingops.install_package(self.marked_as_install, self)

    ###########################################################
    # Functions related to all the Gui
    #
    def back_home(self, widget):
        '''Back home, sweet home'''
        self.ui.search_pkg.set_sensitive(True)
        self.ui.set_focus(self.ui.toolbar.settings)
        self.ui.categorie_icon.set_from_icon_name("stock_down",
                                                  Gtk.IconSize.LARGE_TOOLBAR)
        self.ui.categorie_label.set_text(_("Available Categories"))
        self.choosed_page = 0
        self.ui.pkgs_count.set_text(_("Choose a category to start"))
        self.ui.apps_all.model.clear()
        self.ui.pages.back(None, self.ui.toolbar)
        self.ui.statusbox.combo.set_visible(False)
        self.ui.apps_message.set_visible(False)

    def on_reactive_window(self, widget):
        '''Make the window sensitive'''
        widget.set_visible(False)
        self.ui.set_sensitive(True)

    def on_add_tbi_from_dialog(self, widget):
        '''Add package to marked from the dialog'''
        self.ui.appsinfo.button.set_label(_("Added to the Apps Basket"))
        self.ui.appsinfo.button.set_sensitive(False)
        self.on_add_tbi(None)

    def on_more_info(self, widget, status):
        '''Get more info on the selection'''
        self.ui.toolbar.back.set_sensitive(True)
        self.candidate = self.depcache.get_candidate_ver(
            self.cache[self.pkg_selected[0]])
        if self.cache[self.pkg_selected[0]].current_state == \
                apt_pkg.CURSTATE_INSTALLED:
            inst = True
        else:
            inst = False
        self.setup_infos(
            self.pkg_selected[0],
            self.ui.pages,
            self.pkg_selected[2],
            "\n".join([self.pkg_selected[1].split("\n")[0].decode("UTF-8"),
                      threadingops.getshortdesc(
                          self.pkg_selected[0]).decode("UTF-8")]),
            threadingops.getdesc(self.pkg_selected[0]).replace("\n ", "\n"),
            (apt_pkg.size_to_str(self.candidate.size),
             apt_pkg.size_to_str(self.candidate.installed_size)),
            self.candidate.ver_str,
            self.ui.pages.get_current_page(),
            inst
        )

    def app_item_activated(self, widget, path, column, inst_rem):
        '''Handle the activation of a package'''
        self.pkg = widget.get_model()[path[0]]
        self.pkg_selected = (self.pkg[3], self.pkg[0], self.pkg[1])
        self.on_more_info(None, inst_rem)

    def on_add_tbi(self, widget, view=None):
        '''Mark a package'''
        if view is None:
            view = self.ui.apps_all
        self.pkg_name = self.pkg_selected[0]
        if not self.pkg_name in self.marked_as_install:
            self.marked_as_install.append(self.pkg_name)
            self.on_selected_available(view)
            self.ui.basket_radio.label.set_text(_("Apps Basket") + " (%s)" %
                                                len(self.marked_as_install))

    def on_show_preferences(self, widget):
        '''Show the preferences'''
        self.preferences_dialog = preferences.Preferences_UI(self)
        self.preferences_dialog.refresh_func = self.refresh_system_call
        self.preferences_dialog.show()
        self.ui.set_sensitive(False)

    def on_show_about(self, widget):
        '''Show the About dialog'''
        self.ui.about.run()
        self.ui.about.hide()

    def pop_error(self, message):
        '''Pop up an error with the given message as secondary text'''
        self.dialog = Gtk.MessageDialog(self.ui, 0, Gtk.MessageType.ERROR,
                                        Gtk.ButtonsType.OK, _("Error"))
        self.dialog.format_secondary_text(message)
        self.dialog.run()
        self.dialog.destroy()

    def open_software_properties(self, widget):
        '''Open the software properties'''
        subprocess.call(["/usr/bin/software-properties-gtk"])

    def download_review(self, widget):
        name = self.pkg_selected[0]
        self.ui.appsinfo.check_reviews.set_visible(False)
        for widget in self.ui.appsinfo.reviews_box.get_children():
            self.ui.appsinfo.reviews_box.remove(widget)
        self.tmp_review_label = self.ui.appsinfo.screendesc.add_icon_label(
            "<b>" + _("Reviews") + "</b>", "stock_about")
        self.ui.appsinfo.reviews_box.pack_start(self.tmp_review_label,
                                                False, False, 0)
        threadingops.download_review(
            name, control.controller.reviews_path + "/")
        threadingops.parse_review(name, control.controller.reviews_path + "/",
                                  self.ui.appsinfo.reviews_box)
        self.ui.appsinfo.reviews_box.show_all()

    def setup_infos(self, name, pages, icon, title, description, size,
                    version, last_page, installed):
        '''Setup the infos dialog'''
        if installed:
            self.ui.statusbox.installed.set_from_stock(Gtk.STOCK_YES, 1)
        self.ui.appsinfo.scrot.set_from_stock("", 1)
        self.ui.appsinfo.check_reviews.set_visible(True)
        self.ui.appsinfo.reviews_box.set_visible(False)
        self.ui.statusbox.combo.set_visible(False)
        self.last_page = last_page
        self.last_page_label = self.ui.categorie_label.get_text()
        self.last_page_icon = self.ui.categorie_icon.get_icon_name()[0]
        self.ui.search_pkg.set_sensitive(False)
        if(icon is not None):
            self.ui.appsinfo.icon.set_from_icon_name(icon, 6)
        self.ui.appsinfo.title.set_markup(
            "<b><big>"+title.split("\n")[0]+"</big></b>")
        self.ui.appsinfo.desc.set_text(title.split("\n")[-1])
        description_formatted = description.replace("\n.", "\n")
        #This is needed to remove the double short description
        description_formatted = description_formatted.replace(
            title.split("\n")[-1], "")
        self.ui.appsinfo.desctext.set_text(description_formatted.strip())
        self.ui.appsinfo.details.to_download.set_markup(
            "<b>" + _("Download Size:") + "</b>" + " %s" % size[0])
        self.ui.appsinfo.details.installed.set_markup(
            "<b>" + _("Installed Size:") + "</b>" + " %s" % size[1])
        self.ui.appsinfo.details.version.set_markup(
            "<b>" + _("Version:") + "</b>" + " %s (%s)" % (version, name))
        self.ui.categorie_icon.set_from_icon_name(
            "stock_help", Gtk.IconSize.LARGE_TOOLBAR)
        self.ui.categorie_label.set_text(_(
            "Infos on") + " %s" % title.split("\n")[0])
        self.ui.appsinfo.scrot_button.set_visible(False)
        if control.controller.show_scrot:
            threadingops.download_screenshot(
                name, control.controller.screenshots_path + "/",
                self.ui.appsinfo.scrot, self.ui.appsinfo.scrot_button)
        self.package = name
        self.ui.pages.change_page(4)

    def maximize_screenshot(self, widget, event):
        self.dialog = self.ui.scrot_dialog(
            "/".join([control.controller.screenshots_path, self.package]),
            self.package.capitalize() + " screenshot")

    def update_cache(self, widget):
        '''Update the cache'''
        if os.path.isfile(os.path.join(
                "/usr/lib/xenta-software-center/apc.py")):
            self.response = os.popen(" ".join(["python",
                                     "/usr/lib/xenta-software-center/apc.py",
                                     "update"])).read()
        else:
            self.response = os.popen(" ".join(["python", "scripts/apc.py",
                                     "update"])).read()
        #print self.response
        if self.response == "success\n":
            self.choosed_page = 1
            self.refresh_system_call()

    def define_packages(self, name, pkg, icon, categories, (cur, tot)):
        '''Called by threadingops.refresh_system'''
        self.packages.append([name, pkg, icon, categories])
        self.ui.progressbar.set_fraction(float(cur) / float(tot))

    def refresh_system_call(self):
        '''Call the refresh of the app'''
        apt_pkg.init()
        self.cache = apt_pkg.Cache()
        if self.action_group is not None:
            self.action_group.release()
        self.depcache = apt_pkg.DepCache(self.cache)
        self.action_group = apt_pkg.ActionGroup(self.depcache)
        control.__init__()
        self.aid = control.controller.app_install_directory
        self.marked_as_install = []
        self.theme = Gtk.IconTheme.get_default()
        self.theme.append_search_path("/usr/share/app-install/icons/")
        self.current_apps_model = self.ui.apps_all.model
        self.current_installed_model = self.ui.apps_installed.model
        self.refresh_app_basket()
        self.ui.apps_all.set_model(self.ui.apps_all.model)
        self.ui.apps_installed.set_model(self.ui.apps_installed.model)
        self.ui.apps_message.set_visible(False)
        self.ui.installed_message.set_visible(False)
        if self.ui.toolbar.__class__.__name__ == "Toolbar":
            self.ui.toolbar.set_style(3)
        self.packages = []
        if (not self.startup) and (self.ui.pages.get_page() in [1, 2]):
            if self.ui.pages.get_page() == 1:
                self.get_func()
                if self.choosed_category == "fonts":
                    showboth = True
                else:
                    showboth = False
                self.append_packages_call(self.choosed_category, [],
                                          self.ui.apps_all.model, showboth)
            if self.ui.pages.get_page() == 2:
                self.installed_func()
        elif self.startup:
            self.back_home(None)
        if control.controller.check_internet:
            self.check_internet()
        self.startup = False

    def append_packages_appending(
            self, items,  status, status_dict, model, (cur, tot)):
        '''Called by threadingops.append_packages'''
        try:
            self.pkg_in_cache = self.cache[items[1]]
            if not self.pkg_in_cache.current_state in status:
                self.item = [
                    u'\n'.join([items[0].replace("&", "and"),
                               items[3].replace("&", "and")]),
                    self.define_icon(items[4]),
                    u''.join(items[1]),
                    status_dict[self.pkg_in_cache.current_state],
                ]
                model.append(self.item)
                self.ui.progressbar.set_fraction(float(cur) / float(tot))
        except KeyError:
                pass


def lscmain():
    '''Call the mainloop'''
    global app
    app = LscControl()
    Gtk.main()
