from .base import BaseFrontMatterProcessor

from datetime import datetime
import os
import platform
import subprocess


class LastModifiedDateExtractor(BaseFrontMatterProcessor):

    """Get last modified date based on git last commit date, or file metadata
    if the file is not committed.
    """

    def __init__(self):
        pass

    def process(self, posts, allow_overwrite=True):
        for post in posts:
            try:
                cmd = "git log -1 --format='%ad' --date=format:'%Y-%m-%d' " + \
                        str(post.path)
                date = self.__read_stdout(cmd)
            except RuntimeError:
                date = self.__get_file_mtime(post.path)
            else:
                if len(date) == 0:
                    date = self.__get_file_mtime(post.path)
            post.update("lastmod", date, allow_overwrite)

    def __read_stdout(self, cmd):
        """Run a shell command and get STDOUT.
        """
        try:
            return subprocess.check_output(cmd, shell=True,
                                           encoding="utf-8").rstrip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e)

    def __get_file_mtime(self, path):
        """https://stackoverflow.com/questions/237079/
        """
        if platform.system() == 'Windows':
            ts = os.path.getmtime(path)
        else:
            ts = os.stat(path).st_mtime
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
