from prelims import Post
from prelims.processor import LastModifiedDateExtractor

from unittest import TestCase

import os
import tempfile


content = """
---
aaa: xxx
ccc: xxx
bbb: [xxx]
---
Hello world.
"""


class LastModifiedDateExtractorTestCase(TestCase):

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.mdfile = tempfile.NamedTemporaryFile(suffix='.md',
                                                  dir=self.dir.name,
                                                  delete=False)
        self.mdfile.write(content.encode('utf-8'))
        self.mdfile.seek(0)

    def tearDown(self):
        self.mdfile.close()
        os.unlink(self.mdfile.name)
        self.dir.cleanup()

    def test_process(self):
        extractor = LastModifiedDateExtractor()

        p = Post.load(self.mdfile.name, "utf-8")

        extractor.process([p], allow_overwrite=False)
        self.assertTrue('lastmod' in p.front_matter)
        self.assertRegex(p.front_matter['lastmod'],
                         r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
