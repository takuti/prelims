from .post import Post

import os


class StaticSitePostsHandler(object):

    def __init__(self, path_dir):
        assert os.path.isdir(os.path.expanduser(path_dir)), \
            f'path {path_dir} is not a directory or does not exist'

        self.paths = [os.path.join(path_dir, f) for f in os.listdir(path_dir)]
        self.processors = []

    def register_processor(self, processor):
        """Add a front matter processor to the queue.
        """
        self.processors.append(processor)

    def execute(self):
        """Load all posts under the document root, process front matters, and
        write the results onto the original files.
        """
        posts = self.load_posts()
        for processor in self.processors:
            processor.process(posts)
        self.save_posts(posts)

    def load_posts(self):
        """Get a list of posts under the document root, excluding invalid posts
        e.g., draft articles, empty files.
        """
        posts = []
        for path in self.paths:
            post = Post.load(path)
            if post.is_valid():
                posts.append(post)
        return posts

    @staticmethod
    def save_posts(posts):
        """Call a save operation for given posts.
        """
        for post in posts:
            post.save()
