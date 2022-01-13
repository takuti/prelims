from prelims import Post
from prelims.processor import Recommender

from unittest import TestCase


class RecommenderTestCase(TestCase):

    def test_process(self):
        post_a = Post('/path/to/posts/a.md', {'title': 'foo'},
                      '', 'Hello world.', 'utf-8')
        post_b = Post('/path/to/posts/b.md', {'title': 'bar'},
                      '', 'This is a pen.', 'utf-8')
        posts = [post_a, post_b]

        recommender = Recommender(permalink_base='/posts',
                                  stop_words='english')
        recommender.process(posts)

        # sort alphabetically since the order may differ
        post_a.front_matter['keywords'] = sorted(
            post_a.front_matter['keywords'])
        self.assertEqual(post_a.front_matter, {
            'title': 'foo',
            'recommendations': ['/posts/b/'],
            'keywords': ['hello', 'pen', 'world']
        })

        post_b.front_matter['keywords'] = sorted(
            post_b.front_matter['keywords'])
        self.assertEqual(post_b.front_matter, {
            'title': 'bar',
            'recommendations': ['/posts/a/'],
            'keywords': ['hello', 'pen', 'world']
        })
