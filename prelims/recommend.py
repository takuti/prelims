import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RE_PATH_TO_PERMALINK = re.compile(r'((/ja){0,1}/note/.+?)(\.md|\.html)')


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
