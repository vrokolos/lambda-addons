# -*- coding: utf-8 -*-

'''
    Hellenic TV Addon
    Copyright (C) 2014 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


action              = None
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonDesc           = language(30450).encode("utf-8")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
addonIcon           = os.path.join(addonPath,'icon.png')
addonArt            = os.path.join(addonPath,'resources/art')
addonLogos          = os.path.join(addonPath,'resources/logos')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
movieImage          = os.path.join(addonArt,'image_movie.jpg')
tvImage             = os.path.join(addonArt,'image_tv.jpg')
episodeImage        = os.path.join(addonArt,'image_episode.jpg')
musicImage          = os.path.join(addonArt,'image_music.jpg')
addonArchives       = os.path.join(addonPath,'resources/archives.db')
addonChannels       = os.path.join(addonPath,'resources/channels.xml')
addonEPG            = os.path.join(addonPath,'xmltv.xml')
addonSettings       = os.path.join(dataPath,'settings.db')
addonCache          = os.path.join(dataPath,'cache.db')


class main:
    def __init__(self):
        global action
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        channel = urllib.unquote_plus(params["channel"])
        except:     channel = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None


        if action == None:                            root().get()
        elif action == 'container_refresh':           index().container_refresh()
        elif action == 'cache_clear_list':            index().cache_clear_list()
        elif action == 'item_play':                   contextMenu().item_play()
        elif action == 'item_random_play':            contextMenu().item_random_play()
        elif action == 'item_queue':                  contextMenu().item_queue()
        elif action == 'playlist_open':               contextMenu().playlist_open()
        elif action == 'settings_open':               contextMenu().settings_open()
        elif action == 'view_livetv':                 contextMenu().view('livetv')
        elif action == 'view_movies':                 contextMenu().view('movies')
        elif action == 'view_tvshows':                contextMenu().view('tvshows')
        elif action == 'view_episodes':               contextMenu().view('episodes')
        elif action == 'view_cartoons':               contextMenu().view('cartoons')
        elif action == 'favourite_livetv_add':        contextMenu().favourite_add('Live TV', channel, channel, '', '', '', '', '', refresh=True)
        elif action == 'favourite_movie_add':         contextMenu().favourite_add('Movie', url, name, title, year, image, genre, plot, refresh=True)
        elif action == 'favourite_movie_from_search': contextMenu().favourite_add('Movie', url, name, title, year, image, genre, plot)
        elif action == 'favourite_tv_add':            contextMenu().favourite_add('TV Show', url, name, '', '', image, genre, plot, refresh=True)
        elif action == 'favourite_tv_from_search':    contextMenu().favourite_add('TV Show', url, name, '', '', image, genre, plot)
        elif action == 'favourite_cartoons_add':      contextMenu().favourite_add('Cartoons', url, name, title, year, image, genre, plot, refresh=True)
        elif action == 'favourite_delete':            contextMenu().favourite_delete(name, url)
        elif action == 'epg_menu':                    contextMenu().epg(channel)
        elif action == 'root_livetv':                 channels().get()
        elif action == 'root_networks':               root().networks()
        elif action == 'root_shows':                  root().shows()
        elif action == 'root_movies':                 root().movies()
        elif action == 'root_cartoons':               root().cartoons()
        elif action == 'root_favourites':             root().favourites()
        elif action == 'root_news':                   root().news()
        elif action == 'root_sports':                 root().sports()
        elif action == 'root_music':                  root().music()
        elif action == 'livetv_favourites':           favourites().livetv()
        elif action == 'movies_favourites':           favourites().movies()
        elif action == 'shows_favourites':            favourites().shows()
        elif action == 'cartoons_favourites':         favourites().cartoons()
        elif action == 'movies_search':               gm().search(url)
        elif action == 'movies':                      gm().movies(url)
        elif action == 'shows_search':                gm().search_tv(url)
        elif action == 'shows':                       gm().shows(url)
        elif action == 'shows_mega':                  mega().shows()
        elif action == 'shows_ant1':                  ant1().shows()
        elif action == 'shows_alpha':                 alpha().shows()
        elif action == 'shows_star':                  star().shows()
        elif action == 'shows_skai':                  skai().shows()
        elif action == 'shows_alt_mega':              gm().network('mega')
        elif action == 'shows_alt_ant1':              gm().network('ant1')
        elif action == 'shows_alt_alpha':             gm().network('alpha')
        elif action == 'shows_alt_star':              gm().network('star')
        elif action == 'shows_alt_skai':              gm().network('skai')
        elif action == 'shows_etv':                   gm().network('epsilontv')
        elif action == 'shows_nerit':                 gm().network('nerit')
        elif action == 'shows_sigma':                 sigma().shows()
        elif action == 'shows_ant1cy':                gm().network('ant1_cy')
        elif action == 'shows_kontra':                youtube().kontra()
        elif action == 'shows_bluesky':               gm().network('bluesky')
        elif action == 'shows_action24':              gm().network('action24')
        elif action == 'shows_art':                   gm().network('art')
        elif action == 'shows_mtv':                   gm().network('mtvgreece')
        elif action == 'shows_madtv':                 youtube().madtv()
        elif action == 'shows_networks':              gm().networks()
        elif action == 'shows_skai_docs':             skai().docs()
        elif action == 'cartoons_collection':         archives().cartoons()
        elif action == 'cartoons_collection_gr':      archives().cartoons_gr()
        elif action == 'youtube_cartoons_classics':   youtube().cartoons_classics()
        elif action == 'youtube_cartoons_songs':      youtube().cartoons_songs()
        elif action == 'mega_news':                   mega().news()
        elif action == 'ant1_news':                   ant1().news()
        elif action == 'alpha_news':                  alpha().news()
        elif action == 'star_news':                   star().news()
        elif action == 'skai_news':                   skai().news()
        elif action == 'sigma_news':                  sigma().news()
        elif action == 'youtube_enikos':              youtube().enikos()
        elif action == 'mega_sports':                 mega().sports()
        elif action == 'ant1_sports':                 ant1().sports()
        elif action == 'novasports_shows':            novasports().shows()
        elif action == 'novasports_news':             novasports().news()
        elif action == 'dailymotion_superleague':     dailymotion().superleague()
        elif action == 'dailymotion_superball':       dailymotion().superball()
        elif action == 'youtube_madgreekz':           youtube().madgreekz()
        elif action == 'mtvhitlisthellas':            mtvchart().mtvhitlisthellas()
        elif action == 'rythmoshitlist':              rythmoschart().rythmoshitlist()
        elif action == 'mtvdancefloor':               mtvchart().mtvdancefloor()
        elif action == 'eurotop20':                   mtvchart().eurotop20()
        elif action == 'usatop20':                    mtvchart().usatop20()
        elif action == 'episodes_reverse':            episodes().get(name, url, image, genre, plot, show, reverse=True)
        elif action == 'episodes':                    episodes().get(name, url, image, genre, plot, show)
        elif action == 'play_live':                   resolver().live(channel)
        elif action == 'play':                        resolver().run(url)

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def run(self, url):
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    def live(self, name, epg, url):
        name = re.sub('\s[(]\d{1}[)]$','', name)

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        image = '%s/%s.png' % (addonLogos, name)
        if not xbmcvfs.exists(image): image = '%s/na.png' % addonLogos

        if not xbmc.getInfoLabel('listItem.plot') == '' : epg = xbmc.getInfoLabel('listItem.plot')
        title = epg.split('\n')[0].split('-', 1)[-1].rsplit('[', 1)[0].strip()

        meta = {'title': title, 'tvshowtitle': name, 'studio': name, 'premiered': date, 'director': name, 'writer': name, 'plot': epg, 'genre': 'Live TV', 'duration': '1440'}

        item = xbmcgui.ListItem(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type="Video", infoLabels = meta )

        xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
        xbmc.Player().play(url, item)

    def onPlayBackStarted(self):
        return

    def onPlayBackEnded(self):
        return

    def onPlayBackStopped(self):
        return

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin('Container.Refresh')

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            record = (skin, content)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            view = dbcur.fetchone()
            view = view[2]
            if view == None: raise Exception()
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def cache(self, function, timeout, *args):
        try:
            response = None

            f = repr(function)
            f = re.sub('.+\smethod\s|.+function\s|\sat\s.+|\sof\s.+', '', f)

            import hashlib
            a = hashlib.md5()
            for i in args: a.update(str(i))
            a = str(a.hexdigest())
        except:
            pass

        try:
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM rel_list WHERE func = '%s' AND args = '%s'" % (f, a))
            match = dbcur.fetchone()

            response = eval(match[2].encode('utf-8'))

            t1 = int(re.sub('[^0-9]', '', str(match[3])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) >= int(timeout*60)
            if update == False:
                return response
        except:
            pass

        try:
            r = function(*args)
            if (r == None or r == []) and not response == None:
                return response
            elif (r == None or r == []):
                return r
        except:
            return

        try:
            r = repr(r)
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_list (""func TEXT, ""args TEXT, ""response TEXT, ""added TEXT, ""UNIQUE(func, args)"");")
            dbcur.execute("DELETE FROM rel_list WHERE func = '%s' AND args = '%s'" % (f, a))
            dbcur.execute("INSERT INTO rel_list Values (?, ?, ?, ?)", (f, a, r, t))
            dbcon.commit()
        except:
            pass

        try:
            return eval(r.encode('utf-8'))
        except:
            pass

    def cache_clear_list(self):
        try:
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_list")
            dbcur.execute("VACUUM")
            dbcon.commit()

            index().infoDialog(language(30305).encode("utf-8"))
        except:
            pass

    def rootList(self, rootList):
        if rootList == None or len(rootList) == 0: return

        total = len(rootList)
        for i in rootList:
            try:
                try: name = language(i['name']).encode("utf-8")
                except: name = i['name']

                image = '%s/%s' % (addonArt, i['image'])

                root = i['action']
                u = '%s?action=%s' % (sys.argv[0], root)
                try: u += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                if u == '': raise Exception()

                cm = []
                if root.startswith('movies') or root.startswith('episodes') or root.startswith('cartoons'):
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo(type="Video", infoLabels={"title": name, "plot": addonDesc})
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def channelList(self, channelList):
        if channelList == None or len(channelList) == 0: return

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Live TV'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(channelList)
        for i in channelList:
            try:
                name, epg = i['name'], i['epg']

                fanart = addonFanart

                meta = {'title': name, 'tvshowtitle': name, 'studio': name, 'premiered': date, 'director': name, 'writer': name, 'plot': epg, 'genre': 'Live TV', 'duration': '1440'}

                sysname, sysurl = urllib.quote_plus(name), urllib.quote_plus(name.replace(' ','_'))

                u = '%s?action=play_live&channel=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=epg_menu&channel=%s)' % (sys.argv[0], sysname)))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=container_refresh)' % (sys.argv[0])))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=view_livetv)' % (sys.argv[0])))
                if not name in favourites: cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=favourite_livetv_add&channel=%s)' % (sys.argv[0], sysname)))
                else: cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysname)))

                item = xbmcgui.ListItem(name, iconImage=fanart, thumbnailImage=fanart)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('livetv', {'skin.confluence' : 504})
            xbmc.sleep(100)

    def movieList(self, movieList):
        if movieList == None or len(movieList) == 0: return

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Movie'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(movieList)
        for i in movieList:
            try:
                name, url, image, title, year, genre, plot = i['name'], i['url'], i['image'], i['title'], i['year'], i['genre'], i['plot']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'title': title, 'year': year, 'genre' : genre, 'plot': plot}

                sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(genre), urllib.quote_plus(plot)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = movieImage
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=play&url=%s&name=%s' % (sys.argv[0], sysurl, sysname)

                cm = []
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                if action == 'movies_favourites':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_from_search&name=%s&url=%s&image=%s&title=%s&year=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot)))
                else:
                    if not url in favourites: cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_add&name=%s&url=%s&image=%s&title=%s&year=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot)))
                    else: cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                if not action == 'movies':
                    cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(movies)'):
                return index().container_view('movies', {'skin.confluence' : 50})
            xbmc.sleep(100)

    def cartoonList(self, cartoonList):
        if cartoonList == None or len(cartoonList) == 0: return

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Cartoons'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(cartoonList)
        for i in cartoonList:
            try:
                name, url, image, title, year, genre, plot = i['name'], i['url'], i['image'], i['title'], i['year'], i['genre'], i['plot']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'title': title, 'year': year, 'genre' : genre, 'plot': plot}

                sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(genre), urllib.quote_plus(plot)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = movieImage
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                if i['type'] == 'movie':
                    u = '%s?action=play&url=%s&name=%s' % (sys.argv[0], sysurl, sysname)
                    isFolder = False
                else:
                    u = '%s?action=episodes&name=%s&url=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot, sysname)
                    isFolder = True

                cm = []
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                if action == 'cartoons_favourites':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                else:
                    if not url in favourites: cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_cartoons_add&name=%s&url=%s&image=%s&title=%s&year=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot)))
                    else: cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                if not action == 'movies':
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=view_cartoons)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(movies)'):
                return index().container_view('cartoons', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def showList(self, showList):
        if showList == None or len(showList) == 0: return

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(showList)
        for i in showList:
            try:
                name, url, image, genre, plot = i['name'], i['url'], i['image'], i['genre'], i['plot']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'title': name, 'tvshowtitle': name, 'genre' : genre, 'plot': plot}

                sysname, sysurl, sysimage, sysgenre, sysplot, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(name)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = tvImage
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                if action == 'shows' or action == 'shows_favourites':
                    u = '%s?action=episodes_reverse&name=%s&url=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot, sysshow)
                else:
                    u = '%s?action=episodes&name=%s&url=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot, sysshow)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                if action == 'shows_favourites':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'shows_search':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_from_search&name=%s&url=%s&image=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot)))
                elif action == 'shows':
                    if not url in favourites: cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&name=%s&url=%s&image=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot)))
                    else: cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))

                cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(tvshows)'):
                return index().container_view('tvshows', {'skin.confluence' : 50})
            xbmc.sleep(100)

    def episodeList(self, episodeList):
        if episodeList == None or len(episodeList) == 0: return

        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, date, genre, plot, title, show = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'title': title, 'studio': show, 'premiered': date, 'genre': genre, 'plot': plot}

                sysurl = urllib.quote_plus(url)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = episodeImage
                if show == '0': meta.update({'studio': addonName})
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('episodes', {'skin.confluence' : 50})
            xbmc.sleep(100)

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self, id=addonId):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label == None): break
            record = (skin, content, str(view))
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS views (""skin TEXT, ""view_type TEXT, ""view_id TEXT, ""UNIQUE(skin, view_type)"");")
            dbcur.execute("DELETE FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO views Values (?, ?, ?)", record)
            dbcon.commit()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, type, url, name, title, year, image, genre, plot, refresh=False):
        try:
            record = (url, type, repr(name), repr(title), repr(year), repr(image), repr(genre), repr(plot))

            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS favourites (""url TEXT, ""video_type TEXT, ""name TEXT, ""title TEXT, ""year TEXT, ""image TEXT, ""genre TEXT, ""plot TEXT, ""UNIQUE(url)"");")
            dbcur.execute("DELETE FROM favourites WHERE url = '%s'" % (record[0]))
            dbcur.execute("INSERT INTO favourites Values (?, ?, ?, ?, ?, ?, ?, ?)", record)
            dbcon.commit()

            if refresh == True: index().container_refresh()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, name, url):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM favourites WHERE url = '%s'" % url)
            dbcon.commit()

            index().container_refresh()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def epg(self, channel):
        try:
            epgList = []
            channel = re.sub('\s[(]\d{1}[)]$','', channel)

            now = datetime.datetime.now()
            now = '%04d' % now.year + '%02d' % now.month + '%02d' % now.day + '%02d' % now.hour + '%02d' % now.minute + '%02d' % now.second

            file = xbmcvfs.File(addonEPG)
            result = file.read()
            file.close()

            programmes = re.compile('(<programme.+?</programme>)').findall(result)
        except:
            return
        for programme in programmes:
            try:
                match = common.parseDOM(programme, "programme", ret="channel")[0]
                if not channel == match: raise Exception()

                start = common.parseDOM(programme, "programme", ret="start")[0]
                start = re.split('\s+', start)[0]
                stop = common.parseDOM(programme, "programme", ret="stop")[0]
                stop = re.split('\s+', stop)[0]
                if not (int(start) <= int(now) <= int(stop) or int(start) >= int(now)): raise Exception()

                start = datetime.datetime(*time.strptime(start, "%Y%m%d%H%M%S")[:6])
                title = common.parseDOM(programme, "title")[0]
                title = common.replaceHTMLCodes(title)
                if channel == title : title = 'ÌÇ ÄÉÁÈÅÓÉÌÏ ÐÑÏÃÑÁÌÌÁ'.decode('iso-8859-7')
                epg = "%s    %s" % (str(start), title)
                epgList.append(epg)
            except:
                pass

        select = index().selectDialog(epgList, header='%s - %s' % (language(30351).encode("utf-8"), channel))
        return


class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'root_livetv.jpg', 'action': 'root_livetv'})
        rootList.append({'name': 30502, 'image': 'root_networks.jpg', 'action': 'root_networks'})
        rootList.append({'name': 30503, 'image': 'root_shows.jpg', 'action': 'root_shows'})
        rootList.append({'name': 30504, 'image': 'root_movies.jpg', 'action': 'root_movies'})
        rootList.append({'name': 30505, 'image': 'root_cartoons.jpg', 'action': 'root_cartoons'})
        rootList.append({'name': 30506, 'image': 'root_docs.jpg', 'action': 'shows_skai_docs'})
        rootList.append({'name': 30507, 'image': 'root_favourites.jpg', 'action': 'root_favourites'})
        rootList.append({'name': 30508, 'image': 'root_news.jpg', 'action': 'root_news'})
        rootList.append({'name': 30509, 'image': 'root_sports.jpg', 'action': 'root_sports'})
        rootList.append({'name': 30510, 'image': 'root_music.jpg', 'action': 'root_music'})
        index().rootList(rootList)

    def networks(self):
        rootList = []

        root = 'shows_mega'
        if getSetting("shows_mega") == '1': root = 'shows_alt_mega'
        rootList.append({'name': 'MEGA', 'image': 'logos_mega.jpg', 'action': root})

        root = 'shows_ant1'
        if getSetting("shows_ant1") == '1': root = 'shows_alt_ant1'
        rootList.append({'name': 'ANT1', 'image': 'logos_ant1.jpg', 'action': root})

        root = 'shows_alpha'
        if getSetting("shows_alpha") == '1': root = 'shows_alt_alpha'
        rootList.append({'name': 'ALPHA', 'image': 'logos_alpha.jpg', 'action': root})

        root = 'shows_star'
        if getSetting("shows_star") == '1': root = 'shows_alt_star'
        rootList.append({'name': 'STAR', 'image': 'logos_star.jpg', 'action': root})

        root = 'shows_skai'
        if getSetting("shows_skai") == '1': root = 'shows_alt_skai'
        rootList.append({'name': 'SKAI', 'image': 'logos_skai.jpg', 'action': root})

        rootList.append({'name': 'E TV', 'image': 'logos_etv.jpg', 'action': 'shows_etv'})
        rootList.append({'name': 'NERIT', 'image': 'logos_nerit.jpg', 'action': 'shows_nerit'})
        rootList.append({'name': 'SIGMA', 'image': 'logos_sigma.jpg', 'action': 'shows_sigma'})
        rootList.append({'name': 'ANT1 CY', 'image': 'logos_ant1cy.jpg', 'action': 'shows_ant1cy'})
        rootList.append({'name': 'KONTRA', 'image': 'logos_kontra.jpg', 'action': 'shows_kontra'})
        rootList.append({'name': 'BLUE SKY', 'image': 'logos_bluesky.jpg', 'action': 'shows_bluesky'})
        rootList.append({'name': 'ACTION 24', 'image': 'logos_action24.jpg', 'action': 'shows_action24'})
        rootList.append({'name': 'ART TV', 'image': 'logos_art.jpg', 'action': 'shows_art'})
        rootList.append({'name': 'MTV', 'image': 'logos_mtv.jpg', 'action': 'shows_mtv'})
        rootList.append({'name': 'MAD TV', 'image': 'logos_madtv.jpg', 'action': 'shows_madtv'})
        rootList.append({'name': 30521, 'image': 'shows_networks.jpg', 'action': 'shows_networks'})
        index().rootList(rootList)

    def shows(self):
        rootList = []
        rootList.append({'name': 30531, 'image': 'shows_search.jpg', 'action': 'shows_search'})
        rootList.append({'name': 30532, 'image': 'shows_favourites.jpg', 'action': 'shows_favourites'})
        try:
            titles = gm().showtitles()
            for i in range(0, len(titles)): titles[i].update({'image': 'years_movies.jpg', 'action': 'movies'})
            rootList += titles
        except:
            pass
        index().rootList(rootList)

    def movies(self):
        rootList = []
        rootList.append({'name': 30541, 'image': 'movies_search.jpg', 'action': 'movies_search'})
        rootList.append({'name': 30542, 'image': 'movies_favourites.jpg', 'action': 'movies_favourites'})
        try:
            years = gm().movieyears()
            for i in range(0, len(years)): years[i].update({'image': 'years_movies.jpg', 'action': 'movies'})
            rootList += years
        except:
            pass
        index().rootList(rootList)

    def cartoons(self):
        rootList = []
        rootList.append({'name': 30551, 'image': 'cartoons_favourites.jpg', 'action': 'cartoons_favourites'})
        rootList.append({'name': 30552, 'image': 'cartoons_collection.jpg', 'action': 'cartoons_collection'})
        rootList.append({'name': 30553, 'image': 'cartoons_collection_gr.jpg', 'action': 'cartoons_collection_gr'})
        rootList.append({'name': 30554, 'image': 'cartoons_classics.jpg', 'action': 'youtube_cartoons_classics'})
        rootList.append({'name': 30555, 'image': 'cartoons_songs.jpg', 'action': 'youtube_cartoons_songs'})
        index().rootList(rootList)

    def favourites(self):
        rootList = []
        rootList.append({'name': 30561, 'image': 'livetv_favourites.jpg', 'action': 'livetv_favourites'})
        rootList.append({'name': 30562, 'image': 'shows_favourites.jpg', 'action': 'shows_favourites'})
        rootList.append({'name': 30563, 'image': 'movies_favourites.jpg', 'action': 'movies_favourites'})
        rootList.append({'name': 30564, 'image': 'cartoons_favourites.jpg', 'action': 'cartoons_favourites'})
        index().rootList(rootList)

    def news(self):
        rootList = []
        rootList.append({'name': 'MEGA', 'image': 'logos_mega.jpg', 'action': 'mega_news'})
        rootList.append({'name': 'ANT1', 'image': 'logos_ant1.jpg', 'action': 'ant1_news'})
        rootList.append({'name': 'ALPHA', 'image': 'logos_alpha.jpg', 'action': 'alpha_news'})
        rootList.append({'name': 'STAR', 'image': 'logos_star.jpg', 'action': 'star_news'})
        rootList.append({'name': 'SKAI', 'image': 'logos_skai.jpg', 'action': 'skai_news'})
        rootList.append({'name': 'SIGMA', 'image': 'logos_sigma.jpg', 'action': 'sigma_news'})
        rootList.append({'name': 'ENIKOS', 'image': 'logos_enikos.jpg', 'action': 'youtube_enikos'})
        index().rootList(rootList)

    def sports(self):
        rootList = []
        rootList.append({'name': 'MEGA', 'image': 'logos_mega.jpg', 'action': 'mega_sports'})
        rootList.append({'name': 'ANT1', 'image': 'logos_ant1.jpg', 'action': 'ant1_sports'})
        rootList.append({'name': 'Novasports', 'image': 'logos_novasports.jpg', 'action': 'novasports_shows'})
        rootList.append({'name': 'Novasports News', 'image': 'logos_novasports_news.jpg', 'action': 'novasports_news'})
        rootList.append({'name': 'Super League', 'image': 'logos_superleague.jpg', 'action': 'dailymotion_superleague'})
        rootList.append({'name': 'SuperBALL', 'image': 'logos_superball.jpg', 'action': 'dailymotion_superball'})
        index().rootList(rootList)

    def music(self):
        rootList = []
        rootList.append({'name': 'MAD Greekz', 'image': 'logos_madgreekz.jpg', 'action': 'youtube_madgreekz'})
        rootList.append({'name': 'MTV Hit List Hellas', 'image': 'logos_mtvhits.jpg', 'action': 'mtvhitlisthellas'})
        rootList.append({'name': 'Rythmos Hit List', 'image': 'logos_rythmos.jpg', 'action': 'rythmoshitlist'})
        rootList.append({'name': 'MTV Dance Floor', 'image': 'logos_mtvdance.jpg', 'action': 'mtvdancefloor'})
        rootList.append({'name': 'Euro Top 20', 'image': 'logos_europe.jpg', 'action': 'eurotop20'})
        rootList.append({'name': 'U.S. Top 20', 'image': 'logos_usa.jpg', 'action': 'usatop20'})
        index().rootList(rootList)


class favourites:
    def __init__(self):
        self.list = []

    def livetv(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Live TV'")
            match = dbcur.fetchall()
            match = [(i[0]) for i in match]

            self.list = channels().channel_list()
            self.list = [i for i in self.list if i['name'] in match]
            self.list = sorted(self.list, key=itemgetter('name'))

            index().channelList(self.list)
        except:
            return

    def shows(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[5], i[6], i[7]) for i in match]

            for url, name, image, genre, plot in match:
                try:
                    name, image, genre, plot = eval(name.encode('utf-8')), eval(image.encode('utf-8')), eval(genre.encode('utf-8')), eval(plot.encode('utf-8'))

                    self.list.append({'name': name, 'url': url, 'image': image, 'genre': genre, 'plot': plot})
                except:
                    pass

            self.list = sorted(self.list, key=itemgetter('name'))
            index().showList(self.list)
        except:
            return

    def movies(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Movie'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[3], i[4], i[5], i[6], i[7]) for i in match]

            for url, name, title, year, image, genre, plot in match:
                try:
                    name, title, year, image, genre, plot = eval(name.encode('utf-8')), eval(title.encode('utf-8')), eval(year.encode('utf-8')), eval(image.encode('utf-8')), eval(genre.encode('utf-8')), eval(plot.encode('utf-8'))

                    self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'genre': genre, 'plot': plot})
                except:
                    pass

            self.list = sorted(self.list, key=itemgetter('title'))
            index().movieList(self.list)
        except:
            return

    def cartoons(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Cartoons'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[3], i[4], i[5], i[6], i[7]) for i in match]

            a = [i[0] for i in match if i[0].startswith('archives_')]
            a = [re.compile('archives_.+?_(\d*)_\d*').findall(i)[0] for i in a]

            self.list = archives().arc_list('cartoons_collection')
            self.list = [i for i in self.list if i['imdb'] in a]

            b = [i for i in match if not i[0].startswith('archives_')]
            for url, name, title, year, image, genre, plot in b:
                try:
                    name, title, year, image, genre, plot = eval(name.encode('utf-8')), eval(title.encode('utf-8')), eval(year.encode('utf-8')), eval(image.encode('utf-8')), eval(genre.encode('utf-8')), eval(plot.encode('utf-8'))

                    self.list.append({'name': name, 'url': url, 'image': image, 'fanart': '0', 'title': title, 'year': year, 'genre': genre, 'plot': plot, 'lang': 'el', 'type': 'tvshow'})
                except:
                    pass

            self.list = sorted(self.list, key=itemgetter('title'))
            index().cartoonList(self.list)
        except:
            return

class channels:
    def __init__(self):
        self.list = []
        self.epg = {}
        if not (xbmcvfs.exists(addonEPG) and index().getProperty("htv_Service_Running") == ''):
            index().infoDialog(language(30306).encode("utf-8"))

    def get(self):
        self.list = self.channel_list()
        index().channelList(self.list)

    def channel_list(self):
        try:
            self.epg_list()

            file = xbmcvfs.File(addonChannels)
            result = file.read()
            file.close()

            channels = common.parseDOM(result, "channel", attrs = { "active": "True" })
        except:
            return

        for channel in channels:
            try:
                name = common.parseDOM(channel, "name")[0]

                try: type = common.parseDOM(channel, "type")[0]
                except: type = ''

                url = common.parseDOM(channel, "url")[0]
                url = common.replaceHTMLCodes(url)

                n = re.sub('\s[(]\d{1}[)]$','', name)
                epg = '[B][ÔÙÑÁ] - %s[/B]\nÄåí õðÜñ÷ïõí ðëçñïöïñßåò.'.decode('iso-8859-7') % n.upper()
                try: epg = self.epg[n]
                except: pass
                epg = common.replaceHTMLCodes(epg)

                self.list.append({'name': name, 'epg': epg, 'url': url, 'type': type})
            except:
                pass

        return self.list

    def epg_list(self):
        try:
            now = datetime.datetime.now()
            now = '%04d' % now.year + '%02d' % now.month + '%02d' % now.day + '%02d' % now.hour + '%02d' % now.minute + '%02d' % now.second

            file = open(addonEPG,'r')
            read = file.read()
            file.close()
            programmes = re.compile('(<programme.+?</programme>)').findall(read)
        except:
            return

        for programme in programmes:
            try:
                start = re.compile('start="(.+?)"').findall(programme)[0]
                start = re.split('\s+', start)[0]

                stop = re.compile('stop="(.+?)"').findall(programme)[0]
                stop = re.split('\s+', stop)[0]
                if not int(start) <= int(now) <= int(stop): raise Exception()

                channel = common.parseDOM(programme, "programme", ret="channel")[0]

                title = common.parseDOM(programme, "title")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                desc = common.parseDOM(programme, "desc")[0]
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                epg = "[B][%s] - %s[/B]\n%s" % ('ÔÙÑÁ'.decode('iso-8859-7').encode('utf-8'), title, desc)

                self.epg.update({channel: epg})
            except:
                pass

class archives:
    def __init__(self):
        self.list = []

    def cartoons(self):
        self.list = self.arc_list('cartoons_collection')
        index().cartoonList(self.list)

    def cartoons_gr(self):
        self.list = self.arc_list('cartoons_collection')
        try: self.list = [i for i in self.list if i['lang'] == 'el']
        except: return
        index().cartoonList(self.list)

    def arc_list(self, arc):
        try:
            dbcon = database.connect(addonArchives)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM arc_list WHERE arc = '%s'" % arc)
            match = dbcur.fetchone()
            archives = eval(match[1].encode('utf-8'))
        except:
            pass

        for i in archives:
            try:
                title = i['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = i['year']
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = 'archives_%s_%s_0' % (arc, i['imdb'])
                url = url.encode('utf-8')

                image = i['image']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try: fanart = i['fanart']
                except: fanart = '0'
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                try: genre = i['genre']
                except: genre = 'Greek'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: plot = i['plot']
                except: plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                try: imdb = i['imdb']
                except: imdb = '0'
                imdb = common.replaceHTMLCodes(imdb)
                imdb = imdb.encode('utf-8')

                try: lang = i['language']
                except: lang = '0'
                lang = lang.encode('utf-8')

                try: type = i['type']
                except: type = '0'
                type = type.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'fanart': fanart, 'title': title, 'year': year, 'genre': genre, 'plot': plot, 'imdb': imdb, 'lang': lang, 'type': type})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            arc, imdb = re.compile('archives_(.+?)_(\d*)_\d*').findall(url)[0]

            dbcon = database.connect(addonArchives)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM arc_list WHERE arc = '%s'" % arc)
            match = dbcur.fetchone()

            u = eval(match[1].encode('utf-8'))
            i = [i for i in u if i['imdb'] == imdb][0]

            show = i['title']
            show = common.replaceHTMLCodes(show)
            show = show.encode('utf-8')

            image = i['image']
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')

            try: fanart = i['fanart']
            except: fanart = '0'
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

            try: genre = i['genre']
            except: genre = 'Greek'
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            try: plot = i['plot']
            except: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            episodes = i['link']
        except:
            return

        for i in range(0, len(episodes)):
            try:
                name = 'Åðåéóüäéï '.decode('iso-8859-7') + str(i+1)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = 'archives_%s_%s_%s' % (arc, imdb, str(i))
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'fanart': fanart, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            arc, imdb, idx = re.compile('archives_(.+?)_(\d*)_(\d*)').findall(url)[0]

            dbcon = database.connect(addonArchives)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM arc_list WHERE arc = '%s'" % arc)
            match = dbcur.fetchone()

            link = eval(match[1].encode('utf-8'))
            link = [i for i in link if i['imdb'] == imdb][0]

            size = link['link'][int(idx)]['size']

            url = link['link'][int(idx)]['url']
            url = resolver().sources_resolve(url)

            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
            response = urllib2.urlopen(request, timeout=10)
            s = response.info()["Content-Length"]

            if not s == size: raise Exception()
            return url
        except:
            return

class episodes:
    def get(self, name, url, image, genre, plot, show, reverse=False):
        if url.startswith('archives_'):
            self.list = archives().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(gm().base_link):
            self.list = gm().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(mega().feed_link):
            self.list = mega().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(mega().base_link):
            self.list = mega().episodes_list2(name, url, image, genre, plot, show)
        elif url.startswith(ant1().base_link):
            self.list = ant1().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(alpha().base_link):
            self.list = alpha().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(star().base_link):
            self.list = star().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(skai().base_link):
            self.list = skai().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(sigma().base_link):
            self.list = sigma().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(novasports().base_link):
            self.list = novasports().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(mtvchart().base_link):
            self.list = mtvchart().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(rythmoschart().base_link):
            self.list = rythmoschart().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(dailymotion().api_link):
            self.list = dailymotion().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(youtube().api_link):
            self.list = youtube().episodes_list(name, url, image, genre, plot, show)

        if reverse == True:
            try: self.list = self.list[::-1]
            except: pass
        index().episodeList(self.list)

class resolver:
    def run(self, url):
        try:
            url = self.sources_resolve(url)
            if url is None: raise Exception()

            player().run(url)
            return url
        except:
            index().infoDialog(language(30307).encode("utf-8"))
            return

    def live(self, channel):
        try:
            ch = channel.replace('_',' ')
            data = channels().channel_list()

            i = [i for i in data if ch == i['name']][0]
            name, epg, url, type = i['name'], i['epg'], i['url'], i['type']

            dialog = xbmcgui.DialogProgress()
            dialog.create(addonName.encode("utf-8"), language(30341).encode("utf-8"))
            dialog.update(0)

            try: url = getattr(livestream(), type)(url)
            except: pass
            if url is None: raise Exception()

            dialog.close()

            player().live(name, epg, url)
            return url
        except:
            index().infoDialog(language(30307).encode("utf-8"))
            return

    def sources_resolve(self, url):
        try:
            import commonresolvers
            if url.startswith('archives_'): url = archives().resolve(url)

            elif url.startswith(gm().base_link): url = gm().resolve(url)
            elif url.startswith(mega().base_link): url = mega().resolve(url)
            elif url.startswith(ant1().base_link): url = ant1().resolve(url)
            elif url.startswith(alpha().base_link): url = alpha().resolve(url)
            elif url.startswith(skai().base_link): url = skai().resolve(url)
            elif url.startswith(sigma().base_link): url = sigma().resolve(url)
            elif url.startswith(nerit().base_link): url = nerit().resolve(url)
            elif url.startswith(ant1cy().base_link): url = ant1cy().resolve(url)
            elif url.startswith(ant1cy().old_link): url = ant1cy().resolve(url)
            elif url.startswith(megacy().base_link): url = megacy().resolve(url)
            elif url.startswith(novasports().base_link): url = novasports().resolve(url)
            elif url.startswith(dailymotion().base_link): url = dailymotion().resolve(url)
            elif url.startswith(youtube().search_link): url = youtube().resolve_search(url)
            elif url.startswith(youtube().base_link): url = youtube().resolve(url)

            elif 'vimeo.com' in url: url = commonresolvers.vimeo(url)
            elif 'streamin.to' in url: url = commonresolvers.streamin(url)
            elif 'datemule.com' in url: url = commonresolvers.datemule(url)

            return url
        except:
            return



class gm:
    def __init__(self):
        self.list = []
        self.base_link = 'http://greek-movies.com'
        self.movies_link = 'http://greek-movies.com/movies.php?'
        self.shows_link = 'http://greek-movies.com/shows.php?'
        self.series_link = 'http://greek-movies.com/series.php?'
        self.episode_link = 'http://greek-movies.com/retrieve_data.php?type=episode&epid=%s&view=%s'

    def movieyears(self):
        try:
            self.list = index().cache(self.titles_list, 24, self.movies_link)
            self.list = [i for i in self.list if i['url'].startswith('y=')]
            return self.list
        except:
            pass

    def showtitles(self):
        try:
            self.list = index().cache(self.titles_list, 24, self.shows_link)
            self.list = [i for i in self.list if i['url'].startswith('l=')]
            return self.list
        except:
            pass

    def search(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30361).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.list = self.search_list('movie', self.query)
            index().movieList(self.list)

    def search_tv(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30361).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.list = self.search_list('tv', self.query)
            index().showList(self.list)

    def movies(self, url):
        self.list = index().cache(self.movies_list, 24, url)
        index().movieList(self.list)

    def shows(self, url):
        self.list = index().cache(self.shows_list, 24, url)
        index().showList(self.list)

    def networks(self):
        networks = ['mega', 'ant1', 'alpha', 'star', 'skai', 'nerit', 'epsilontv', 'kontrachannel', 'bluesky', 'action24', 'art', 'sigmatv', 'ant1_cy', 'mtvgreece', 'madtv']
        self.list = index().cache(self.shows_list, 24, 'y=1')
        try: self.list = [i for i in self.list if i['network'] in networks]
        except: return
        index().showList(self.list)

    def network(self, limit):
        self.list = index().cache(self.shows_list, 24, 'y=1')
        try: self.list = [i for i in self.list if i['network'] == limit]
        except: return
        index().showList(self.list)

    def titles_list(self, url):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "select", attrs = { "onChange": ".+?" })
            result = ''.join(result)

            titles = re.compile('(<option.+?</option>)').findall(result)
        except:
            return

        for title in titles:
            try:
                name = common.parseDOM(title, "p", attrs = { "class": ".+?" })[0]
                name = name[0].capitalize() + name[1:]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(title, "option", ret="value")[0]
                url = url.split('?')[-1]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def search_list(self, content, url):
        try:
            query = urllib.quote_plus(url)
            query = 'https://encrypted.google.com/search?as_q=%s&as_sitesearch=greek-movies.com' % query

            result = getUrl(query).result

            if content == 'movie':
                result = re.compile('greek-movies.com/(movies.php[?]m=\d*)').findall(result)
            elif content == 'tv':
                result = re.compile('greek-movies.com/(shows.php[?]s=\d*|series.php[?]s=\d*)').findall(result)
            result = uniqueList(result).list

            for i in result:
                self.list.append({'name': '0', 'url': '%s/%s' % (self.base_link, i), 'image': '0', 'title': '0', 'year': '0', 'genre': 'Greek', 'plot': '0'})
        except:
            return self.list

        threads = []
        if content == 'movie':
            for i in range(0, len(self.list)): threads.append(Thread(self.movies_info, i))
        elif content == 'tv':
            for i in range(0, len(self.list)): threads.append(Thread(self.shows_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['name'] == '0']

        return self.list

    def movies_info(self, i):
        try:
            result = getUrl(self.list[i]['url']).result
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]

            title = common.parseDOM(result, "p", attrs = { "class": "movieheading2" })[0]
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'title': title})

            year = common.parseDOM(result, "p", attrs = { "class": "movieheading3" })[0]
            year = re.sub('[^0-9]', '', year.encode('utf-8'))
            if not year == '0': self.list[i].update({'year': year})

            name = '%s (%s)' % (title, year)
            try: name = name.encode('utf-8')
            except: pass
            if not title == '0': self.list[i].update({'name': name})

            image = common.parseDOM(result, "img", ret="src")[0]
            image = '%s/%s' % (self.base_link, image)
            if image.endswith('icon/film.jpg'): image = '0'
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            if not image == '0': self.list[i].update({'image': image})
        except:
            pass

    def shows_info(self, i):
        try:
            result = getUrl(self.list[i]['url']).result
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]

            title = common.parseDOM(result, "p", attrs = { "class": "seriesheading2" })[0]
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'name': title, 'title': title})

            image = common.parseDOM(result, "img", ret="src")[0]
            image = '%s/%s' % (self.base_link, image)
            if image.endswith('icon/film.jpg'): image = '0'
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            if not image == '0': self.list[i].update({'image': image})
        except:
            pass

    def movies_list(self, url):
        try:
            result = getUrl(self.movies_link + url).result
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })

            movies = common.parseDOM(result, "td")
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "p")[0]
                title = re.compile('(.+?) [(]\d{4}[)]$').findall(title)[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "p")[0]
                year = re.compile('.+? [(](\d{4})[)]$').findall(year)[0]
                year = common.replaceHTMLCodes(year)
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s/%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(movie, "IMG", ret="SRC")[0]
                image = '%s/%s' % (self.base_link, image)
                if image.endswith('icon/film.jpg'): image = '0'
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        return self.list

    def shows_list(self, url):
        try:
            self.result = []
            self.result2 = []

            def thread(url):
                try: self.result.append(getUrl(url).result)
                except: pass
            def thread2(url):
                try: self.result2.append(getUrl(url).result)
                except: pass

            threads = []
            threads.append(Thread(thread, self.series_link + url))
            threads.append(Thread(thread2, self.shows_link + url))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.result == [] or self.result2 == []: return
            result = ''.join(self.result) + ''.join(self.result2)
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })

            shows = common.parseDOM(result, "td")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "p")[0]
                name = re.compile('(.+?) [(].+?[)]$').findall(name)[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s/%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "IMG", ret="SRC")[0]
                image = '%s/%s' % (self.base_link, image)
                if image.endswith('icon/film.jpg'): image = '0'
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                network = common.parseDOM(show, "IMG", ret="SRC")[1]
                network = network.split("/")[-1].split('.')[0]
                network = common.replaceHTMLCodes(network)
                network = network.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'network': network, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]

            sort_dict = {'ce99ceb1cebd':'01', 'cea6ceb5ceb2':'02', 'ce9cceaccf81':'03', 'ce91cf80cf81':'04', 'ce9cceacceb9':'05', 'ce99cebfcf8dcebd':'06', 'ce99cebfcf8dcebb':'07', 'ce91cf8dceb3':'08', 'cea3ceb5cf80':'09', 'ce9fcebacf84':'10', 'ce9dcebfcead':'11', 'ce94ceb5ceba':'12'}
            sort_date = common.parseDOM(result, "div", attrs = { "class": "year_container_new" })

            episodes = common.parseDOM(result, "div", attrs = { "class": "episodemenu_new" })
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a", attrs = { "class": "episodetitle" })[0]

                if not len(sort_date) == 0:
                    r = result.split(episode)[0]
                    y = common.parseDOM(r, "div", attrs = { "class": "year_container_new" })[-1]
                    m = common.parseDOM(r, "div", attrs = { "class": "month_container_new" })[-1]
                    m = common.parseDOM(m, "div", attrs = { "class": "left_element_new" })[0]
                    m = repr(m.encode('utf-8')).replace('\\x', '').replace('\'', '')
                    m = sort_dict[m]
                    name = '%04d-%02d-%02d' % (int(y), int(m), int(name))

                name = 'Åðåéóüäéï '.decode('iso-8859-7') + name
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="onclick")[0]
                url = re.compile("'(.+?)'").findall(url)
                url = self.episode_link % (url[0], url[1])
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            host_order = ['youtube', 'dailymotion', 'datemule', 'streamin', 'megatv', 'antenna', 'alphatv', 'skai', 'sigmatv', 'nerit', 'ant1iwo', 'livenews']

            if url.startswith(self.movies_link):
                result = getUrl(url).result
                result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]
                result = common.parseDOM(result, "tr",)[-1]
                result = common.parseDOM(result, "p")
                result = uniqueList(result).list
            else:
                u = url.split('?')
                result = getUrl(u[0], post=u[1]).result
                result = re.compile('(<a.+?</a>)').findall(result)
                result = uniqueList(result).list

            sources = []
            for i in result:
                try:
                    host = common.parseDOM(i, "a")[0]
                    host = host.split(' ')[-1].split('>', 1)[-1].rsplit('<', 1)[0]
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = '%s/%s' % (self.base_link, url)
                    sources.append({'host': host, 'url': url})
                except:
                    pass

            sources = [i for i in sources if any(x in i['host'] for x in host_order)]
            sources.sort(key=lambda x: host_order.index(x['host']))

            if len(sources) == 0:
                url = common.parseDOM(result, "a", ret="href")[0]
                url = '%s/%s' % (self.base_link, url)
                sources.append({'url': url})

            if len(sources) == 0: return
        except:
            return

        for i in sources:
            try:
                url = i['url']
                result = getUrl(url).result
                url = common.parseDOM(result, "button", ret="OnClick")[0]
                url = url.split("'")[1]

                url = resolver().sources_resolve(url)

                if url == None: raise Exception()
                return url
            except:
                pass

class mega:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.megatv.com'
        self.feed_link = 'http://megatv.feed.gr'
        self.media_link = 'http://media.megatv.com'
        self.shows_link = 'http://megatv.feed.gr/mobile/mobile.asp?pageid=816&catidlocal=32623&subidlocal=20933'
        self.episodes_link = 'http://megatv.feed.gr/mobile/mobile/ekpompiindex_29954.asp?pageid=816&catidlocal=%s'
        self.news_link = 'http://www.megatv.com/webtv/default.asp?catid=27377&catidlocal=27377'
        self.sports_link = 'http://www.megatv.com/webtv/default.asp?catid=27377&catidlocal=27387'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)

    def news(self):
        name = 'MEGA GEGONOTA'
        self.list = self.episodes_list2(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def sports(self):
        name = 'MEGA SPORTS'
        self.list = self.episodes_list2(name, self.sports_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link, mobile=True).result
            shows = common.parseDOM(result, "li")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "h1")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                tpl = common.parseDOM(show, "a", ret="data-tpl")[0]
                if not tpl == 'ekpompiindex': raise Exception()

                url = common.parseDOM(show, "a", ret="data-params")[0]
                url = self.episodes_link % url.split("catid=")[-1]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': '0', 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.shows_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def shows_info(self, i):
        try:
            result = getUrl(self.list[i]['url'], mobile=True).result

            image = common.parseDOM(result, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            self.list[i].update({'image': image})
        except:
            pass

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result
            result = common.parseDOM(result, "section", attrs = { "class": "ekpompes.+?" })[0]
            episodes = common.parseDOM(result, "li")
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "h5")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="data-vUrl")[0]
                url = url.replace(',', '').split('/i/', 1)[-1].rsplit('.csmil', 1)[0]
                url = '%s/%s' % (self.media_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def episodes_list2(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')

            v1 = '/megagegonota/'
            match = re.search("addPrototypeElement[(]'.+?','REST','(.+?)','(.+?)'.+?[)]", result)
            v2,v3 = match.groups()
            redirect = '%s%s%s?%s' % (self.base_link, v1, v2, v3)

            result = getUrl(redirect).result
            result = result.decode('iso-8859-7').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "rest" })[0]
            episodes = common.parseDOM(result, "li")
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a")[1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = url.split("catid=")[-1].replace("')",'')
                url = '%s/r.asp?catid=%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                if not image.startswith('http://'):
                    image = '%s%s%s' % (self.base_link, v1, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('{file:"(%s/.+?)"' % self.media_link).findall(result)[0]
            return url
        except:
            return

class ant1:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.antenna.gr'
        self.img_link = 'http://www.antenna.gr/imgHandler/326'
        self.shows_link = 'http://www.antenna.gr/tv/doubleip/shows?version=3.0'
        self.episodes_link = 'http://www.antenna.gr/tv/doubleip/show?version=3.0&sid='
        self.episodes_link2 = 'http://www.antenna.gr/tv/doubleip/categories?version=3.0&howmany=100&cid='
        self.news_link = 'http://www.antenna.gr/tv/doubleip/show?version=3.0&sid=222903'
        self.sports_link = 'http://www.antenna.gr/tv/doubleip/categories?version=3.0&howmany=100&cid=3062'
        self.watch_link = 'http://www.antenna.gr/webtv/watch?cid=%s'
        self.info_link = 'http://www.antenna.gr/webtv/templates/data/player?cid=%s'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)

    def news(self):
        name = 'ANT1 NEWS'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def sports(self):
        name = 'ANT1 SPORTS'
        self.list = self.episodes_list(name, self.sports_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            self.list.append({'name': 'ANT1 NEWS', 'url': self.news_link, 'image': 'http://www.antenna.gr/imgHandler/326/5a7c9f1a-79b6-47e0-b8ac-304d4e84c591.jpg', 'genre': 'Greek', 'plot': 'ANT1 NEWS'})

            result = getUrl(self.shows_link, mobile=True).result
            shows = re.compile('({.+?})').findall(result)
        except:
            return

        for show in shows:
            try:
                i = json.loads(show)

                name = i['teasertitle'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = i['webpath'].strip()
                image = '%s/%s' % (self.img_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                url = i['id'].strip()
                url = self.episodes_link + url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: plot = i['teasertext'].strip()
                except: plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result

            if url.startswith(self.episodes_link):
                id = json.loads(result)
                id = id['feed']['show']['videolib']
                if url.endswith('sid=223077'): id = '3110'#EUROPA LEAGUE
                elif url.endswith('sid=318756'): id = '3246'#ÏËÁ ÔÑÅËÁ
                elif url.endswith('sid=314594'): id = '4542'#THE VOICE
            elif url.startswith(self.episodes_link2):
                id = ''

            if id == '':
                episodes = result.replace("'",'"').replace('"title"','"caption"').replace('"image"','"webpath"').replace('"trailer_contentid"','"contentid"')
                episodes = re.compile('({.+?})').findall(episodes)
            else:
                url = self.episodes_link2 + id
                episodes = getUrl(url, mobile=True).result
                episodes = re.compile('({.+?})').findall(episodes)
        except:
            return

        for episode in episodes:
            try:
                i = json.loads(episode)

                name = i['caption'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = i['webpath'].strip()
                image = '%s/%s' % (self.img_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                url = i['contentid'].strip()
                url = self.watch_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        id = url.split("?")[-1].split("cid=")[-1].split("&")[0]
        dataUrl = self.info_link % id
        pageUrl = self.watch_link % id
        swfUrl = 'http://www.antenna.gr/webtv/images/fbplayer.swf'

        try:
            result = getUrl(dataUrl).result
            rtmp = common.parseDOM(result, "FMS")[0]
            playpath = common.parseDOM(result, "appStream")[0]
            url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
            if playpath.startswith('http://'): url = playpath
            return url
        except:
            pass

class alpha:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.alphatv.gr'
        self.shows_link = 'http://www.alphatv.gr/shows'
        self.shows_link2 = 'http://www.alphatv.gr/views/ajax?view_name=alpha_shows_category_view&view_display_id=page_3&view_path=shows&view_base_path=shows&page=%s'
        self.news_link = 'http://www.alphatv.gr/shows/informative/news'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)

    def news(self):
        name = 'ALPHA NEWS'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            filter = common.parseDOM(result, "span", attrs = { "class": "field-content" })
            filter = common.parseDOM(filter, "a", ret="href")
            filter = uniqueList(filter).list

            threads = []
            result = ''
            for i in range(0, 5):
                self.data.append('')
                showsUrl = self.shows_link2 % str(i)
                threads.append(Thread(self.thread, showsUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += json.loads(i)[1]['data']

            shows = common.parseDOM(result, "li")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "span")[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                if not any(url == i for i in filter): raise Exception()
                url = '%s%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            redirects = ['/webtv/shows?page=0', '/webtv/shows?page=1', '/webtv/shows?page=2', '/webtv/shows?page=3', '/webtv/episodes?page=0', '/webtv/episodes?page=1', '/webtv/episodes?page=2', '/webtv/episodes?page=3', '/webtv/news?page=0', '/webtv/news?page=1']
            base = url

            count = 0
            threads = []
            result = ''
            for redirect in redirects:
                self.data.append('')
                threads.append(Thread(self.thread, url + redirect, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "views-field.+?" })
        except:
        	return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "img", ret="alt")[-1]
                if name == '': raise Exception()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[-1]
                url = '%s%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if not url.startswith(base): raise Exception()
                if url in [i['url'] for i in self.list]: raise Exception()

                image = common.parseDOM(episode, "img", ret="src")[-1]
                if not image.startswith('http://'): image = '%s%s' % (self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.replace('\n','')

            try:
                url = re.compile("playlist:.+?file: '(.+?[.]m3u8)'").findall(result)[0]
                if "EXTM3U" in getUrl(url).result: return url
            except:
                pass

            url = re.compile('playlist:.+?"(rtmp[:].+?)"').findall(result)[0]
            url += ' timeout=10'
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class star:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.star.gr'
        self.shows_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=hosts'
        self.episodes_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=%s&artId=%s'
        self.news_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=News&artId=9'
        self.watch_link = 'http://cdnapi.kaltura.com/p/21154092/sp/2115409200/playManifest/entryId/%s/flavorId/%s/format/url/protocol/http/a.mp4'
        self.enikos_link = 'http://gdata.youtube.com/feeds/api/users/enikoslive/uploads'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)

    def news(self):
        name = 'STAR NEWS'
        image = 'http://www.star.gr/tv/PublishingImages/160913114342_2118.jpg'
        self.list = self.episodes_list(name, self.news_link, image, 'Greek', '0', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link, mobile=True).result
            result = json.loads(result)
            shows = result['hosts']
        except:
            return

        for show in shows:
            try:
                name = show['Title'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = show['Image'].strip()
                image = '%s%s' % (self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                id = show['ProgramId']
                cat = show['ProgramCat'].strip()
                url = self.episodes_link % (cat, id)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if url.endswith('artId=42'): url = self.enikos_link

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result
            result = json.loads(result)

            try: plot = result['programme']['StoryLinePlain'].strip()
            except: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            episodes = result['videosprogram']
        except:
        	return

        for episode in episodes:
            try:
                name = episode['Title'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = episode['VideoID'].strip()
                url = self.watch_link % (url, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class skai:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.skai.gr'
        self.show_link = 'http://www.skai.gr/player/TV/?mmid=%s'
        self.shows_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.TV.ProgramListView&la=0&Type=TV&Day=%s'
        self.episodes_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.Player.ItemView&type=TV&cid=6&alid=%s'
        self.docs_link = 'http://www.skai.gr/mobile/tv/category?cid=6'
        self.news_link = 'http://www.skai.gr/player/TV/?mmid=243980'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)

    def docs(self):
        self.list = index().cache(self.docs_list, 24)
        index().showList(self.list)

    def news(self):
        name = 'SKAI NEWS'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def docs_list(self):
        try:
            result = getUrl(self.docs_link).result
            result = common.parseDOM(result, "div", attrs = { "id": "mbl-tv-ondemand" })[0]

            docs = common.parseDOM(result, "li")
        except:
            return

        for doc in docs:
            try:
                name = common.parseDOM(doc, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                u = common.parseDOM(doc, "a", ret="href")[0]
                u = '%s%s' % (self.base_link, u)
                u = common.replaceHTMLCodes(u)
                u = u.encode('utf-8')

                self.list.append({'name': name, 'u': u, 'url': '0', 'image': '0', 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.docs_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['url'] == '0']

        return self.list

    def docs_info(self, i):
        try:
            result = getUrl(self.list[i]['u']).result
            result = common.parseDOM(result, "div", attrs = { "id": "mbl-tv-ondemand" })[0]

            url = common.parseDOM(result, "a", ret="href")[0]
            url = self.show_link % url.split('=')[-1]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            if not url == '0': self.list[i].update({'url': url})

            image = common.parseDOM(result, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            if not image == '0': self.list[i].update({'image': image})
        except:
            pass

    def shows_list(self):
        try:
            url = []
            d = datetime.datetime.utcnow()
            for i in range(0, 7):
                url.append(self.shows_link % d.strftime("%d.%m.%Y"))
                d = d - datetime.timedelta(hours=24)
            url = url[::-1]

            self.result = []

            def thread(url):
                try: self.result.append(getUrl(url).result)
                except: pass

            threads = []
            for i in range(0, 7): threads.append(Thread(thread, url[i]))
            [i.start() for i in threads]
            [i.join() for i in threads]

            result = ''.join(self.result)

            shows = common.parseDOM(result, "Show", attrs = { "TVonly": "0" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "Show")[0]
                name = name.split('[')[-1].split(']')[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "Link")[0]
                url = url.split('[')[-1].split(']')[0]
                url = '%s%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "ShowImage")[0]
                image = image.split('[')[-1].split(']')[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                plot = common.parseDOM(show, "Description")[0]
                plot = plot.split('[')[-1].split(']')[0]
                plot = plot.replace('<br>','').replace('</br>','').replace('\n','').split('<')[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                if image in str(self.list): raise Exception()
                if not 'mmid=' in url: raise Exception()

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "li", ret="id", attrs = { "class": "active_sub" })[0]

            self.result = []

            def thread(url, i):
                try: self.result[i] = getUrl(url).result
                except: pass

            threads = []
            for i in range(1, 3): self.result.append('')
            for i in range(1, 3): threads.append(Thread(thread, self.episodes_link % url + '&Page=%s' % str(i), i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]

            result = ''
            for i in self.result: result += i

            episodes = common.parseDOM(result, "Item")
        except:
        	return

        for episode in episodes:
            try:
                title = common.parseDOM(episode, "Title")[0]
                title = title.split('[')[-1].split(']')[0]

                date = common.parseDOM(episode, "Date")[0]
                date = date.split('[')[-1].split(']')[0]
                date = date.split('T')[0]

                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "File")[0]
                url = url.split('[')[-1].split(']')[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "Photo1")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "span", attrs = { "id": "p-file" })[0]
            return url
        except:
            return

class sigma:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.sigmatv.com'
        self.shows_link = 'http://www.sigmatv.com/shows'
        self.news_link = 'http://www.sigmatv.com/shows/tomes-sta-gegonota/episodes'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)

    def news(self):
        name = 'SIGMA NEWS'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            shows = common.parseDOM(result, "div", attrs = { "class": "show_entry.+?" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "div", attrs = { "class": "body" })[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                filter = ['/uefa-champions-league', '/seirestainies', '/tilenouveles', '/alpha']
                if any(url.endswith(i) for i in filter): raise Exception()
                url = '%s/%s/episodes' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = image.replace('/./', '')
                image = '%s/%s' % (self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try: plot = common.parseDOM(show, "div", attrs = { "style": "min.+?" })[-1]
                except: plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(0, 100, 20):
                self.data.append('')
                episodesUrl = url + '/page/%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "entry .+?" })
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "img", ret="alt")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                if '/no-image' in image: raise Exception()
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result

            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/flash" })[0]
            url = common.replaceHTMLCodes(url)

            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class nerit:
    def __init__(self):
        self.base_link = 'http://webtv.nerit.gr'
        self.m3u8_link = 'http://hprt-vod.flashcloud.mediacdn.com/mediacache/mobile/mp4:hprt/%s/playlist.m3u8'

    def resolve(self, url):
        try:
            result = getUrl(url).result

            embed = common.parseDOM(result, "div", attrs = { "id": "player-embed" })[0]
            embed = common.parseDOM(embed, "iframe", ret="src")[0]
            embed = embed.replace(' ', '%20')

            result = getUrl(embed).result
            url = re.compile("file:\s+'(.+?)'").findall(result)[0]
            url = url.replace(' ', '%20')
            url = self.m3u8_link % url
            return url
        except:
            return

class ant1cy:
    def __init__(self):
        self.base_link = 'http://www.ant1iwo.com'
        self.old_link = 'http://www.ant1.com.cy'

    def resolve(self, url):
        try:
            result = getUrl(url).result
            rtmp = re.compile("netConnectionUrl:\s+'(.+?)'").findall(result)[0]
            playpath = common.parseDOM(result, "div", ret="data-video")[0]
            if ' ' in playpath: raise Exception()
            url = '%s playpath=%s' % (rtmp, playpath)
            return url
        except:
            return

class megacy:
    def __init__(self):
        self.base_link = 'http://www.livenews.com.cy'

    def resolve(self, url):
        try:
            result = getUrl(url, mobile=True).result

            embed = common.parseDOM(result, "iframe", ret="src")
            embed = [i for i in embed if 'itemid' in i][0]

            result = getUrl(embed, mobile=True).result
            url = common.parseDOM(result, "video", ret="sr.+?")[0]
            return url
        except:
            return

class novasports:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.novasports.gr'
        self.episodes_link = 'http://www.novasports.gr/LiveWebTV.aspx%s'
        self.series_link = 'http://www.novasports.gr/handlers/LiveWebTv/LiveWebTvMediaGallery.ashx?containerid=-1&mediafiletypeid=0&latest=true&isBroadcast=true&tabid=shows'
        self.news_link = 'http://www.novasports.gr/handlers/LiveWebTv/LiveWebTvMediaGallery.ashx?containerid=-1&mediafiletypeid=2&latest=true&tabid=categories'

    def shows(self):
        name = 'Novasports'
        self.list = self.episodes_list(name, self.series_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def news(self):
        name = 'Novasports News'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = json.loads(result)['HTML']
            episodes = common.parseDOM(result, "li")
        except:
            return

        for episode in episodes:
            try:
                title = common.parseDOM(episode, "a", ret="title")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                try:
                    name = common.parseDOM(episode, "a", ret="title")[0]
                    date = common.parseDOM(episode, "span", attrs = { "class": "date" })[0]
                    name = '%s (%s)' % (name, date.rsplit(',', 1)[0])
                except:
                    pass
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = self.episodes_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                image = '%s/%s' % (self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': title, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = re.compile("type: 'html5'.+?'file': '(.+?)'").findall(result)[0]
            return url
        except:
            return

class mtvchart:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.mtvgreece.gr'
        self.mtvhitlisthellas_link = 'http://www.mtvgreece.gr/hitlisthellas'
        self.mtvdancefloor_link = 'http://www.mtvgreece.gr/mtv-dance-flour-chart'
        self.eurotop20_link = 'http://www.mtvgreece.gr/mtv-euro-top-20'
        self.usatop20_link = 'http://www.mtvgreece.gr/mtv-usa-top-20'
        self.youtube_search = 'http://gdata.youtube.com/feeds/api/videos?q='

    def mtvhitlisthellas(self):
        name = 'MTV Hit List Hellas'
        self.list = self.episodes_list(name, self.mtvhitlisthellas_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def mtvdancefloor(self):
        name = 'MTV Dance Floor'
        self.list = self.episodes_list(name, self.mtvdancefloor_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def eurotop20(self):
        name = 'Euro Top 20'
        self.list = self.episodes_list(name, self.eurotop20_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def usatop20(self):
        name = 'U.S. Top 20'
        self.list = self.episodes_list(name, self.usatop20_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result

            episodes = common.parseDOM(result, "span", attrs = { "class": "artistRow" })
        except:
            return

        for episode in episodes:
            try:
                name = ' '.join(re.sub('<.+?>', '', episode).split()).strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                show = common.parseDOM(result, "strong")[0]
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                query = ' '.join(re.sub('=|&|:|;|-|"|,|\'|\.|\?|\/', ' ', name).split())
                url = self.youtube_search + query + ' official'
                url = common.replaceHTMLCodes(url)

                self.list.append({'name': name, 'url': url, 'image': musicImage, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class rythmoschart:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.rythmosfm.gr'
        self.top20_link = 'http://www.rythmosfm.gr/community/top20/'
        self.youtube_search = 'http://gdata.youtube.com/feeds/api/videos?q='

    def rythmoshitlist(self):
        name = 'Rythmos Hit List'
        self.list = self.episodes_list(name, self.top20_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result

            episodes = common.parseDOM(result, "span", attrs = { "class": "toptitle" })
        except:
            return

        for episode in episodes:
            try:
                name = episode
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                show = episode.rsplit('-', 1)[-1].strip()
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                query = ' '.join(re.sub('=|&|:|;|-|"|,|\'|\.|\?|\/', ' ', name).split())
                url = self.youtube_search + query + ' official'
                url = common.replaceHTMLCodes(url)

                self.list.append({'name': name, 'url': url, 'image': musicImage, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class dailymotion:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.dailymotion.com'
        self.api_link = 'https://api.dailymotion.com'
        self.playlist_link = 'https://api.dailymotion.com/user/%s/videos?fields=description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&sort=recent&family_filter=1'
        self.watch_link = 'http://www.dailymotion.com/video/%s'
        self.info_link = 'http://www.dailymotion.com/embed/video/%s'

    def superleague(self):
        name = 'Super League'
        channel = 'greeksuperleague'
        url = self.playlist_link % channel
        self.list = self.episodes_list(name, url, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def superball(self):
        name = 'Super Ball'
        channel = 'Super-Ball'
        url = self.playlist_link % channel
        self.list = self.episodes_list(name, url, '0', 'Greek', '0', name)
        index().episodeList(self.list)

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            threads = []
            result = []
            for i in range(1, 3):
                self.data.append('')
                episodesUrl = url + '&limit=100&page=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += json.loads(i)['list']

            episodes = result
        except:
        	return

        for episode in episodes:
            try:
                name = episode['title']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = episode['id']
                url = self.watch_link % url
                url = url.encode('utf-8')

                image = episode['thumbnail_large_url']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            id = url.split("/")[-1].split("?")[0]
            result = getUrl(self.info_link % id).result

            url = None
            try: url = re.compile('"stream_h264_ld_url":"(.+?)"').findall(result)[0]
            except: pass
            try: url = re.compile('"stream_h264_url":"(.+?)"').findall(result)[0]
            except: pass
            try: url = re.compile('"stream_h264_hq_url":"(.+?)"').findall(result)[0]
            except: pass
            try: url = re.compile('"stream_h264_hd_url":"(.+?)"').findall(result)[0]
            except: pass

            url = urllib.unquote(url).decode('utf-8').replace('\\/', '/')
            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class youtube:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.youtube.com'
        self.api_link = 'http://gdata.youtube.com'
        self.playlists_link = 'http://gdata.youtube.com/feeds/api/users/%s/playlists'
        self.playlist_link = 'http://gdata.youtube.com/feeds/api/playlists/%s'
        self.search_link = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.watch_link = 'http://www.youtube.com/watch?v=%s'
        self.info_link = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'
        self.enikos_link = 'http://gdata.youtube.com/feeds/api/users/enikosgr/uploads'

    def kontra(self):
        channel = 'kontrachannelhellas'
        self.list = index().cache(self.shows_list, 24, channel, [], [])
        index().showList(self.list)

    def madtv(self):
        channel = 'MADTVGREECE'
        exclude = ["PL1RY_6CEqdtnxJYgudDydiG4fKVoQouHf", "PL1RY_6CEqdtlu30q6SyuNe6Tk5IYjAiks", "PLE4B3F6B7F753D97C", "PL85C952EA930B9E90", "PL04B2C2D8B304BA48", "PL46B9D152167BA727"]
        self.list = index().cache(self.shows_list, 24, channel, [], exclude)
        index().showList(self.list)

    def madgreekz(self):
        channel = 'madtvgreekz'
        exclude = ["PL20iPi-qHKiz1wJCqvbvy5ffrtWT1VcVF", "PL20iPi-qHKiyWnRbBdnSF7RlDdAePiKzj", "PL20iPi-qHKiyZGlOs5DTElzAK_YNCDJn0", "PL20iPi-qHKiwyRhqqmOnbDvPSUgRzzxgq"]
        self.list = index().cache(self.shows_list, 24, channel, [], exclude)
        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: return
        index().showList(self.list)

    def enikos(self):
        name = 'ENIKOS'
        self.list = self.episodes_list(name, self.enikos_link, '0', 'Greek', '0', name)
        index().episodeList(self.list[:100])

    def cartoons_classics(self):
        self.list = index().cache(self.cartoons_classics_parser, 24)
        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: return
        index().cartoonList(self.list)

    def cartoons_classics_parser(self):
        self.list = self.shows_list('GreekTvCartoon', [], [])
        self.list = self.shows_list('GreekTvCartoons', [], [])
        self.list = self.shows_list('GreekCartoonClassics', [], [])
        self.list = self.shows_list('ToonsFromThePast', [], ['PLStChvmvfcLCTv__R0DdRG95E0DC-wQik'])
        self.list = self.shows_list('lilithvii', ['PL3420AA02720B05E5', 'PL147140D5904AFBE4', 'PLF191388E07E9E127', 'PL8F5C47492E11C109', 'PLAD759EE008F12C43', 'PLC3C3861A770162F5', 'PL0C994DFD3BCDAEDB', 'PLE3470893493CF5A8', 'PLD2C2707D06DA58DC', 'PL724AA3356D663CED', 'PLC34BCF01941BAC02'], [])
        self.list = self.shows_list('Michaletosjr', [], [])
        self.list = self.shows_list('GPITRAL5', [], [])
        return self.list

    def cartoons_songs(self):
        self.list = index().cache(self.cartoons_songs_parser, 24)
        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: return
        index().cartoonList(self.list)

    def cartoons_songs_parser(self):
        self.list = self.shows_list('sapiensgr2', [], ['PLB3126415BC8BCDE3'])
        self.list = self.shows_list('Aviosys', ['PL9E9CD72ED3715FEA', 'PL35F8EE4D9D188A0C', 'PLEC7CC64E658C1D7E'], [])
        return self.list

    def shows_list(self, channel, include, exclude):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(1, 250, 25):
                self.data.append('')
                showsUrl = self.playlists_link % channel + '?max-results=25&start-index=%s' % str(i)
                threads.append(Thread(self.thread, showsUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            shows = common.parseDOM(result, "entry")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "id")[0]
                url = self.playlist_link % url.split("/")[-1]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = image.encode('utf-8')

                if image.endswith("/00000000000/0.jpg"): raise Exception() #empty playlist
                if not include == [] and not any(url.endswith(i) for i in include): raise Exception()
                if any(url.endswith(i) for i in exclude): raise Exception()

                self.list.append({'name': name, 'title': name, 'url': url, 'image': image, 'year': '0', 'genre': 'Greek', 'type': 'tvshow', 'plot': '0'})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(1, 250, 25):
                self.data.append('')
                episodesUrl = url + '?max-results=25&start-index=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "entry")
        except:
        	return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "media:player", ret="url")[0]
                url = url.split("&amp;")[0].split("=")[-1]
                url = self.watch_link % url
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve_search(self, url):
        try:
            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url).result
            result = common.parseDOM(result, "entry")
            result = common.parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]
                url = self.watch_link % url
                url = self.resolve(url)
                if not url is None: return url
        except:
            return

    def resolve(self, url):
        try:
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(self.info_link % id).result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(self.watch_link % id).result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class livestream:
    def http(self, url):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            response.close()
            response = response.info()
            return url
        except:
            return

    def hls(self, url):
        try:
            result = getUrl(url).result
            if "EXTM3U" in result: return url
        except:
            return

    def skai(self, url):
        try:
            root = 'http://www.skai.gr/ajax.aspx?m=NewModules.LookupMultimedia&mmid=/Root/TVLive'
            result = getUrl(root).result
            url = common.parseDOM(result, "File")[0]
            url = url.split('[')[-1].split(']')[0]
            url = 'http://www.youtube.com/watch?v=%s' % url

            result = getUrl(url).result
            url = re.compile('"hlsvp": "(.+?)"').findall(result)[0]
            url = urllib.unquote(url).replace('\\/', '/')
            return url
        except:
            return

    def madtv(self, url):
        try:
            result = getUrl(url, timeout=30).result
            url = common.parseDOM(result, "iframe", ret="src")
            url = [i for i in url if 'apps.' in i][0]
            if not url.startswith('http://'): url = url.replace('//', 'http://') 

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src")[0]
            url = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            url = 'http://www.youtube.com/watch?v=%s' % url

            result = getUrl(url).result
            url = re.compile('"hlsvp": "(.+?)"').findall(result)[0]
            url = urllib.unquote(url).replace('\\/', '/')
            return url
        except:
            return

    def viiideo(self, url):
        try:
            result = getUrl(url).result
            url = re.compile("ipadUrl.+?'http://(.+?)/playlist[.]m3u8'").findall(result)[0]
            url = 'rtmp://%s live=1 timeout=10' % url
            return url
        except:
            return

    def dailymotion(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"flashvars".+?value="(.+?)"').findall(result)[0]
            url = urllib.unquote(url).decode('utf-8').replace('\\/', '/')
            quality = None
            try: quality = re.compile('"ldURL":"(.+?)"').findall(url)[0]
            except: pass
            try: quality = re.compile('"sdURL":"(.+?)"').findall(url)[0]
            except: pass
            try: quality = re.compile('"hqURL":"(.+?)"').findall(url)[0]
            except: pass
            quality += '&redirect=0'
            url = getUrl(quality).result
            url = '%s live=1 timeout=10' % url
            return url
        except:
            return

    def livestream(self, url):
        try:
            name = url.split("/")[-1]
            url = 'http://x%sx.api.channel.livestream.com/3.0/getstream.json' % name
            result = getUrl(url).result
            isLive = str(result.find('isLive":true'))
            if isLive == '-1': return
            url = re.compile('"httpUrl".+?"(.+?)"').findall(result)[0]
            return url
        except:
            return

    def streamago(self, url):
        try:
            result = getUrl(url + '/xml/').result
            url = common.parseDOM(result, "path_rtsp")[0]
            url = url.split('[')[-1].split(']')[0]
            return url
        except:
            return

    def ustream(self, url):
        try:
            try:
                result = getUrl(url).result
                id = re.compile('ustream.tv/embed/(.+?)"').findall(result)[0]
            except:
                id = url.split("/embed/")[-1]
            #url = 'http://iphone-streaming.ustream.tv/uhls/%s/streams/live/iphone/playlist.m3u8' % id
            url = 'http://sjc-uhls-proxy-beta01.ustream.tv/watch/playlist.m3u8?cid=%s' % id
            for i in range(1, 51):
                result = getUrl(url).result
                if "EXT-X-STREAM-INF" in result: return url
                if not "EXTM3U" in result: return
            return
        except:
            return

    def veetle(self, url):
        try:
            akamaiProxy = os.path.join(addonPath,'akamaisecurehd.py')
            xbmc.executebuiltin('RunScript(%s)' % akamaiProxy)
            name = url.split("#")[-1]
            url = 'http://www.veetle.com/index.php/channel/ajaxStreamLocation/%s/flash' % name
            result = getUrl(url).result
            url = json.loads(result)
            url = base64.encodestring(url['payload']).replace('\n', '')
            url = 'http://127.0.0.1:64653/veetle/%s' % url
            return url
        except:
            return


main()