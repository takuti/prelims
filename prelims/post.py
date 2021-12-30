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

    def __init__(self, path, front_matter, raw_content, content):
        self.path = path
        self.front_matter = front_matter
        self.raw_content = raw_content
        self.content = content

    def update(self, key, value, allow_overwrite=False):
        if key in self.front_matter and not allow_overwrite:
            return
        self.front_matter[key] = value

    def is_draft(self):
        # avoid processing draft articles
        return 'draft' in self.front_matter and self.front_matter['draft']

    def is_valid(self):
        return self.front_matter is not None \
                and len(self.content) > 0 \
                and not self.is_draft()

    def save(self):
        if not self.is_valid():
            return

        m = RE_FRONT_MATTER.search(self.raw_content)
        with open(self.path, 'w') as f:
            content = self.raw_content.replace(
                m.group(1),
                yaml.dump(self.front_matter, allow_unicode=True,
                          default_flow_style=None)
            )
            f.write(content)

    @staticmethod
    def load(path):
        with open(path) as f:
            raw_content = f.read()

        front_matter = None
        content = raw_content

        m = RE_FRONT_MATTER.search(raw_content)

        if m is not None:
            front_matter = yaml.safe_load(m.group(1))

            # remove front matter
            content = raw_content.replace(m.group(0), '')

        for re_filter in RE_FILTERS:
            content = re_filter.sub('', content)

        return Post(path, front_matter, raw_content, content)
