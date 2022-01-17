from .base import BaseFrontMatterProcessor

import re


class OpenGraphMediaExtractor(BaseFrontMatterProcessor):

    """Extract image, audio, and/or video paths from an article and add them to
    dedicated front matter elements as lists of permalinks.

    In particular, the processor modifies three front matter elements with
    keys: ``images``, ``audio``, and ``videos``.

    Parameters
    ----------
    image_base : str, default=None
        Non-file name part of image permalink. If an article refers to an image
        as ``/images/foo.png``, ``image_base`` is expected to be ``'/images'``.
        The extractor looks for all permalinks that match
        ``/images/*.{jpg,jpeg,png}``. Won't do anything if ``None``.

    audio_base: str, default=None
        Non-file name part of audio permalink. If an article refers to an audio
        as ``/audio/foo.mp3``, ``audio_base`` is expected to be ``'/audio'``.
        The extractor looks for all permalinks that match
        ``/audio/*.{mp3,wav}``. Won't do anything if ``None``.

    video_base: str, default=None
        Non-file name part of video permalink. If an article refers to a video
        as ``/movies/foo.mp4``, ``video_base`` is expected to be ``'/movies'``.
        The extractor looks for all permalinks that match
        ``/movies/*.{mp4,wov}``. Won't do anything if ``None``.
    """

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

    def process(self, posts, allow_overwrite=False):
        for post in posts:
            target = dict()
            for key, re_path in self.pattern.items():
                re_path = self.pattern[key]
                paths = re_path.findall(post.content)
                target[key] = paths
            post.update_all(target, allow_overwrite)
