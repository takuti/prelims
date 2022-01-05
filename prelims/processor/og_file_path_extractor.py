from .base import BaseFrontMatterProcessor

import re


class OpenGraphFilePathExtractor(BaseFrontMatterProcessor):

    def __init__(self, image_base=None, audio_base=None, video_base=None):
        self.pattern = dict()
        if image_base is not None:
            self.pattern['images'] = re.compile(
                rf'{re.escape(image_base)}/.+?(?:\.jpg|\.jpeg|\.png)'
            )

        if audio_base is not None:
            self.pattern['audio'] = re.compile(
                rf'{re.escape(audio_base)}/.+?(?:\.mp3|\.wav)'
            )

        if video_base is not None:
            self.pattern['videos'] = re.compile(
                rf'{re.escape(video_base)}/.+?(?:\.mp4|\.mov)'
            )

    def process(self, posts):
        for post in posts:
            for key, re_path in self.pattern.items():
                paths = re_path.findall(post.content)
                if len(paths) == 0:
                    continue
                post.update(key, paths)
