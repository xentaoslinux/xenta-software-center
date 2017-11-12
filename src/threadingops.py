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
from gi.repository import Pango
from gi.repository import GdkPixbuf
from ConfigParser import RawConfigParser
from notify import notify
import control
import os
from aptdaemon import client, gtk3widgets

from . import LOG

import gettext

_ = gettext.gettext

client = client.AptClient()
dialog = gtk3widgets.AptProgressDialog(debconf=True)

control.__init__()

import sqlite3
db_path = os.path.join(control.controller.db_path, "lsc_packages.db")
try:
    db = sqlite3.Connection(db_path)
    cursor = db.cursor()
except sqlite3.OperationalError:
    result = os.system('gksu -m %s xenta-software-center-build-db %s %s \
                       /usr/share/LSC/categories.ini' % (_(
        '"The database for Xenta Software Center needs to be (re-)created"'),
        db_path, control.controller.app_install_directory))
    if result == 0:
        db = sqlite3.Connection(db_path)
        cursor = db.cursor()
    else:
        pass
        #Error message should appear. There is no db and it couldn't be created
try:
    cursor.execute("SELECT * FROM packages")
except sqlite3.OperationalError:
    result = os.system('gksu -m %s xenta-software-center-build-db %s %s \
                       /usr/share/LSC/categories.ini' % (_(
        '"The database for Xenta Software Center needs to be (re-)created"'),
        db_path, control.controller.app_install_directory))
    if result == 0:
        db = sqlite3.Connection(db_path)
        cursor = db.cursor()
    else:
        pass
        # Error message: Table exists, but seems empty and couldn't be filled.


class append_packages:
    def __init__(self, app, category, status, model, showboth):
        control.__init__()
        self.app = app
        self.category = category
        self.status = status
        self.model = model
        self.sortkey = 0
        self.showboth = showboth

    def run(self):
        '''Append the packages to the given Gtk.ListStore'''

        self.status_dict = {
            0: "",
            1: "",
            2: "",
            4: "",
            5: "",
            6: Gtk.STOCK_YES
        }

        LOG.debug("sensitive!")
        if control.controller.expert_mode:
            id = 1
        else:
            id = 0
        if self.showboth:
            for items in cursor.execute(
                    "SELECT * FROM %s ORDER BY name" % (self.category)):
                self.app.append_packages_appending(
                    items, self.status, self.status_dict, self.model, (1, 1))

        else:
            for items in cursor.execute(
                    "SELECT * FROM %s WHERE ID=%s ORDER BY name" %
                    (self.category, id)):
                self.app.append_packages_appending(
                    items, self.status, self.status_dict, self.model, (1, 1))

        self.app.ui.pkgs_count.set_text("%s " % len(self.model) +
                                        _("packages listed"))
        if self.app.ui.search_pkg.search_entry.get_text() != \
                self.app.ui.search_pkg.search_string:
            self.app.ui.search_pkg.search_function(
                self.app.ui.search_pkg.search_entry.get_text(), 20)


def get_categories():
    categories = {}
    cat_parser = RawConfigParser()
    if os.path.isfile(os.path.join("data", "categories.ini")):
        cat = open(os.path.join("data", "categories.ini"))
    else:
        cat = open(os.path.join(
            control.controller.data_system_path, "categories.ini"))
    cat_parser.readfp(cat)
    for section in cat_parser.sections():
        name = cat_parser.get(section, "name")
        icon = cat_parser.get(section, "icon")
        #tags = cat_parser.get(section, "contains")
        showboth = cat_parser.getboolean(section, "showboth")
        categories[section] = [icon, _(name), showboth]
    return categories


def getdesc(pkg):
    for items in cursor.execute(
            "SELECT desc FROM packages WHERE pkg_name='%s'" % pkg):
        return items[0]


def getshortdesc(pkg):
    for items in cursor.execute(
            "SELECT comment FROM packages WHERE pkg_name='%s'" % pkg):
        return items[0]


