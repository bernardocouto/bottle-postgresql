from bottle_cerberus import Schema


class EntitySchema(Schema):

    @staticmethod
    def schema(self):
        return {
            'field': {
                'empty': False,
                'nullable': False,
                'required': True,
                'type': 'string'
            }
        }
