from prelims import Post
from prelims.processor import Recommender

from unittest import TestCase


class RecommenderTestCase(TestCase):

    def test_process(self):
        post_a = Post('/path/to/posts/a.md', {'title': 'foo'},
                      '', 'Hello world.')
        post_b = Post('/path/to/posts/b.md', {'title': 'bar'},
                      '', 'This is a pen.')
        posts = [post_a, post_b]

        recommender = Recommender(permalink_base='/posts')
        recommender.process(posts)

        # sort alphabetically since the order may differ
        post_a.front_matter['keywords'] = sorted(
            post_a.front_matter['keywords'])
        self.assertEqual(post_a.front_matter, {
            'title': 'foo',
            'recommendations': ['/posts/b/'],
            'keywords': ['hello', 'is', 'pen', 'this', 'world']
        })

        post_b.front_matter['keywords'] = sorted(
            post_b.front_matter['keywords'])
        self.assertEqual(post_b.front_matter, {
            'title': 'bar',
            'recommendations': ['/posts/a/'],
            'keywords': ['hello', 'is', 'pen', 'this', 'world']
        })
