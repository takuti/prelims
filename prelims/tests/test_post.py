from prelims import Post

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

content_draft = """
---
aaa: yyy
bbb: yyy
draft: true
---

This is draft content to be ignored.
"""

# A post that quotes its own front matter in the body
content_quoting = """
---
aaa: xxx
---

Hello world. Every post starts with:

---
aaa: xxx
---
"""

content_block_style = """
---
aaa: xxx
bbb:
  - xxx
  - yyy
---

Hello world.
"""


class PostTestCase(TestCase):

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
        self.mdfile_quoting = tempfile.NamedTemporaryFile(suffix='.md',
                                                          dir=self.dir.name,
                                                          delete=False)
        self.mdfile_quoting.write(content_quoting.encode('utf-8'))
        self.mdfile_quoting.seek(0)
        self.mdfile_block_style = tempfile.NamedTemporaryFile(
            suffix='.md', dir=self.dir.name, delete=False)
        self.mdfile_block_style.write(content_block_style.encode('utf-8'))
        self.mdfile_block_style.seek(0)

    def tearDown(self):
        self.mdfile.close()
        os.unlink(self.mdfile.name)
        self.mdfile_draft.close()
        os.unlink(self.mdfile_draft.name)
        self.mdfile_quoting.close()
        os.unlink(self.mdfile_quoting.name)
        self.mdfile_block_style.close()
        os.unlink(self.mdfile_block_style.name)
        self.dir.cleanup()

    def test_load(self):
        post = Post.load(self.mdfile.name, "utf-8")
        self.assertEqual(post.path, self.mdfile.name)
        self.assertEqual(post.front_matter, {'aaa': 'xxx', 'ccc': 'xxx', 'bbb': ['xxx']})
        self.assertEqual(post.raw_content, content)
        self.assertEqual(post.content, 'Hello world.')

    def test_is_draft(self):
        post = Post.load(self.mdfile.name, "utf-8")
        self.assertFalse(post.is_draft())
        post_draft = Post.load(self.mdfile_draft.name)
        self.assertTrue(post_draft.is_draft())

    def test_is_valid(self):
        post = Post.load(self.mdfile.name, "utf-8")
        self.assertTrue(post.is_valid())
        post_draft = Post.load(self.mdfile_draft.name)
        self.assertFalse(post_draft.is_valid())

    def test_update(self):
        post = Post.load(self.mdfile.name, "utf-8")

        post.update('aaa', 'zzz', allow_overwrite=False)
        post.update('bbb', ['zzz'], allow_overwrite=True)
        post.update('foo', 'bar')

        self.assertEqual(post.path, self.mdfile.name)
        self.assertEqual(post.front_matter,
                         {'aaa': 'xxx', 'ccc': 'xxx', 'bbb': ['zzz'], 'foo': 'bar'})

    def test_save(self):
        post = Post.load(self.mdfile.name, "utf-8")
        post.update('foo', 'bar')
        post.save()

        expected_content = """
---
aaa: xxx
ccc: xxx
bbb: [xxx]
foo: bar
---

Hello world.
"""

        self.assertEqual(
            '\n'.join(self.mdfile.read().decode().splitlines()) + '\n',
            expected_content)

    def test_load_keeps_quoted_front_matter(self):
        post = Post.load(self.mdfile_quoting.name, "utf-8")
        self.assertEqual(post.front_matter, {'aaa': 'xxx'})
        self.assertEqual(post.content,
                         'Hello world. Every post starts with:\n\n'
                         '---\naaa: xxx\n---')

    def test_save_keeps_quoted_front_matter(self):
        post = Post.load(self.mdfile_quoting.name, "utf-8")
        post.update('foo', 'bar')
        post.save()

        expected_content = """
---
aaa: xxx
foo: bar
---

Hello world. Every post starts with:

---
aaa: xxx
---
"""

        self.assertEqual(
            '\n'.join(self.mdfile_quoting.read().decode().splitlines()) + '\n',
            expected_content)

    def test_save_unchanged(self):
        post = Post.load(self.mdfile_block_style.name, "utf-8")

        # No-op since `aaa` is already set
        post.update('aaa', 'zzz', allow_overwrite=False)
        post.save()

        # `bbb` stays block style instead of becoming `[xxx, yyy]`
        with open(self.mdfile_block_style.name, encoding='utf-8') as f:
            self.assertEqual(f.read(), content_block_style)

    def test_save_changed(self):
        post = Post.load(self.mdfile_block_style.name, "utf-8")

        # Overwriting `aaa` is a real update, so the file is rewritten
        post.update('aaa', 'zzz', allow_overwrite=True)
        post.save()

        expected_content = """
---
aaa: zzz
bbb: [xxx, yyy]
---

Hello world.
"""

        with open(self.mdfile_block_style.name, encoding='utf-8') as f:
            self.assertEqual(f.read(), expected_content)
