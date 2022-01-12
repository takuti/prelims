from .base import BaseFrontMatterProcessor

import re
import numpy as np
from pathlib import PurePosixPath
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender(BaseFrontMatterProcessor):

    """Tokenize contents, extract keywords, and generate a list of recommended
    article paths.


    Parameters
    ----------
    permalink_base : str, default=''
        Part of your article path (i.e., directory) that is directly used in
        the permalinks. For example, if the articles are under
        ``/path/to/posts`` and your website eventually gives permalinks like
        ``https://awesome-website.com/posts/article-aaa/``, it means
        ``permalink_base='/posts'``; path and permalink share the same
        ``/posts`` portion.

    topk : int, default=3
        Number of recommended articles.

    **kwargs : dict
        Keyword arguments to be used to initialize sklearn's
        ``TfidfVectorizer``.

    Notes
    -----
    One possibility of using ``**kwargs`` is to explicitly provide
    ``stop_words`` so the processor can filter out meaningless terms (e.g.,
    'is', 'this', 'of'). Besides sklearn's ``stop_words='english'``, you could
    leverage an arbitrary set of words; if you have installed ``spacy`` in your
    environment, for example, their stop word list will give wider coverage of
    words.

    Examples
    --------
    >>> from prelims import Post
    >>> from prelims.processor import Recommender
    >>> from spacy.lang import en
    >>> post_a = Post('/path/to/posts/a.md', {'title': 'foo'},
    ...               '---\ntitle: foo\n---\n\nHellow world.',
    ...               'Hello world.')
    >>> post_b = Post('/path/to/posts/b.md', {'title': 'bar'},
    ...               '---\ntitle: bar\n---\n\nThis is a pen.',
    ...               'This is a pen.')
    >>> recommender = Recommender(permalink_base='/posts',
    ...                           stop_words=en.STOP_WORDS)
    >>> recommender.process([post_a, post_b])
    >>> post_a.front_matter.keywords
    ['world', 'hello', 'pen']
    >>> post_a.front_matter.recommendations
    ['/posts/b/']
    >>> post_b.front_matter.keywords
    ['pen', 'world', 'hello']
    >>> post_b.front_matter.recommendations
    ['/posts/a/']
    """

    def __init__(self, permalink_base='', topk=3, **kwargs):
        self.permalink_base = permalink_base
        self.topk = topk

        vectorizer_kwargs = TfidfVectorizer.__init__.__kwdefaults__
        for arg, value in kwargs.items():
            if arg in vectorizer_kwargs:
                vectorizer_kwargs[arg] = value
        self.vectorizer_kwargs = vectorizer_kwargs

    def process(self, posts):
        """Extract keywords and generate a list of recommended articles
        based on the content-based filtering technique.
        """
        contents = [post.content for post in posts]
        paths = [post.path for post in posts]

        # build model
        vectorizer = TfidfVectorizer(**self.vectorizer_kwargs)

        tfidf = vectorizer.fit_transform(contents)

        indices = tfidf.toarray().argsort(axis=1, kind='stable')[:, ::-1]
        keywords = np.array(vectorizer.get_feature_names_out())[indices]

        similarities = cosine_similarity(tfidf)

        for i in range(len(contents)):
            # find top-k most-similar articles
            # (except for target article itself which is similarity=1.0)
            top_indices = np.argsort(
                similarities[i, :], kind='stable')[::-1][1:(self.topk + 1)]
            recommend_permalinks = [
                self.__path_to_permalink(paths[j]) for j in top_indices
            ]

            posts[i].update('keywords', keywords[i, :10].tolist(),
                            allow_overwrite=True)
            posts[i].update('recommendations', recommend_permalinks,
                            allow_overwrite=True)

    def __path_to_permalink(self, path):
        """Extract a permalink portion of a file path, excluding a file extension.
        """
        pattern = rf'({re.escape(self.permalink_base)}/.+?)(\.md|\.html)'
        return re.search(pattern, str(PurePosixPath(path))).group(1) + '/'
