# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class SportsfixIE(InfoExtractor):
    _VALID_URL = r'https?://live\.sportsfix\.tv/stadium(?P<id>[0-9]+)'
    _BRIGHTCOVE_URL = 'https://edge.api.brightcove.com/playback/v1/accounts/5370537652001/videos/'
    _TEST = {
        'url': 'http://live.sportsfix.tv/stadium377',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '337',
            'ext': 'm3u8'
        }
    }

    def _real_extract(self, url):
        stadiumId = self._match_id(url)
        isLive = self._download_json(url + '/api/liveEventStatus', stadiumId,note='Checking if stream live',)
        if isLive['result'] != 'index-live':
            print '[Sportsfix] Stream not live'
            return {
                'id': stadiumId,
                'url': None,
                'title': None,
                'formats': []
            }
        webpage = self._download_webpage(url, stadiumId)

        policyKey = self._html_search_regex(r'policyKey: "(.*)",', webpage, 'policyKey')
        print policyKey
        videoId = self._html_search_regex(r'<link itemprop="embedURL" content="https://players\.brightcove\.net/[0-9]+/[A-z0-9_-]+/index\.html\?videoId=([0-9]+)">', webpage, 'videoId')
        print videoId
        jsonUrl = self._BRIGHTCOVE_URL + videoId
        videoJson = self._download_json(jsonUrl, stadiumId,
                       note='Downloading JSON metadata',
                       errnote='Unable to download JSON metadata',
                       fatal=True, headers={
                       'Accept': 'application/json;pk=' + policyKey
                       })

        return {
            'id': videoId,
            'title': videoJson['name'],
            'description': videoJson['description'],
            'formats': {
                'manifest_url': videoJson['sources'][0]['src'],
                'format': 'm3u8-live-master',
                'format_id': 0,
                'protocol': 'm3u8-native',
            },
            # TODO more properties (see youtube_dl/extractor/common.py)
        }