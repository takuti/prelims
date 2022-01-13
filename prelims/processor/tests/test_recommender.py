from prelims import Post
from prelims.processor import Recommender

from unittest import TestCase

import os


class RecommenderTestCase(TestCase):

    def setUp(self):
        # file paths
        self.path_a = os.path.abspath(
                os.path.join(os.sep, 'path', 'to', 'articles', 'a.md'))
        self.path_b = os.path.abspath(
                os.path.join(os.sep, 'path', 'to', 'articles', 'b.md'))

        # urls
        self.permalink_base = '/diary/post'
        self.permalink_a = '/diary/post/a/'
        self.permalink_b = '/diary/post/b/'

    def test_process(self):
        post_a = Post(self.path_a, {'title': 'foo'},
                      '', 'Hello world.', 'utf-8')
        post_b = Post(self.path_b, {'title': 'bar'},
                      '', 'This is a pen.', 'utf-8')
        posts = [post_a, post_b]

        recommender = Recommender(permalink_base=self.permalink_base,
                                  stop_words='english')
        recommender.process(posts)

        # sort alphabetically since the order may differ
        post_a.front_matter['keywords'] = sorted(
            post_a.front_matter['keywords'])
        self.assertEqual(post_a.front_matter, {
            'title': 'foo',
            'recommendations': [self.permalink_b],
            'keywords': ['hello', 'pen', 'world']
        })

        post_b.front_matter['keywords'] = sorted(
            post_b.front_matter['keywords'])
        self.assertEqual(post_b.front_matter, {
            'title': 'bar',
            'recommendations': [self.permalink_a],
            'keywords': ['hello', 'pen', 'world']
        })
