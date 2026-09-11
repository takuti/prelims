from prelims import Post
from prelims.processor import LastModifiedDateExtractor

from unittest import TestCase

import os
import subprocess
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
        self.mdfile.close()

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

    def test_process_content_change(self):
        self._init_git()
        self._commit('Initial content', '2020-01-02T00:00:00+0000')

        with open(self.mdfile.name, 'w', encoding='utf-8') as f:
            f.write("""
---
aaa: xxx
ccc: xxx
bbb: [xxx]
---
Good morning.
""")
        self._commit('Change content', '2020-02-03T00:00:00+0000')

        lastmod = self._lastmod_in_temp_dir(skip_front_matter=True)
        self.assertEqual('2020-02-03', lastmod)

    def test_process_skips_front_matter_only_change(self):
        self._init_git()
        self._commit('Initial content', '2020-01-02T00:00:00+0000')

        with open(self.mdfile.name, 'w', encoding='utf-8') as f:
            f.write("""
---
aaa: changed
ccc: xxx
bbb: [xxx]
---
Hello world.
""")
        self._commit('Change front matter', '2020-02-03T00:00:00+0000')

        lastmod = self._lastmod_in_temp_dir(skip_front_matter=True)
        self.assertEqual('2020-01-02', lastmod)

    def test_process_uses_front_matter_only_change(self):
        self._init_git()
        self._commit('Initial content', '2020-01-02T00:00:00+0000')

        with open(self.mdfile.name, 'w', encoding='utf-8') as f:
            f.write("""
---
aaa: changed
ccc: xxx
bbb: [xxx]
---
Hello world.
""")
        self._commit('Change front matter', '2020-02-03T00:00:00+0000')

        lastmod = self._lastmod_in_temp_dir(skip_front_matter=False)
        self.assertEqual('2020-02-03', lastmod)

    def _init_git(self):
        subprocess.check_call(['git', 'init'], cwd=self.dir.name,
                              stdout=subprocess.DEVNULL)
        subprocess.check_call(['git', 'config', 'user.email',
                               'test@example.com'], cwd=self.dir.name)
        subprocess.check_call(['git', 'config', 'user.name', 'Test User'],
                              cwd=self.dir.name)

    def _commit(self, message, date):
        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = date
        env['GIT_COMMITTER_DATE'] = date
        subprocess.check_call(['git', 'add', os.path.basename(self.mdfile.name)],
                              cwd=self.dir.name, stdout=subprocess.DEVNULL)
        subprocess.check_call(['git', 'commit', '-m', message],
                              cwd=self.dir.name, env=env,
                              stdout=subprocess.DEVNULL)

    def _lastmod_in_temp_dir(self, skip_front_matter):
        original_dir = os.getcwd()
        try:
            # run in the temp directory to ensure git commands are executed in the correct context
            os.chdir(self.dir.name)
            extractor = LastModifiedDateExtractor(skip_front_matter=skip_front_matter)
            p = Post.load(self.mdfile.name, "utf-8")

            extractor.process([p], allow_overwrite=False)
        finally:
            os.chdir(original_dir)
        return p.front_matter['lastmod']
