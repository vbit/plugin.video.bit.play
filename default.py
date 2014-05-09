
import util, urllib2
import xbmc

def playVideo(params):
    link = WEB_PAGE_BASE + params['link']
    response = urllib2.urlopen(link)
    if response and response.getcode() == 200:
        content = response.read()
        videoLink = util.extract(content, "source src='", "'")
        util.playMedia(params['title'], params['image'], videoLink, 'Video')
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to get video information' % (params['video']))

'''def buildMenu():
	util.addMenuItem('LiveTV', util.makeLinkMenu('/livetv/'), util.makeThumbnail('tv-live.png'), util.makeThumbnail('tv-live.png'), True)
	util.logAddon('debug1')
	util.addMenuItem('ShowTV', util.makeLinkMenu('/the-loai/tvshow'), util.makeThumbnail('tv-show.png'), util.makeThumbnail('tv-show.png'), True)
	util.logAddon('debug2')
	util.addMenuItem('Sport Video', util.makeLinkMenu('/the-loai/sport'), util.makeThumbnail('tv-sport.png'), util.makeThumbnail('tv-sport.png'), True)
	util.logAddon('debug3')
	util.addMenuItem('Music Video', util.makeLinkMenu('/the-loai/music'), util.makeThumbnail('tv-music.png'), util.makeThumbnail('tv-music.png'), True)
	util.logAddon('debug4')
	util.addMenuItem('Collection Video',util.makeLinkMenu('/the-loai/general'), util.makeThumbnail('tv-video.png'), util.makeThumbnail('tv-video.png'), True)
	util.logAddon('debug5')
	util.endListing()
	util.logAddon('debug6')'''

def buildMenu():
    url = 'http://play.fpt.vn/'
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        makeLinks = util.extract(content, '"nav navbar-nav menu"', '</ul>')
        links = util.extractAll(makeLinks,'<li >','a>')
        for link in links:
            params = {'key':'makeMenu'}
            params['link'] = util.extract(link,'href="','\"')
            params['title'] = util.extract(link,'\">','</')
            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, 'DefaultVideo.png', 'DefaultVideo.png', True)
        
        util.endListing()
        xbmc.executebuiltin("Container.SetViewMode(500)")

    else:
        util.showError(ADDON_ID, 'Could not open URL CATEGORIES %s to create menu' %(url))



def buildCategories(inputParams):
    url = WEB_PAGE_BASE + inputParams['link']
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        links = util.extractAll(content, 'idscroll="', '<ul class="thumn">')
        for link in links:
        	if 'tvshow' in inputParams['link']:
        		params = {'key':'makeCategoriesTV'}
        	else:
        		params = {'key':'makeCategories'}
        	params['link'] = util.extract(link,'href="','\"')
        	params['title'] = util.extract(link,'/1">','</a>')
        	link = util.makeLink(params)
        	util.addMenuItem(params['title'], link, 'DefaultVideo.png', 'DefaultVideo.png', True)
        util.endListing()
        xbmc.executebuiltin("Container.SetViewMode(500)")
    else:
    	util.showError(ADDON_ID, 'Could not open URL CATEGORIES %s to create menu' %(url))
            
        
               
        
    

def buildShow(inputParams):
    url = WEB_PAGE_BASE + inputParams['link']
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        links = util.extractAll(content, '<div class="col">', '</span>')
        for link in links:
        	if 'makeCategoriesTV' in inputParams['key']:
        		params = {'key':'makeShows'}
        	else:
        		params = {'key':'makePlay'}
        		util.logAddon('MakePlay')
        	params['title'] = util.extract(link,'data-original-title="','\"')
        	params['link'] = util.extract(link,'href="','\"')
        	params['image'] = util.extract(link,'img src="','"')
        	link = util.makeLink(params)
        	util.addMenuItem(params['title'], link, params['image'], params['image'], True)

        util.endListing()
        xbmc.executebuiltin("Container.SetViewMode(500)")

    else:
    	util.showError(ADDON_ID, 'Could not open URL SHOW %s to create menu' %(url))
            
            
        


def buildPlay(inputParams):
    url = WEB_PAGE_BASE + inputParams['link']
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        links = util.extract(content, 'a href="#">&laquo', 'href="#">&raquo')
        extractLinks = util.extractAll(links,'a href="','"')
        for link in extractLinks:
            params = {'key':'makePlaymakePlay'}
            params['title'] = util.extractTitle(link)
            params['link'] = link
            params['image'] = inputParams['image']

            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, params['image'], params['image'], False)
        util.endListing()
        xbmc.executebuiltin("Container.SetViewMode(500)")

        
    else:
        util.showError(ADDON_ID, 'Could not open URL PLAY %s to create menu' %(url))

WEB_PAGE_BASE = 'http://play.fpt.vn'
ADDON_ID = 'plugin.video.bit.play'

parameters = util.parseParameters()
if 'makePlay' in parameters:
    playVideo(parameters)
elif 'makeShows' in parameters:
    buildPlay(parameters)
elif 'makeCategories' in parameters and 'makeCategoriesTV' in parameters:
    buildShow(parameters)
elif 'makeMenu' in parameters:
    buildCategories(parameters)
else: 
    buildMenu()




    



