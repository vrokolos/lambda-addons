# -*- coding: utf-8 -*-

'''
    Hellenic TV Add-on
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

import urllib2,re,os,threading,datetime,time,xbmc,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter

try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


action              = None
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonLogos          = os.path.join(addonPath,'resources/logos')
addonChannels       = os.path.join(addonPath,'resources/channels.xml')
addonEPG            = os.path.join(addonPath,'xmltv.xml')


class main:
    def __init__(self):
        while (not xbmc.abortRequested):
            epg()
            count = 60
            while (not xbmc.abortRequested) and count > 0:
                count -= 1
                time.sleep(1)


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
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
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

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class index:
    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

class epg:
    def __init__(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            t1 = datetime.datetime.utcfromtimestamp(os.path.getmtime(addonEPG))
            t2 = datetime.datetime.utcnow()
            update = abs(t2 - t1) > datetime.timedelta(hours=24)
            if update is False: return
        except:
            pass
        if index().getProperty('htv_Service_Running') == 'true': return
        index().setProperty('htv_Service_Running', 'true')

        self.xmltv = ''
        self.get_dates()
        self.get_channels()
        threads = []
        threads.append(Thread(self.ote_data))
        [i.start() for i in threads]
        [i.join() for i in threads]
        self.xmltv_creator()

        index().clearProperty('htv_Service_Running')

    def get_dates(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            self.dates = []
            now = self.greek_datetime()
            today = datetime.date(now.year, now.month, now.day)
            for i in range(0, 3):
                d = today + datetime.timedelta(days=i)
                self.dates.append(str(d))
        except:
            return

    def get_channels(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            self.channels = []
            file = xbmcvfs.File(addonChannels)
            result = file.read()
            file.close()
            channels = common.parseDOM(result, "channel", attrs = { "active": "True" })
        except:
            return
        for channel in channels:
            try:
                channel = common.parseDOM(channel, "name")[0]
                self.channels.append(channel)
            except:
                pass

    def ote_data(self):
        if xbmc.abortRequested == True: sys.exit()
        threads = []
        self.oteData = []
        for date in self.dates:
            date = date.replace('-','')
            url = 'http://otetv.ote.gr/otetv_program/ProgramListServlet?t=sat&d=%s' % date
            threads.append(Thread(self.ote_data2, date, url))
        [i.start() for i in threads]
        [i.join() for i in threads]

    def ote_data2(self, date, url):
        if xbmc.abortRequested == True: sys.exit()
        try:
            result = getUrl(url).result
            self.oteData.append({'date': date, 'value': result})
        except:
            return

    def ote_programme(self, channel, id):
        if xbmc.abortRequested == True: sys.exit()
        programmes = []
        programmeList = []

        for data in self.oteData:
            try:
                date = data["date"]
                data = data["value"]
                data = json.loads(data)
                data = data["titles"][id]
                data = data.iteritems()
                [programmes.append({'date': date, 'value': value}) for key, value in data]
            except:
                pass

        for programme in programmes:
            try:
                date = programme["date"]
                programme = programme["value"]
                start = programme["start"].replace(':','')
                start = date + str('%04d' % int(start)) + '00'
                start = self.start_processor(start)
                title = programme["title"]
                title = self.title_prettify(title)
                subtitle = programme["category"]
                desc = programme["desc"].split("<br/>")[-1]
                desc = self.desc_prettify(desc)
                programmeList.append({'start': start, 'title': title, 'desc': desc})
            except:
                pass

        self.programme_creator(channel, programmeList)

    def tvc_data(self, id):
        if xbmc.abortRequested == True: sys.exit()
        threads = []
        self.tvcData = []
        for date in self.dates:
            date = date.replace('-','')
            url = 'http://www.tvcontrol.gr/json/events/channel_%s_0.json?d=%s000000' % (id, date)
            threads.append(Thread(self.tvc_data2, date, url))
        [i.start() for i in threads]
        [i.join() for i in threads]

    def tvc_data2(self, date, url):
        if xbmc.abortRequested == True: sys.exit()
        try:
            result = getUrl(url).result
            self.tvcData.append({'date': date, 'value': result})
        except:
            return

    def tvc_programme(self, channel, id):
        if xbmc.abortRequested == True: sys.exit()
        self.tvc_data(id)
        self.tvcData = sorted(self.tvcData, key=itemgetter('date'))
        programmes = []
        programmeList = []

        for data in self.tvcData:
            try:
                date = data["date"]
                d = json.loads(data["value"])
                data = []
                for i in range(0, len(d)): data += d[i]["events"]
                [programmes.append({'date': date, 'value': value}) for value in data]
            except:
                pass

        for programme in programmes:
            try:
                date = programme["date"]
                programme = programme["value"]
                start = programme["event_time"].replace(':','')
                start = date + str('%04d' % int(start)) + '00'
                start = self.start_processor(start)
                title = programme["constructed_titlegr"]
                title = self.title_prettify(title)
                descDict = {'1': '¡ËÎÁÙÈÍ‹', '3': '≈È‰ﬁÛÂÈÚ', '4': 'ÕÙÔÍÈÏ·ÌÙ›Ò', '5': '–·È‰ÈÍ‹', '6': '‘·ÈÌﬂ·', '8': '”ÂÈÒ‹', '10': 'ÿı˜·„˘„ﬂ·'}
                desc = programme["main_genre_id"]
                try: desc = descDict[desc].decode('iso-8859-7')
                except: desc = descDict['10'].decode('iso-8859-7')
                programmeList.append({'start': start, 'title': title, 'desc': desc})
            except:
                pass

        self.programme_creator(channel, programmeList)

    def dummy_programme(self, channel):
        if xbmc.abortRequested == True: sys.exit()
        desc = 'ƒÂÌ ı‹Ò˜ÔıÌ ÎÁÒÔˆÔÒﬂÂÚ.'.decode('iso-8859-7')
        self.get_titleDict()
        programmeList = []

        for date in self.dates:
            for i in range(0, 2400, 1200):
                start = date.replace('-','') + '%04d' % i + '00'
                start = self.start_processor(start)
                try: title = self.titleDict[channel]
                except: title = channel
                programmeList.append({'start': start, 'title': title, 'desc': desc})

        self.programme_creator(channel, programmeList)

    def greek_datetime(self):
        if xbmc.abortRequested == True: sys.exit()
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 2)
        d = datetime.datetime(dt.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt < dstoff:
            return dt + datetime.timedelta(hours = 1)
        else:
            return dt

    def start_processor(self, start):
        if xbmc.abortRequested == True: sys.exit()
        dt1 = self.greek_datetime()
        dt2 = datetime.datetime.now()
        dt3 = datetime.datetime.utcnow()
        dt1 = datetime.datetime(dt1.year, dt1.month, dt1.day, dt1.hour)
        dt2 = datetime.datetime(dt2.year, dt2.month, dt2.day, dt2.hour)
        dt3 = datetime.datetime(dt3.year, dt3.month, dt3.day, dt3.hour)
        start = datetime.datetime(*time.strptime(start, "%Y%m%d%H%M%S")[:6])
        if dt2 >= dt1 :
            dtd = (dt2 - dt1).seconds/60/60
            tz = (dt1 - dt3).seconds/60/60
            tz = ' +' + '%02d' % (dtd + tz) + '00'
            start = start + datetime.timedelta(hours = int(dtd))
        else:
            dtd = (dt1 - dt2).seconds/60/60
            tz = (dt1 - dt3).seconds/60/60
            tz = ' -' + '%02d' % (dtd - tz) + '00'
            start = start - datetime.timedelta(hours = int(dtd))
        start = '%04d' % start.year + '%02d' % start.month + '%02d' % start.day + '%02d' % start.hour + '%02d' % start.minute + '%02d' % start.second + tz
        return start

    def title_prettify(self, title):
        if xbmc.abortRequested == True: sys.exit()
        acuteDict = {u'\u0386': u'\u0391', u'\u0388': u'\u0395', u'\u0389': u'\u0397', u'\u038A': u'\u0399', u'\u038C': u'\u039F', u'\u038E': u'\u03A5', u'\u038F': u'\u03A9', u'\u0390': u'\u03AA', u'\u03B0': u'\u03AB'}
        title = common.replaceHTMLCodes(title)
        title = title.strip().upper()
        for key in acuteDict:
            title = title.replace(key, acuteDict[key])
        return title

    def desc_prettify(self, desc):
        if xbmc.abortRequested == True: sys.exit()
        desc = common.replaceHTMLCodes(desc)
        desc = desc.strip()
        return desc

    def xml_attrib(self, str):
        if xbmc.abortRequested == True: sys.exit()
        str = str.replace("&", "&amp;")
        str = str.replace("'", "&apos;")
        str = str.replace("\"", "&quot;")
        str = str.replace("<", "&lt;")
        str = str.replace(">", "&gt;")
        return str

    def programme_creator(self, channel, list):
        if xbmc.abortRequested == True: sys.exit()
        list = sorted(list, key=itemgetter('start'))
        for i in range(0, len(list)):
            start = list[i]['start']
            try: stop = list[i+1]['start']
            except: stop = list[i]['start']
            title = list[i]['title']
            desc = list[i]['desc']
            channel, title, desc = self.xml_attrib(channel), self.xml_attrib(title), self.xml_attrib(desc)
            self.xmltv += '<programme channel="%s" start="%s" stop="%s">\n' % (channel, start, stop)
            self.xmltv += '<title lang="el">%s</title>\n' % (title)
            self.xmltv += '<desc>%s</desc>\n' % (desc)
            self.xmltv += '</programme>\n'

    def xmltv_creator(self):
        if xbmc.abortRequested == True: sys.exit()
        self.xmltv += '<tv>\n'
        for channel in self.channels:
            channel = self.xml_attrib(channel)
            self.xmltv += '<channel id="%s">\n' % (channel)
            self.xmltv += '<display-name>%s</display-name>\n' % (channel)
            self.xmltv += '<icon src="%s/%s.png"/>\n' % (addonLogos, channel)
            self.xmltv += '<stream>plugin://plugin.video.hellenic.tv/?action=play_live&amp;channel=%s</stream>\n' % (channel.replace(' ','_'))
            self.xmltv += '</channel>\n'

        self.get_channelDict()

        for c in self.channelDict:
            try:
                if not c[0] in self.channels: raise Exception()
                self.channels = [i for i in self.channels if not i == c[0]]
                if c[1] == 'OTE': self.ote_programme(c[0], c[2])
                elif c[1] == 'TVC': self.tvc_programme(c[0], c[2])
            except:
                pass

        for channel in self.channels:
            self.dummy_programme(channel)

        self.xmltv += '</tv>'
        write = self.xmltv.replace('\n','').encode('utf8')

        try: xbmcvfs.delete(addonEPG)
        except: pass
        file = xbmcvfs.File(addonEPG, 'w')
        file.write(str(write))
        file.close()

    def get_titleDict(self):
        self.titleDict = {
            'RIK SAT'                   : 'ƒœ—’÷œ—… œ —… '.decode('iso-8859-7'),
            'NICKELODEON+'              : '–¡…ƒ… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7'),
            'MUSIC TV'                  : 'Ãœ’”… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7'),
            'GREEK CINEMA'              : '≈ÀÀ«Õ… « ‘¡…Õ…¡'.decode('iso-8859-7'),
            'CY SPORTS'                 : '¡»À«‘… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7'),
            'ODIE TV'                   : '…––œƒ—œÃ…≈”'.decode('iso-8859-7'),
            'SMILE TV'                  : '–¡…ƒ… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7'),
            'GNOMI TV'                  : 'Ãœ’”… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7')
        }

    def get_channelDict(self):
        self.channelDict = [
            ('MEGA',                      'OTE', '90'),
            ('ANT1',                      'OTE', '150'),
            ('STAR',                      'OTE', '98'),
            ('ALPHA',                     'OTE', '132'),
            ('SKAI',                      'OTE', '120'),
            ('NERIT',                     'OTE', '593'),
            ('MACEDONIA TV',              'OTE', '152'),
            ('BOYLH TV',                  'OTE', '119'),
            ('EURONEWS',                  'OTE', '19'),
            ('NICKELODEON',               'OTE', '117'),
            ('MTV',                       'OTE', '121'),
            ('MAD TV',                    'OTE', '144'),
            ('KONTRA CHANNEL',            'OTE', '44'),
            ('BLUE SKY',                  'OTE', '153'),
            ('ART CHANNEL',               'OTE', '156'),
            ('EXTRA 3',                   'OTE', '135'),
            ('CHANNEL 9',                 'OTE', '163'),
            ('SBC TV',                    'OTE', '136'),
            ('AB CHANNEL',                'OTE', '157'),
            ('TV 100',                    'OTE', '137'),
            ('4E TV',                     'OTE', '133'),
            ('STAR KENTRIKIS ELLADOS',    'OTE', '139'),
            ('EPIRUS TV1',                'OTE', '145'),
            ('CORFU CHANNEL',             'OTE', '166'),
            ('BEST TV',                   'OTE', '165'),
            ('KRITI TV',                  'OTE', '138'),
            ('KOSMOS',                    'OTE', '169'),
            ('TV AIGAIO',                 'OTE', '164'),
            ('DIKTYO TV',                 'OTE', '146'),
            ('DELTA TV',                  'OTE', '147'),

            ('E TV',                      'TVC', '326'),
            ('ACTION 24',                 'TVC', '189'),
            ('MEGA CYPRUS',               'TVC', '306'),
            ('ANT1 CYPRUS',               'TVC', '258'),
            ('SIGMA',                     'TVC', '305'),
            ('TV PLUS',                   'TVC', '289'),
            ('EXTRA TV',                  'TVC', '290'),
            ('CAPITAL',                   'TVC', '282'),
            ('RIK SAT',                   'TVC', '83')
        ]


main()