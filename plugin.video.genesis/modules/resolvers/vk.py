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
import urlparse
from modules.libraries import client


def resolve(url):
    try:
        base = url.replace('https://', 'http://')
        result = str(client.request(base))

        u = re.compile('url(720|540|480|360|240)=(.+?)&').findall(result)

        url = []
        try: url += [[{'quality': 'HD', 'url': i[1]} for i in u if i[0] == '720'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '540'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '480'][0]]
        except: pass
        if not url == []: return url
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '360'][0]]
        except: pass
        if not url == []: return url
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '240'][0]]
        except: pass

        if not url == []: return url


        try: s = 'http://www.vkvideosearch.com/video.php?v=%s' % re.compile('video(.+_.+)').findall(base)[0]
        except: pass
        try: s = 'http://www.vkvideosearch.com/video.php?v=%s_%s' % (urlparse.parse_qs(urlparse.urlparse(base).query)['oid'][0], urlparse.parse_qs(urlparse.urlparse(base).query)['id'][0])
        except: pass
        result = str(client.request(s))

        u = re.compile('<a href="(.+?)">(720|540|480|360|240)p</a>').findall(result)

        url = []
        try: url += [[{'quality': 'HD', 'url': i[0]} for i in u if i[1] == '720'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[0]} for i in u if i[1] == '540'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[0]} for i in u if i[1] == '480'][0]]
        except: pass
        if not url == []: return url
        try: url += [[{'quality': 'SD', 'url': i[0]} for i in u if i[1] == '360'][0]]
        except: pass
        if not url == []: return url
        try: url += [[{'quality': 'SD', 'url': i[0]} for i in u if i[1] == '240'][0]]
        except: pass

        if not url == []: return url

    except:
        return

