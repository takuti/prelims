import re
import yaml

RE_FRONT_MATTER = re.compile(r'---\n([\s\S]*?\n)---\n')
RE_FILTERS = [
    # HTML tag
    re.compile(r'<.*?>'),
    # Markdown codefence / math block
    re.compile(r'^(\$\$|```)(.*)\n(.*\n)+(\$\$|```)', re.MULTILINE),
    # inline math
    re.compile(r'\$(.*)\$'),
    # URL
    re.compile(r'https?:\/\/[\S]+')
]


class Post(object):

    def __init__(self, path, front_matter, raw_content, content,
                 encoding='utf-8'):
        self.path = path
        self.front_matter = front_matter
        self.raw_content = raw_content
        self.content = content
        self.encoding = encoding

    def update(self, key, value, allow_overwrite=False):
        """Update value of a specific front matter element.

        Parameters
        ----------
        key : str
            Front matter key to update.

        value : str or list
            Updated value of the target key.

        allow_overwrite : bool, default=False
            What to do if the target key already exisits. Its value is
            overwritten when ``allow_overwrite=True``.
        """
        if key in self.front_matter and not allow_overwrite:
            return
        if value is None or len(value) == 0:
            return
        self.front_matter[key] = value

    def update_all(self, target, allow_overwrite=False):
        """Update multiple keys in the front matter all at once.

        Parameters
        ----------
        target : dict
            Updated front matter key-value pairs.

        allow_overwrite : bool, default=False
            If True, all keys in ``target`` are first cleared from the current
            front matter, then their values are freshly inserted. Otherwise,
            delegate every single key-value pair to ``update`` one-by-one.
        """
        if allow_overwrite:
            self.__remove_all(target.keys())

        for key, value in target.items():
            self.update(key, value, allow_overwrite)

    def is_draft(self):
        # avoid processing draft articles
        return ('draft' in self.front_matter and self.front_matter['draft']) \
                or ('published' in self.front_matter and
                    not self.front_matter['published'])

    def is_valid(self):
        return self.front_matter is not None \
                and len(self.content) > 0 \
                and not self.is_draft()

    def save(self):
        if not self.is_valid():
            return

        m = RE_FRONT_MATTER.search(self.raw_content)
        # Don't expand array value to markdown-style list notation
        # https://github.com/yaml/pyyaml/pull/256
        value_types = {type(value) for value in self.front_matter.values()}
        flow_style = None if list in value_types else False
        with open(self.path, 'w', encoding=self.encoding) as f:
            content = self.raw_content.replace(
                m.group(1),
                yaml.dump(self.front_matter, allow_unicode=True,
                          default_flow_style=flow_style,
                          sort_keys=False)
            )
            f.write(content)

    @staticmethod
    def load(path, encoding="utf-8"):
        with open(path, encoding=encoding) as f:
            raw_content = f.read()

        front_matter = None
        content = raw_content

        m = RE_FRONT_MATTER.search(raw_content)

        if m is not None:
            front_matter = yaml.safe_load(m.group(1))

            # remove front matter
            content = raw_content.replace(m.group(0), '')

        for re_filter in RE_FILTERS:
            content = re_filter.sub('', content).strip()

        return Post(path, front_matter, raw_content, content, encoding)

    def __remove(self, key):
        """Delete a specific front matter element.

        Parameters
        ----------
        key : str
            Front matter key to delete.
        """
        if key in self.front_matter:
            del self.front_matter[key]

    def __remove_all(self, keys):
        """Delete multiple front matter elements.

        Parameters
        ----------
        keys : list
            Front matter keys to delete.
        """
        for key in keys:
            self.__remove(key)
