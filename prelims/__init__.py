from .post import Post

import os
import re
import yaml
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RE_FRONT_MATTER = re.compile(r'---\n([\s\S]*?\n)---\n')
RE_PATH_TO_PERMALINK = re.compile(r'((/ja){0,1}/note/.+?)(\.md|\.html)')
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


def extract_contents(paths):
    for path in paths:
        with open(path) as f:
            content = f.read()

        m = RE_FRONT_MATTER.search(content)

        if m is None:
            continue

        # avoid recommending draft articles by making their contents empty
        front_matter = yaml.safe_load(m.group(1))
        if 'draft' in front_matter and front_matter['draft']:
            continue

        # remove front matter
        content = content.replace(m.group(0), '')

        for re_filter in RE_FILTERS:
            content = re_filter.sub('', content)

        yield Post(path, front_matter, content)


def path_to_permalink(path):
    return RE_PATH_TO_PERMALINK.search(path).group(1) + '/'


def recommend(posts, topk=3, tokenizer=None):
    """Content-based collaborative filtering
    """
    contents = [post.content for post in posts]
    paths = [post.path for post in posts]

    # build model
    vectorizer = TfidfVectorizer(max_df=0.95, tokenizer=tokenizer)

    tfidf = vectorizer.fit_transform(contents)

    indices = tfidf.toarray().argsort(axis=1, kind='stable')[:, ::-1]
    keywords = np.array(vectorizer.get_feature_names_out())[indices]

    similarities = cosine_similarity(tfidf)

    for i in range(len(contents)):
        # find top-k most-similar articles
        # (except for target article itself which is similarity=1.0)
        top_indices = np.argsort(
            similarities[i, :], kind='stable')[::-1][1:(topk + 1)]
        recommend_permalinks = [
            path_to_permalink(paths[j]) for j in top_indices
        ]

        posts[i].update('keywords', keywords[i, :10].tolist(), allow_overwrite=True)
        posts[i].update('recommendations', recommend_permalinks, allow_overwrite=True)


def update_front_matter(posts):
    for post in posts:
        path = post.path

        with open(path) as f:
            content = f.read()

        m = RE_FRONT_MATTER.search(content)
        if m is None:
            return

        with open(path, 'w') as f:
            f.write(content.replace(
                m.group(1),
                yaml.dump(post.front_matter, allow_unicode=True,
                          default_flow_style=None)))


def process(path_dir, tokenizer=None, custom_funcs=[]):
    assert os.path.isdir(os.path.expanduser(path_dir)), \
            f'path {path_dir} is not a directory or does not exist'
    paths = [os.path.join(path_dir, f) for f in os.listdir(path_dir)]

    posts = list(extract_contents(paths))

    recommend(posts, topk=3, tokenizer=tokenizer)
    for func in custom_funcs:
        func(posts)

    update_front_matter(posts)
