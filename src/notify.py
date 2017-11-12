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

from gi.repository import Notify
import gettext

from . import LOG

_ = gettext.gettext
Notify.init("Xenta Software Center")


def notify(message):
    show_notif = True

    if(message == "installed"):
        notify_message = "Apps installed successfully"
    elif(message == "removed"):
        notify_message = "Apps removed successfully"
    elif (message == "no-connection"):
        notify_message = "No connection found, you can't install \n\
                         applications, however you can browse for them"
    else:
        show_notif = False
        LOG.error("ERROR: No rule for command:", message)

    if show_notif:
        lubuntu_notify = Notify.Notification.new(
            "Xenta Software Center", _(notify_message),
            "xenta-software-center")
        lubuntu_notify.show()
