from .processors.recommender import Recommender
from .handler import StaticSitePostsHandler


def process(path_dir, permalink_base='', tokenizer=None, custom_processors=[]):

    handler = StaticSitePostsHandler(path_dir)
    recommender = Recommender(permalink_base=permalink_base, topk=3,
                              tokenizer=tokenizer)
    handler.register_processor(recommender)
    for processor in custom_processors:
        handler.register_processor(processor)

    handler.execute()