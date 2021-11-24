class VkSession(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(VkSession, cls).__new__(cls)
        return cls.instance