# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
import json


class MycujooIE(InfoExtractor):
    _VALID_URL = r'https?://mycujoo\.tv/video/la-roma\?id=(?P<id>[^?#/]+)'

    _IS_LIVE_URL = 'https://api.mycujoo.tv/events/'
    _INFO_RE = r'window._d = {(?P<info>.*)};'

    _TEST = {
        'url': 'https://mycujoo.tv/video/la-roma?id=cjg4k1h8k00033k6js1qqfi1e',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '337',
            'ext': 'm3u8'
        }
    }

    def _real_extract(self, url):
        html = self._download_webpage(url, 'id')
        info = self._html_search_regex( self._INFO_RE, html, 'info')
        infoDict = self._parse_json(unicode('{'+info+'}'), 'id')
        title = ''
        descr = ''
        print json.dumps(infoDict, indent=4)
        isLive = False
        if not 'live' in infoDict:
            isLive = False
            title = infoDict['channel']['name']
        else:
            if 'id' in infoDict['live']:
                ID = infoDict['live']['id']
                isLive = self._download_json(self._IS_LIVE_URL + ID + "/is_live",note='Checking if stream live',)
            title = infoDict['live']['title']
            descr = infoDict['live']['descr']
        formats = []
        if 'url_hls' in infoDict['channel']:
            formats = self._extract_m3u8_formats(infoDict['channel']['url_hls'], 'id',
                              entry_protocol='m3u8', fatal=True, live=isLive)

        return {
            'id': 'id',
            'title': title,
            'description': descr,
            'formats': formats,
            # TODO more properties (see youtube_dl/extractor/common.py)
        }
