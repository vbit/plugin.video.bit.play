

import sys, urllib, os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

def playMedia(title, thumbnail, link, mediaType='Video') :
    
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=link)
    li.setInfo(type=mediaType, infoLabels={ "Title": title })
    xbmc.Player().play(item=link, listitem=li)

def parseParameters(inputString=sys.argv[2]):
   
    parameters = {}
    p1 = inputString.find('?')
    if p1 >= 0:
        splitParameters = inputString[p1 + 1:].split('&')
        for nameValuePair in splitParameters:
            if (len(nameValuePair) > 0):
                pair = nameValuePair.split('=')
                key = pair[0]
                value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                parameters[key] = value        
    return parameters

def parseParametersFirstRun(inputString):
   
    parameters = {}
    p1 = inputString.find('?')
    if p1 >= 0:
        splitParameters = inputString[p1 + 1:].split('&')
        for nameValuePair in splitParameters:
            if (len(nameValuePair) > 0):
                pair = nameValuePair.split('=')
                key = pair[0]
                value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                parameters[key] = value        
    return parameters

def notify(addonId, message, timeShown=5000):
   
    addon = xbmcaddon.Addon(addonId)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))


def showError(addonId, errorMessage):
   
    notify(addonId, errorMessage)
    xbmc.log(errorMessage, xbmc.LOGERROR)

def logAddon(input):
    xbmc.log("plugin.video.FPTTEST: %s" %input)


def extractAll(text, startText, endText):
    
    result = []
    start = 0
    pos = text.find(startText, start)
    while pos != -1:
        start = pos + startText.__len__()
        end = text.find(endText, start)
        result.append(text[start:end].replace('\n', '').replace('\t', '').lstrip())
        pos = text.find(startText, end)
    return result

def extract(text, startText, endText):

    start = text.find(startText, 0)
    if start != -1:
        start = start + startText.__len__()
        end = text.find(endText, start + 1)
        if end != -1:
            return text[start:end]
    return None

def extractTitle(text):
    for x in range(0,20):
        request = text.find('/',len(text) - x)
        if request != -1:
            break
    txt = 'Tap ' + text[request+1:len(text)]
    return txt.encode('utf-8')

def makeLinkMenu(inputString):
    params = {'makeMenu':1}
    params['link'] = inputString
    link = makeLink(params)
    return link

def makeThumbnail(inputName):
    mysettings = xbmcaddon.Addon(id='plugin.video.bit.play')
    return os.path.join(mysettings.getAddonInfo('path'), "media", inputName)

def makeLink(params, baseUrl=sys.argv[0]):
    return baseUrl + '?' +urllib.urlencode(dict([k,v] for k,v in params.items()))

def addMenuItem(caption, link, icon=None, thumbnail=None, folder=False):

    listItem = xbmcgui.ListItem(caption, iconImage=icon, thumbnailImage=thumbnail)
    listItem.setInfo(type="Video", infoLabels={ "Title": caption})
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=link, listitem=listItem, isFolder=folder)

def endListing():

    xbmcplugin.endOfDirectory(int(sys.argv[1]))