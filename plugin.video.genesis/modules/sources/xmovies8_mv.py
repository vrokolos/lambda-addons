# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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


import re
import urllib
import urlparse
from modules.libraries import cleantitle
from modules.libraries import cloudflare
from modules.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://xmovies8.co'
        self.cookie = 'location.href=1'
        self.search_link = '/?s=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            result = cloudflare.source(query)

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            match = client.parseDOM(result, "div", attrs = { "class": "post-panel" })
            match = client.parseDOM(match, "h2")

            if len(match) == 0:
                t = client.parseDOM(result, "meta", ret="content", attrs = { "property": "og:title" })[0]
                t = re.compile(': (.+?\(\d{4}\))').findall(t)[0]
                if not title == cleantitle.movie(t): return
                if not any(x in t for x in years): return
                result = client.parseDOM(result, "link", ret="href", attrs = { "rel": "canonical" })[0]
            else:
                result = [(client.parseDOM(i, "a", ret="href")[0], client.parseDOM(i, "a")[0]) for i in match]
                result = [i for i in result if title == cleantitle.movie(i[1])]
                result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            if not self.base_link in result: return

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = cloudflare.source(url)

            url = re.compile('(<a .+?</a>)').findall(result)
            url = [(client.parseDOM(i, "a", ret="href"), client.parseDOM(i, "a")) for i in url]
            url = [(i[0][0], i[1][0]) for i in url if len(i[0]) > 0 and len(i[1]) > 0]

            try: sources.append({'source': 'GVideo', 'quality': '1080p', 'provider': 'Xmovies8', 'url': [i[0] for i in url if i[1].startswith('1920') and 'google' in i[0]][0]})
            except: pass
            try: sources.append({'source': 'GVideo', 'quality': 'HD', 'provider': 'Xmovies8', 'url': [i[0] for i in url if i[1].startswith('1280') and 'google' in i[0]][0]})
            except: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

