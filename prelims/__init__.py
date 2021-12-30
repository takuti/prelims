from .processors.recommender import Recommender
from .utils import load_posts, save_posts

import os


def process(path_dir, permalink_base='', tokenizer=None, custom_processors=[]):
    assert os.path.isdir(os.path.expanduser(path_dir)), \
            f'path {path_dir} is not a directory or does not exist'
    paths = [os.path.join(path_dir, f) for f in os.listdir(path_dir)]

    posts = load_posts(paths)

    recommender = Recommender(permalink_base=permalink_base, topk=3,
                              tokenizer=tokenizer)
    recommender.process(posts)
    for processor in custom_processors:
        processor.process(posts)

    save_posts(posts)
