from prelims import Post
from prelims.processor import OpenGraphMediaExtractor

from unittest import TestCase

import os
from pathlib import Path

class OpenGraphFilePathExtractorTestCase(TestCase):

    def setUp(self):
        self.post_path = Path(f'{os.sep}path').joinpath('to', 'posts', 'a.md')

    def test_process(self):
        extractor = OpenGraphMediaExtractor(
            image_base='/images', audio_base='/audio', video_base='/videos')

        p = Post(self.post_path, {'title': 'foo'},
                 '', """
                 Image:

                 ![img1](/images/foo/img1.png)

                 Audio:

                 <audio controls src="/audio/foo/music.mp3" type="audio/mpeg">
                 </audio>

                 Video:

                 <video width="320" height="240" controls>
                   <source src="/videos/foo/movie.mp4" type="video/mp4">
                   Your browser does not support the video tag.
                 </video>
                 """,
                 "utf-8")
        extractor.process([p])

        self.assertTrue('images' in p.front_matter)
        self.assertTrue('audio' in p.front_matter)
        self.assertTrue('videos' in p.front_matter)
        self.assertEqual(sorted(p.front_matter.items()),
                         sorted({
                            'title': 'foo',
                            'images': ['/images/foo/img1.png'],
                            'audio': ['/audio/foo/music.mp3'],
                            'videos': ['/videos/foo/movie.mp4']
                         }.items()))

        p.content = """
        modified contents

        ![img1](/images/foo/img2.png)
        """

        extractor.process([p], allow_overwrite=False)
        self.assertEqual(sorted(p.front_matter.items()),
                         sorted({
                            'title': 'foo',
                            'images': ['/images/foo/img1.png'],
                            'audio': ['/audio/foo/music.mp3'],
                            'videos': ['/videos/foo/movie.mp4']
                         }.items()))

        extractor.process([p], allow_overwrite=True)
        self.assertEqual(sorted(p.front_matter.items()),
                         sorted({
                            'title': 'foo',
                            'images': ['/images/foo/img2.png']
                         }.items()))