def getdeps(pkg):
    tmp = ""
    for item in cursor.execute(
            "SELECT deps FROM packages WHERE pkg_name='%s'" % pkg):
        tmp = item[0]
    if tmp == "":
        return []
    else:
        return tmp.split(";")


def getrecs(pkg):
    tmp = ""
    for item in cursor.execute(
            "SELECT recs FROM packages WHERE pkg_name='%s'" % pkg):
        tmp = item[0]
    if tmp == "":
        return []
    else:
        return tmp.split(";")


def download_screenshot(pkg, path, image, button):
    path_screenshot = os.path.join("/usr/share/pyshared/",
                                   "xenta-software-center/",
                                   "xenta-software-center-download-scrot")
    if os.path.isfile(path_screenshot):
        response = os.popen(" ".join(["python",
                            path_screenshot,
                            pkg, path])).read()
    else:
        response = os.popen(" ".join(["python",
                            "scripts/xenta-software-center-download-scrot",
                            pkg, path])).read()
    button.set_visible(True)
    if os.path.exists("/".join([path, pkg])):
        try:
            scrot_buf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                "/".join([path, pkg]), 250, 250)
            image.set_from_pixbuf(scrot_buf)
        except:
            pass


def download_review(pkg, path):
    path_review = os.path.join("/usr/share/pyshared/",
                               "xenta-software-center/",
                               "xenta-software-center-download-review")
    if os.path.isfile(path_review):
        response = os.popen(" ".join(["python",
                            path_review,
                            pkg, path])).read()
    else:
        response = os.popen(" ".join(["python",
                            "scripts/xenta-software-center-download-review",
                            pkg, path])).read()
    return path + pkg


def parse_review(pkg, path, box):
    if os.path.exists(path + pkg + ".ini"):
        review_parser = RawConfigParser()
        review = open(path + pkg + ".ini", "r")
        review_parser.readfp(review)
        for reviews in review_parser.sections():
            summary = Gtk.Label("<b>" + review_parser.get(
                reviews, "summary").capitalize() + "</b>")
            summary.set_use_markup(True)
            summary.props.xalign = 0.0
            summary.props.xpad = 5
            text = Gtk.Label(review_parser.get(reviews, "review_text"))
            text.props.xalign = 0.0
            text.props.xpad = 10
            text.set_line_wrap_mode(Pango.WrapMode.WORD)
            text.set_line_wrap(True)
            box.pack_start(summary, False, False, 0)
            box.pack_start(text, False, False, 0)
    if len(box.get_children()) == 1:  # If only the Reviews title is in the box
        summary = Gtk.Label("<b>" + _("No reviews available") + "</b>")
        summary.set_use_markup(True)
        box.pack_start(summary, False, False, 0)


def install_package(pkgs, app):
    transaction = client.install_packages(pkgs)
    transaction.connect("finished", finish_trans, app, True)
    dialog.set_transaction(transaction)
    LOG.debug("running dialog")
    dialog.run()


def remove_package(pkgs, app):
    transaction = client.remove_packages(pkgs)
    transaction.connect("finished", finish_trans, app, False)
    dialog.set_transaction(transaction)
    LOG.debug("running dialog")
    dialog.run()


def get_if_apt_lies(pkg):
    '''test if the apt cache lies'''
    result = os.system("apt-get -s install %s" % pkg)
    if result == 0:
        # Apt Cache lies, we can install it!
        return True
    else:
        # It's true, damaged packages
        return False


def finish_trans(transaction, exit_status, root, inst):
    if exit_status == "exit-success":
        dialog.hide()
        LOG.debug("success")
        if inst:
            notify("installed")
        else:
            notify("removed")
        root.choosed_page = 1
        root.refresh_system_call()
    else:
        dialog.hide()
        finishdialog = gtk3widgets.AptErrorDialog(error=transaction.error)
        finishdialog.run()
        LOG.warn("failed")
