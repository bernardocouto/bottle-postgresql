class ObjectConverter:

    def __init__(self, entity):
        for key, value in entity.items():
            if isinstance(value, (list, tuple)):
                setattr(self, key, [ObjectConverter(child) if isinstance(child, dict) else child for child in value])
            else:
                setattr(self, key, ObjectConverter(value) if isinstance(value, dict) else value)
