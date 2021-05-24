class Singleton(type):

    instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instance:
            cls.instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance[cls]

    @staticmethod
    def clear():
        Singleton.instance.clear()
