from .base import BaseFrontMatterProcessor

import subprocess


class LastModifiedDateExtractor(BaseFrontMatterProcessor):

    """Get last modified date based on git last commit date, or `date -r` if
    the file is not committed.
    """

    def __init__(self):
        pass

    def process(self, posts, allow_overwrite=True):
        for post in posts:
            cmd = "git log -1 --format='%ad' --date=format:'%Y-%m-%d' " + \
                    str(post.path)
            date = self.__read_stdout(cmd)
            if len(date) == 0:
                cmd = f"date -r {post.path} +'%Y-%m-%d'"
                date = self.__read_stdout(cmd)
            post.update("lastmod", date, allow_overwrite)

    def __read_stdout(self, cmd):
        """Run a shell command and get STDOUT.
        """
        return subprocess.check_output(cmd, shell=True,
                                       encoding="utf-8").rstrip()
