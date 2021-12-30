from .base import BaseFrontMatterProcessor

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender(BaseFrontMatterProcessor):

    def __init__(self, permalink_base='', topk=3, tokenizer=None):
        self.permalink_base = permalink_base
        self.topk = topk
        self.tokenizer = tokenizer

    def process(self, posts):
        """Content-based filtering
        """
        contents = [post.content for post in posts]
        paths = [post.path for post in posts]

        # build model
        vectorizer = TfidfVectorizer(max_df=0.95, tokenizer=self.tokenizer)

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
        return re.search(rf'({re.escape(self.permalink_base)}/.+?)(\.md|\.html)',
                        path).group(1) + '/'