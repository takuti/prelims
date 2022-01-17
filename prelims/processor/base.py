class BaseFrontMatterProcessor(object):

    def __init__(self, **params):
        """Set processor-specific parameters.
        """
        pass

    def process(self, posts, allow_overwrite):
        """Process a list of posts and update their front matters.
        """
        pass
