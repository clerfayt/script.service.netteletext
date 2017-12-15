#!/bin/python
# -*- coding: utf-8 -*-
#
# TELETEXT RESOLVERS  (resolve URLs to teletext images)

import urllib2, re

from .utils import *


def loadImageUrls_ORF(page):
	"""Resolves the URL to the given page at ORF Teletext."""
	page = int(page)
	imageURLs = []
	urlPattern = "http://teletext.orf.at/" + str((page/100)*100) + "/" + str(page) + "_%s.%s"
	if pageExists(urlPattern % ("0001", "png")):
		htmlContent = getHtmlContent(urlPattern % ("0001", "htm"))
		noOfSubpages = re.search('">([0-9]+)</a><b></span></td>', htmlContent)
		if noOfSubpages is None:
			imageURLs.append(urlPattern % ("0001", "png"))
		else:
			noOfSubpages = noOfSubpages.group(1)
			for i in range(1, int(noOfSubpages)+1):
				imageURLs.append(urlPattern % (str(i).rjust(4, "0"), "png"))
	return imageURLs


def loadImageUrls_RTP(page):
	"""Resolves the URL to the given page at RTP Teletexto."""
	imageURLs = []
	if pageExists('http://www.rtp.pt/wportal/fab-txt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.png')==True:
		htmlContent = getHtmlContent('http://www.rtp.pt/wportal/fab-txt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.htm')
		noOfSubpages = re.search('">([0-9]+)</A>&nbsp;&nbsp;<A HREF="', htmlContent)
		if noOfSubpages==None:
				imageURLs.append('http://www.rtp.pt/wportal/fab-txt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.png')
		else:
			noOfSubpages = noOfSubpages.group(1)
			for i in range(1,int(noOfSubpages)+1):
				imageURLs.append('http://www.rtp.pt/wportal/fab-txt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_' + str(i).rjust(4, '0') + '.png')
	return imageURLs


def loadImageUrls_SRF(page):
	"""Resolves the URL to the given page at SRF1 Teletext."""
	page = int(page)
	imageURLs = []
	imgUrl = "http://api.teletext.ch/online/pics/medium/SRF1_%s-0.gif" % str(page)
	if pageExists(imgUrl): imageURLs.append(imgUrl)
	return imageURLs


###################################################################################
# HELPER FUNCTIONS

def pageExists(url):
	request = urllib2.Request(url)
	request.get_method = lambda : 'HEAD'
	try:
		response = urllib2.urlopen(request)
		return True
	except (urllib2.HTTPError, urllib2.URLError):
		return False


def getHtmlContent(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
