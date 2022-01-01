Prelims
===

[![Dry Run Build](https://github.com/takuti/prelims/actions/workflows/dryrun.yml/badge.svg)](https://github.com/takuti/prelims/actions/workflows/dryrun.yml) [![PyPI version](https://badge.fury.io/py/prelims.svg)](https://badge.fury.io/py/prelims)

Front matter post-processor for static site generators.

## Overview

**Prelims** eases updating YAML front matter of the static site generator contents (e.g., [Hugo](https://gohugo.io/content-management/front-matter/), [Jekyll](https://jekyllrb.com/docs/front-matter/), [Hexo](https://hexo.io/docs/front-matter.html)).

You can extract keywords based on [TF-IDF weighting](https://en.wikipedia.org/wiki/Tf%E2%80%93idf), generate a list of recommended posts by [content-based filtering](https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering), and even apply arbitrary custom functions to update front matters on-the-fly.

### Example

Below is an original front matter for "[User-Centricity Matters: My Reading List from RecSys 2021](https://takuti.me/note/recsys-2021/)" at [takuti.me](https://takuti.me/):

```yaml
---
categories: [Recommender Systems]
date: 2021-10-05
lang: en
title: 'User-Centricity Matters: My Reading List from RecSys 2021'
---
```

Once a Python script is executed against all the posts, new metadata `recommendations` and `keywords` are dynamically generated and inserted as:

```yaml
---
categories: [Recommender Systems]
date: 2021-10-05
keywords: [recsys, bias, papers, wordcloud, echo, user, recommendations, metrics,
  recommender, users]
lang: en
recommendations: [/note/recsys-2021-echo-chambers-and-filter-bubbles/, /note/recsys-wordcloud/,
  /note/ethical-challenges-in-recommender-systems/]
title: 'User-Centricity Matters: My Reading List from RecSys 2021'
---
```

## Installation

```
$ pip install prelims
```

## Usage

Assume your posts are under `/path/to/posts` where a static site generator uses as a document root:

```
posts
├── article-aaa.md
├── ...
└── article-zzz.md
```

Here, the following script reads all `.md` and `.html` files in the folder, builds recommendations, and update each post's front matter:

```py
from prelims import StaticSitePostsHandler
from prelims.processor import Recommender


handler = StaticSitePostsHandler('/path/to/posts')
handler.register_processor(
	Recommender(permalink_base='/post')
)
handler.execute()
```

For instance, a front matter of `article-aaa.md` may eventually become:

```yaml
---
date: 2022-01-01
title: Awesome Blog Post
recommendations: [/post/article-zzz/, /post/article-abc/, /post/article-xyz/]
keywords: [happy, beer, coffee, park, ...]
---
```

You can run the script as a pre-commit hook and automate the process e.g., with [lint-staged](https://github.com/okonet/lint-staged):

```
$ npm install -D lint-staged
```

```json
{
  ...
  "lint-staged": {
    "posts/*.{md,html}": [
      "python ./scripts/prelims.py",
      "git add -u posts/"
    ]
  },
  ...
}
```
