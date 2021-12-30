from .post import Post


def load_posts(paths):
    posts = []
    for path in paths:
        post = Post.load(path)
        if post.is_valid():
            posts.append(post)
    return posts


def save_posts(posts):
    for post in posts:
        post.save()
