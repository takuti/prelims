Prelims
===

Front matter post-processor for static site generators.

## Overview

Post-process YAML front matter of the static site generator contents (e.g., [Hugo](https://gohugo.io/content-management/front-matter/), [Jekyll](https://jekyllrb.com/docs/front-matter/), [Hexo](https://hexo.io/docs/front-matter.html)), and insert a list of **recommended posts** and **keywords** generated by [content-based filtering](https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering).

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

Once `prelims` based post-processing is triggered against all the posts, new metadata `recommendations` and `keywords` are dynamically generated and inserted as:

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
$ pip install git+https://github.com/takuti/prelims.git
```

## Usage

Assume your posts are under `/path/to/content/dir` where a static site generator uses as a document root:

```
content
└── dir
    ├── article-aaa.md
    ├── ...
    └── article-zzz.md
```

Here, the following script reads all `.md` and `.html` files in the folder, builds recommendations, and update each post's front matter:

```py
from prelims import process

process('/path/to/content/dir', permalink_base='/dir')
```

For instance, a front matter of `article-aaa.md` may eventually become:

```yaml
---
date: 2022-01-01
title: Awesome Blog Post
recommendations: [/dir/article-zzz/, /dir/article-abc/, /dir/article-xyz/]
keywords: [happy, beer, coffee, park, ...]
---
```

You can run the script as a pre-commit hook and automate the post-processing e.g., with [lint-staged](https://github.com/okonet/lint-staged):

```
$ npm install -D lint-staged
```

```json
{
  ...
  "lint-staged": {
    "content/dir/*.{md,html}": [
      "python ./scripts/prelims.py",
      "git add -u content/dir"
    ]
  },
  ...
}
```
