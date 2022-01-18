from .post import Post

import os
from pathlib import Path

class StaticSitePostsHandler(object):

    def __init__(self, path_dir, ignore_files=None, encoding='utf-8'):
        assert os.path.isdir(os.path.expanduser(path_dir)), \
            f'path {path_dir} is not a directory or does not exist'

        exts = ['.md', '.html']
        self.paths = [p for p in Path(path_dir).rglob('*') if p.suffix in exts]
        self.processors = []
        self.encoding = encoding
        self.ignore_files = [] if ignore_files is None else ignore_files

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
            if path.name in self.ignore_files:
                continue

            post = Post.load(path, self.encoding)
            if post.is_valid():
                posts.append(post)
        return posts

    @staticmethod
    def save_posts(posts):
        """Call a save operation for given posts.
        """
        for post in posts:
            post.save()
