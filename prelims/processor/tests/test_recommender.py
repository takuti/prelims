from prelims import Post
from prelims.processor import Recommender

from unittest import TestCase

import os
from pathlib import Path

class RecommenderTestCase(TestCase):

    def setUp(self):
        # file paths
        self.path_a = Path(f'{os.sep}path').joinpath('to', 'articles', 'a.md')
        self.path_b = Path(f'{os.sep}path').joinpath('to', 'articles', 'b.md')
        self.path_c = Path(f'{os.sep}path').joinpath('to', 'articles', 'c', 'index.md')
        self.path_d = Path(f'{os.sep}path').joinpath('to', 'articles', 'D.md')

        # urls
        self.permalink_base = '/diary/post'
        self.permalink_a = '/diary/post/a/'
        self.permalink_b = '/diary/post/b/'
        self.permalink_c = '/diary/post/c/'
        self.permalink_d = '/diary/post/d/'

    def test_process(self):
        post_a = Post(self.path_a, {'title': 'foo'},
                      '', 'Hello world.', 'utf-8')
        post_b = Post(self.path_b, {'title': 'bar'},
                      '', 'This is a pen.', 'utf-8')
        post_c = Post(self.path_c, {'title': 'buzz'},
                      '', 'There is a man in the high castle.', 'utf-8')
        post_d = Post(self.path_d, {'title': 'qux'},
                      '', 'Greatest showman was there.', 'utf-8')
        posts = [post_a, post_b, post_c, post_d]

        recommender = Recommender(permalink_base=self.permalink_base,
                                  stop_words='english', lower_path=True)
        recommender.process(posts)

        # sort alphabetically since the order may differ
        post_a.front_matter['keywords'] = sorted(
            post_a.front_matter['keywords'])
        self.assertEqual(post_a.front_matter, {
            'title': 'foo',
            'recommendations': [self.permalink_d, self.permalink_c, self.permalink_b],
            'keywords': [
                'castle',
                'greatest',
                'hello',
                'high',
                'man',
                'pen',
                'showman',
                'world'
            ]
        })

        post_b.front_matter['keywords'] = sorted(
            post_b.front_matter['keywords'])
        self.assertEqual(post_b.front_matter, {
            'title': 'bar',
            'recommendations': [self.permalink_d, self.permalink_c, self.permalink_a],
            'keywords': [
                'castle',
                'greatest',
                'hello',
                'high',
                'man',
                'pen',
                'showman',
                'world'
            ]
        })

        post_c.front_matter['keywords'] = sorted(
            post_c.front_matter['keywords'])
        self.assertEqual(post_c.front_matter, {
            'title': 'buzz',
            'recommendations': [self.permalink_d, self.permalink_b, self.permalink_a],
            'keywords': [
                'castle',
                'greatest',
                'hello',
                'high',
                'man',
                'pen',
                'showman',
                'world'
            ]
        })

        post_d.front_matter['keywords'] = sorted(
            post_d.front_matter['keywords'])
        self.assertEqual(post_d.front_matter, {
            'title': 'qux',
            'recommendations': [self.permalink_c, self.permalink_b, self.permalink_a],
            'keywords': [
                'castle',
                'greatest',
                'hello',
                'high',
                'man',
                'pen',
                'showman',
                'world'
            ]
        })

        post_b.content = "It's an apple"

        # nothing should change
        recommender.process(posts, allow_overwrite=False)
        post_b.front_matter['keywords'] = sorted(
            post_b.front_matter['keywords'])
        self.assertEqual(post_b.front_matter, {
            'title': 'bar',
            'recommendations': [self.permalink_d, self.permalink_c, self.permalink_a],
            'keywords': [
                'castle',
                'greatest',
                'hello',
                'high',
                'man',
                'pen',
                'showman',
                'world'
            ]
        })

        # keyword "pen" in article B should be overwritten by "apple"
        recommender.process(posts, allow_overwrite=True)
        post_b.front_matter['keywords'] = sorted(
            post_b.front_matter['keywords'])
        self.assertEqual(post_b.front_matter, {
            'title': 'bar',
            'recommendations': [self.permalink_d, self.permalink_c, self.permalink_a],
            'keywords': [
                'apple',
                'castle',
                'greatest',
                'hello',
                'high',
                'man',
                'showman',
                'world'
            ]
        })
