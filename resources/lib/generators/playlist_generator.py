# -*- coding: utf-8 -*-
"""Generate playlist based on available channels"""
from lib.providers import ProviderInterface

class PlaylistGenerator:
    """This class provides tools to generate a playlist based on the given channel information"""

    def __init__(self, provider):
        self.entries = ['#EXTM3U tvg-shift=0', '']
        self.provider = provider
        self._load_streams()

    # pylint: disable=line-too-long
    def _load_streams(self):
        """Load streams from provider"""

        stream_template = [
            '## {name}',
            '#EXTINF:-1 tvg-name="{name}" tvg-id="{id}" tvg-logo="{logo}" tvg-chno="{chno}" group-title="Orange TV France;{group}",{name}',
            '{stream}',
            ''
        ]

        for stream in self.provider.get_streams():
            self.entries.append(stream_template[0].format(name=stream['name']))
            self.entries.append(stream_template[1].format(
                name=stream['name'],
                id=stream['id'],
                logo=stream['logo'],
                chno=stream['preset'],
                group=','.join(stream['group'])
            ))
            self.entries.append(stream_template[2].format(stream=stream['stream']))
            self.entries.append(stream_template[3])

    def write(self, filepath):
        """Write the loaded channels into M3U8 file"""
        with open(filepath, 'wb') as file:
            file.writelines('{}\n'.format(entry).encode('utf-8') for entry in self.entries)
