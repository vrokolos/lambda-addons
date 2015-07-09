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
from modules.libraries import client


class source:
    def __init__(self):
        self.base_link = 'https://m.sweflix.to'
        self.agent_link = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u='
        self.search_link = '/index.php?show=query&q=%s'
        self.player_link = '/view.php?vicloid=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            if result == None: result = client.source(self.agent_link + urllib.quote_plus(query))

            result = result.replace('\r','').replace('\n','').replace('\t','')

            result = re.compile('(<div id="*\d*.+?</div>)').findall(result)

            title = cleantitle.movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(re.compile('id="*(\d*)"*').findall(i), re.compile('<h4>(.+?)</h4>').findall(i), re.compile('Releasedatum *: *(\d{4})').findall(i)) for i in result]
            result = [(i[0][0], i[1][0], i[2][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            result = [(i[0], i[1].rsplit('</span>')[0].split('>')[-1].strip(), i[2]) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

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

            url = urlparse.urljoin(self.base_link, self.player_link % url)

            result = client.source(url)
            if result == None: result = client.source(self.agent_link + urllib.quote_plus(url))

            result = result.replace('\r','').replace('\n','').replace('\t','')

            result = re.compile('<source src="*(.+?)"* type="*video').findall(result)[0]
            url = result.replace('sweflix.net', 'sweflix.%s' % (urlparse.urlparse(url).netloc).split('.')[-1])

            if '1080p' in url: quality = '1080p'
            else: quality = 'HD'

            sources.append({'source': 'Sweflix', 'quality': quality, 'provider': 'Sweflix', 'url': url})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url

