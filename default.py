#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import datetime

from resources.lib.utils import *
from resources.lib.resolvers import *

class Channel():
	def __init__(self, name, resolverFunc, lowestPage = 100, highestPage = 888):
		self.name = name
		self.resolverFunc = resolverFunc
		self.lowestPage = lowestPage
		self.highestPage = highestPage


class TeletextWindow(xbmcgui.WindowDialog):

	CHANNEL_LIST = [Channel("ORF", loadImageUrls_ORF, 100, 899),
                        Channel("SRF1", loadImageUrls_SRF, 100, 899),
                        Channel("RTP", loadImageUrls_RTP, 100, 888)]

	DEFAULT_PAGE = 100

        ACTION_EXIT           = 0
        ACTION_SELECT_CHANNEL = 1
        ACTION_ENTER_PAGE     = 2
        ACTION_NEXT_PAGE      = 3
        ACTION_PREV_PAGE      = 4
        ACTION_NEXT_SUB       = 5
        ACTION_PREV_SUB       = 6

	def __init__(self, channel = None, page = DEFAULT_PAGE):
                """Constructor"""
                self.noOfChannels = len(self.CHANNEL_LIST)
		self.channel = channel if channel is not None else MySettings.defaultChannel(self.CHANNEL_LIST)
		self.page = page
                if MySettings.askForChannelAtStartup():
                        self.channel = self.selectChannel()
                self.initPageData(self.page)
                self.initPage()


        def initPageData(self, page, subpage = 1):
                """Retrieve / Set the data."""
                self.page = page
                self.subpage = subpage
                self.imageURLs = self.channel.resolverFunc(self.page)


	def initPage(self):
                """Build the UI."""
                # bgImage gets displayed when changing from one page to another
                self.bgImage = xbmcgui.ControlImage(0,0,1280,720, getNotFoundImgPath())
                self.bgImage.setImage(IMAGEFOLDER+"/background.jpg", useCache=False)
                self.addControl(self.bgImage)
                self.pageImage = xbmcgui.ControlImage(0,0,1280,720, getNotFoundImgPath())
		if len(self.imageURLs) > 0:
			self.pageImage.setImage(self.imageURLs[self.subpage-1], useCache=False)

		self.addControl(self.pageImage)

                dt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
		if len(self.imageURLs) > 1:
			self.pagelabel = xbmcgui.ControlLabel(30, 5, 500, 500,
			                                      "%s   %s %d - %d/%d" % (dt, transl(30001), self.page, self.subpage, len(self.imageURLs)),
			                                      font="font24_title", angle=-90)
		else:
			self.pagelabel = xbmcgui.ControlLabel(30, 5, 500, 500,
			                                      "%s   %s %d" % (dt, transl(30001), self.page),
			                                      font="font24_title", angle=-90)
		self.addControl(self.pagelabel)

		if self.noOfChannels > 1:
			self.buttonSelectChannel = xbmcgui.ControlButton(1202,340,80,70, '',
			                                                 focusTexture=IMAGEFOLDER+'buttonSelectChannel.png', noFocusTexture=IMAGEFOLDER+'buttonSelectChannel.png')
			self.addControl(self.buttonSelectChannel)
		self.buttonEnterPage = xbmcgui.ControlButton(0,340,80,70,'', focusTexture=IMAGEFOLDER+'buttonEnterPage.png', noFocusTexture=IMAGEFOLDER+'buttonEnterPage.png')
		self.addControl(self.buttonEnterPage)
		self.buttonExit = xbmcgui.ControlButton(1202,0,80,70,'', focusTexture=IMAGEFOLDER+'buttonExit.png', noFocusTexture=IMAGEFOLDER+'buttonExit.png')
		self.addControl(self.buttonExit)
		self.buttonPrevious = xbmcgui.ControlButton(0,652,80,70,'', focusTexture=IMAGEFOLDER+'buttonPrevious.png', noFocusTexture=IMAGEFOLDER+'buttonPrevious.png')
		self.addControl(self.buttonPrevious)
		self.buttonNext = xbmcgui.ControlButton(1202,652,80,70,'', focusTexture=IMAGEFOLDER+'buttonNext.png', noFocusTexture=IMAGEFOLDER+'buttonNext.png')
		self.addControl(self.buttonNext)


	def onControl(self, control):
                """Called when a control is activated."""
		if control == self.buttonPrevious:
			self.performAction(self.ACTION_PREV_SUB)
		elif control == self.buttonNext:
			self.performAction(self.ACTION_NEXT_SUB)
		elif control == self.buttonEnterPage:
			self.performAction(self.ACTION_ENTER_PAGE)
		elif control == self.buttonExit:
			self.performAction(self.ACTION_EXIT)
		elif control == self.buttonSelectChannel:
                        self.performAction(self.ACTION_SELECT_CHANNEL)


	def onAction(self, action):
                """Called on click or keyboard events."""
		actionId = action.getId()
		if actionId == xbmcgui.ACTION_MOVE_LEFT:
                        self.performAction(self.ACTION_PREV_SUB)
		elif actionId == xbmcgui.ACTION_MOVE_RIGHT:
                        self.performAction(self.ACTION_NEXT_SUB)
		elif actionId == xbmcgui.ACTION_MOVE_DOWN:
			self.performAction(self.ACTION_PREV_PAGE)
		elif actionId == xbmcgui.ACTION_MOVE_UP:
			self.performAction(self.ACTION_NEXT_PAGE)
		elif actionId == xbmcgui.ACTION_SELECT_ITEM:
			self.performAction(self.ACTION_ENTER_PAGE)
		elif actionId == xbmcgui.ACTION_PREVIOUS_MENU or \
                     actionId == xbmcgui.ACTION_NAV_BACK:
			self.performAction(self.ACTION_EXIT)
		elif actionId == xbmcgui.ACTION_PAUSE:
                        self.performAction(self.ACTION_SELECT_CHANNEL)
		elif actionId == xbmcgui.REMOTE_1 or \
                     actionId == xbmcgui.REMOTE_2 or \
                     actionId == xbmcgui.REMOTE_3 or \
                     actionId == xbmcgui.REMOTE_4 or \
                     actionId == xbmcgui.REMOTE_5 or \
                     actionId == xbmcgui.REMOTE_6 or \
                     actionId == xbmcgui.REMOTE_7 or \
                     actionId == xbmcgui.REMOTE_8 or \
                     actionId == xbmcgui.REMOTE_9:
                        self.performAction(self.ACTION_ENTER_PAGE, str(actionId - xbmcgui.REMOTE_0))


        def performAction(self, action, args=None):
                """Perform my custom actions."""

                if action == self.ACTION_NEXT_PAGE:
                        if self.page == self.channel.highestPage: self.page = self.channel.lowestPage
			else: self.page += 1
			self.initPageData(self.page)
			self.updatePage()
		
                elif action == self.ACTION_PREV_PAGE:
                        if self.page == self.channel.lowestPage: self.page = self.channel.highestPage
			else: self.page -= 1
			self.initPageData(self.page)
			self.updatePage()
		
                elif action == self.ACTION_NEXT_SUB:
                        if len(self.imageURLs) > 1:
                                if self.subpage == len(self.imageURLs): self.subpage = 1
                                else: self.subpage += 1
                                self.updatePage()
                
                elif action == self.ACTION_PREV_SUB:
                        if len(self.imageURLs) > 1:
                                if self.subpage == 1: self.subpage = len(self.imageURLs)
                                else: self.subpage -= 1
                                self.updatePage()
                
                elif action == self.ACTION_ENTER_PAGE:
                        tmpPage = self.enterPageNumber(args if args else "")
			if tmpPage:
                                self.initPageData(tmpPage)
                                self.updatePage()
                
                elif action == self.ACTION_SELECT_CHANNEL:
                        if self.noOfChannels > 1:
                                self.channel = self.selectChannel()
                                self.initPageData(self.DEFAULT_PAGE)
                                self.updatePage()
                
                elif action == self.ACTION_EXIT:
                        self.close()


	def updatePage(self):
		if self.pageImage is None or self.imageURLs is None or self.pagelabel is None:
			return
		if len(self.imageURLs) > 0:
			self.pageImage.setImage(self.imageURLs[self.subpage-1], useCache=False)
		else:
			self.pageImage.setImage(getNotFoundImgPath())

		dt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
		if len(self.imageURLs) > 1:
			self.pagelabel.setLabel("%s   %s %d - %d/%d" % (dt, transl(30001), self.page, self.subpage, len(self.imageURLs)))
		else:
			self.pagelabel.setLabel("%s   %s %d"         % (dt, transl(30001), self.page))


	def enterPageNumber(self, default = ""):
		page_ = xbmcgui.Dialog().numeric(0, transl(30002) + (" (%d-%d)" % (self.channel.lowestPage, self.channel.highestPage)), default)
		if page_ == "": return None
		page_ = int(page_)
		return page_ if page_ in range(self.channel.lowestPage, self.channel.highestPage+1) else self.enterPageNumber()


	def channelNames(self):
		return list(c.name for c in self.CHANNEL_LIST)


	def selectChannel(self):
		c = xbmcgui.Dialog().select(transl(30003), self.channelNames())
		if c not in range(0, self.noOfChannels): c = 0
		return self.CHANNEL_LIST[c]


###################################################################################
# STARTUP CODE
window = TeletextWindow()
window.doModal()
