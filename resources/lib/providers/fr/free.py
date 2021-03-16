# -*- coding: utf-8 -*-
"""Free"""
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from lib.providers.provider_interface import ProviderInterface
from lib.utils import log, LogLevel, random_ua

class FreeProvider(ProviderInterface):
    """Free Provider"""

    def get_stream_info(self, channel_id: int) -> dict:
        return {}

    def get_streams(self) -> list:
        endpoint = 'http://mafreebox.freebox.fr/freeboxtv/playlist.m3u'

        req = Request(endpoint, headers={
            'User-Agent': random_ua(),
            'Host': urlparse(endpoint).netloc
        })

        res = urlopen(req)

        channels = re.findall(
            r"\#EXTINF:0,(\d+) - ([A-Za-z0-9\s]+)\s\(auto\)\n(rtsp://mafreebox.freebox.fr/fbxtv_pub/stream\?namespace=1&service=(\d+))",
            res.read().decode('utf-8')
        )
        streams = []

        for channel in channels:
            streams.append({
                'id': channel[3],
                'name': channel[1],
                'preset': channel[0],
                'stream': channel[2]
            })

        log(streams, LogLevel.INFO)
        return streams

    def get_epg(self) -> dict:
        return {}