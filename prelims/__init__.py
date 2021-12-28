from .post import Post
from .recommend import recommend

import os


def extract_contents(paths):
    posts = []
    for path in paths:
        with open(path) as f:
            raw_content = f.read()

        post = Post.create(path, raw_content)
        if post.is_valid():
            posts.append(post)
    return posts


def update_front_matter(posts):
    for post in posts:
        post.save()


def process(path_dir, tokenizer=None, custom_funcs=[]):
    assert os.path.isdir(os.path.expanduser(path_dir)), \
            f'path {path_dir} is not a directory or does not exist'
    paths = [os.path.join(path_dir, f) for f in os.listdir(path_dir)]

    posts = extract_contents(paths)

    recommend(posts, topk=3, tokenizer=tokenizer)
    for func in custom_funcs:
        func(posts)

    update_front_matter(posts)
