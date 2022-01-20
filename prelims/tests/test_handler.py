from prelims import StaticSitePostsHandler
from prelims.processor import BaseFrontMatterProcessor

from unittest import TestCase
import os
import tempfile


content = """
---
aaa: xxx
bbb: [xxx]
---

Hello world.
"""

content_draft = """
---
aaa: yyy
bbb: yyy
draft: true
---

This is draft content to be ignored.
"""

content_ignore = """
---
zzz: iii
yyy: jjj
---

[Tags](/tags)
"""

class DummyProcessor(BaseFrontMatterProcessor):

    def process(self, posts):
        for post in posts:
            post.update('aaa', 'zzz', allow_overwrite=False)
            post.update('bbb', ['zzz'], allow_overwrite=True)
            post.update('foo', 'bar')


class StaticSitePostsHandlerTestCase(TestCase):

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.mdfile = tempfile.NamedTemporaryFile(suffix='.md',
                                                  dir=self.dir.name,
                                                  delete=False)
        self.mdfile.write(content.encode('utf-8'))
        self.mdfile.seek(0)
        self.mdfile_draft = tempfile.NamedTemporaryFile(suffix='.md',
                                                        dir=self.dir.name,
                                                        delete=False)
        self.mdfile_draft.write(content_draft.encode('utf-8'))
        self.mdfile_draft.seek(0)
        self.mdfile_ignore = tempfile.NamedTemporaryFile(suffix='.md',
                                                        dir=self.dir.name,
                                                        delete=False)
        self.mdfile_ignore.write(content_ignore.encode('utf-8'))
        self.mdfile_ignore.seek(0)

    def tearDown(self):
        self.mdfile.close()
        os.unlink(self.mdfile.name)
        self.mdfile_draft.close()
        os.unlink(self.mdfile_draft.name)
        self.mdfile_ignore.close()
        os.unlink(self.mdfile_ignore.name)
        self.dir.cleanup()

    def test_register_processor(self):
        handler = StaticSitePostsHandler(self.dir.name)
        self.assertEqual(len(handler.processors), 0)
        handler.register_processor(DummyProcessor())
        self.assertEqual(len(handler.processors), 1)

    def test_load_posts(self):
        handler = StaticSitePostsHandler(
            self.dir.name,
            ignore_files=[os.path.basename(self.mdfile_ignore.name)])
        posts = handler.load_posts()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].front_matter, {'aaa': 'xxx', 'bbb': ['xxx']})

    def test_load_posts_without_ignorance(self):
        handler = StaticSitePostsHandler(self.dir.name)
        posts = handler.load_posts()
        self.assertEqual(len(posts), 2)

    def test_load_posts_lower_path(self):
        handler = StaticSitePostsHandler(self.dir.name, lower_path=False)
        handler.register_processor(DummyProcessor())
        self.assertEqual(len(handler.processors), 1)
        self.assertEqual(handler.processors[0].lower_path, False)

    def test_execute(self):
        handler = StaticSitePostsHandler(self.dir.name)
        handler.register_processor(DummyProcessor())
        handler.execute()

        # 'aaa' was not overrode
        expected_content = """
---
aaa: xxx
bbb: [zzz]
foo: bar
---

Hello world.
"""
        self.assertEqual(
            '\n'.join(self.mdfile.read().decode().splitlines()) + '\n',
            expected_content)
