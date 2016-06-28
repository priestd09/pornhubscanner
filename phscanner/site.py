"""This module contains a class for every supported site (only Pornhub
for now). Each class contains the instructions and the correct values
for retrieving the site informations, like the list of the titles
contained in a page, the address of the page containing a video direct
url, and the direct url itself."""

import re
from bs4 import BeautifulSoup
from urllib.parse import unquote
from urllib.request import urlopen


class PHub(object):
    home = 'http://www.pornhub.com'
    path = '/video'
    query = 'page='
    tags = 'a', {'class': 'img'}
    regex = re.compile(
        r'var player[\w_]*\d{3}p = \\\'(http[://\.\w\?=&]*)',
        re.IGNORECASE
    )

    def __init__(self, page=1):
        self.page = page

    def get_page_url(self):
        url = ''.join([PHub.home, PHub.path, '?', PHub.query + str(self.page)])
        return url

    def get_body(self):
        with urlopen(self.get_page_url()) as html:
            sp = BeautifulSoup(html, 'html.parser')
            body = [i for i in sp.find_all(*PHub.tags) if i.has_attr('title')]
        return body

    def get_catalogue(self):
        video_page_urls = {}
        for i in self.get_body():
            video_page_urls[i.get('title')] = i.get('href')
        return video_page_urls

    def get_video_url(self, video_page_url):
        with urlopen(PHub.home + video_page_url) as html:
            match = re.search(PHub.regex, str(html.read()))
        video_url = unquote(re.sub('&amp', '', match.group(1)))
        return video_url
