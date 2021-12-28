class Post(object):

    def __init__(self, path, front_matter, content):
        self.path = path
        self.front_matter = front_matter
        self.content = content

    def update(self, key, value, allow_overwrite=False):
        if key in self.front_matter and not allow_overwrite:
            return
        self.front_matter[key] = value