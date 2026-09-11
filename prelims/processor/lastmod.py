from .base import BaseFrontMatterProcessor
from ..post import Post

from datetime import datetime
from pathlib import Path
import git
import os
import platform


class LastModifiedDateExtractor(BaseFrontMatterProcessor):

    """Get last modified date based on git last commit date, or file metadata
    if the file is not committed.
    """

    def __init__(self, skip_front_matter=False):
        self.repo = None
        self.skip_front_matter = skip_front_matter

    def process(self, posts, allow_overwrite=True):
        try:
            for post in posts:
                try:
                    lastmod = self.__get_last_commit_date(post.path)
                    date = lastmod.strftime('%Y-%m-%d') if lastmod else ''
                except RuntimeError:
                    date = self.__get_file_mtime(post.path)
                else:
                    if len(date) == 0:
                        date = self.__get_file_mtime(post.path)
                post.update("lastmod", date, allow_overwrite)
        finally:
            if self.repo is not None:
                self.repo.close()
                self.repo = None

    def __get_last_commit_date(self, path):
        """Get the last commit date where content changed."""
        if self.repo is None:
            # Initialize repo on first use
            self.repo = git.Repo(search_parent_directories=True)

        try:
            # Ensure we have an absolute path
            abs_file_path = Path(path).resolve()

            # Get commit history for this file
            commits = list(self.repo.iter_commits(paths=str(abs_file_path)))

            # Read latest content with or without front matter
            with open(abs_file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            if self.skip_front_matter:
                _, current_body = Post.extract_front_matter(current_content)
            else:
                current_body = current_content

            # Default to now if we can't find a change date
            last_content_change = datetime.now()

            for commit in commits:
                try:
                    # Convert to posix path (forward slashes) for git tree navigation
                    relative_path = abs_file_path.relative_to(Path(self.repo.working_dir).resolve()).as_posix()
                    blob = commit.tree / relative_path

                    # Get file content at this commit
                    old_content = blob.data_stream.read().decode('utf-8')
                    # Normalize blob line endings in case Git is configured without normalization
                    old_content = old_content.replace('\r\n', '\n').replace('\r', '\n')
                    if self.skip_front_matter:
                        _, old_body = Post.extract_front_matter(old_content)
                    else:
                        old_body = old_content

                    if old_body.strip() == current_body.strip():
                        last_content_change = commit.committed_datetime
                    else:
                        # Content differs, we've found where it actually changed
                        break
                except Exception as e:
                    # File might not exist in this commit
                    break

            return last_content_change
        except Exception as e:
            print(f"Error processing {path}: {e}")
            return None

    def __get_file_mtime(self, path):
        """https://stackoverflow.com/questions/237079/
        """
        if platform.system() == 'Windows':
            ts = os.path.getmtime(path)
        else:
            ts = os.stat(path).st_mtime
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
