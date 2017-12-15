#!/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui
import os.path

ADDON = xbmcaddon.Addon()
ADDONNAME = ADDON.getAddonInfo("name")
ADDONFOLDER = ADDON.getAddonInfo("path")
IMAGEFOLDER = ADDONFOLDER + "/resources/img/"


def transl(translationId):
    """Returns the translated string with the given id."""
    return ADDON.getLocalizedString(translationId).encode("utf-8")


def getNotFoundImgPath(languageCode=None):
    if not languageCode:
        languageCode = xbmc.getLanguage(xbmc.ISO_639_1)
    imgFile = IMAGEFOLDER + "notfound-" + languageCode + ".jpg"
    if not os.path.isfile(imgFile):
        myLog("[Teletext] file not found: " + imgFile)
        imgFile = IMAGEFOLDER + "notfound-en.jpg"
    return imgFile


def myNotify(message, header=None, time_=3000, icon=None, sound=True):
    """Send notification. If header==None the addon-name is used.
       If icon==None the addon-icon is used.
    """
    header = ADDONNAME if not header else header
    icon   = ADDON.getAddonInfo('icon') if not icon else icon
    xbmcgui.Dialog().notification(header, message, icon, time_, sound)

def myNotifyError(message, header=None, time_=3000, sound=True):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_ERROR, sound)

def myNotifyWarning(message, header=None, time_=3000, sound=True):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_WARNING, sound)

def myNotifyInfo(message, header=None, time_=3000, sound=True):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_INFO, sound)


def myLog(message, level=xbmc.LOGNOTICE):
    """Log a message."""
    output = "[netteletext]: " + message
    xbmc.log(msg=output, level=level)


class MySettings:
    """Helper class with static methods for retrieving settings values."""
    _addon = xbmcaddon.Addon()
    @staticmethod
    def askForChannelAtStartup():
        return MySettings._addon.getSetting("askForChannelAtStartup") == "true"
    @staticmethod
    def defaultChannel(channelList):
        defChannel = MySettings._addon.getSetting("defaultChannel")
        try:
            return channelList[int(defChannel)]
        except (IndexError, ValueError):
            return channelList[0]
