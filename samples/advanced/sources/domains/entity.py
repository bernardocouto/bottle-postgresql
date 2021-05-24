from samples.advanced.sources.domains.database import Database
from samples.advanced.sources.log import get_logger

logger = get_logger(__name__)


class EntityModel:

    def __init__(self, entity):
        self.id = entity.id
        self.name = entity.name


class EntityRepository(Database):

    def __init__(self):
        super(EntityRepository, self).__init__('entities')

    def delete_entity(self, entity):
        (
            self.delete(self.table_name)
                .where('id', entity.get('id'), operator='=')
                .execute()
        )

    def insert_entity(self, entity):
        return (
            self.insert(self.table_name)
                .set('id', entity.id)
                .set('field', entity.field)
                .execute()
                .fetch_one()
        )

    def select_entity_all(self):
        return (
            self.select(self.table_name)
                .execute()
                .fetch_all()
        )

    def select_entity_by_id(self, id):
        return (
            self.select(self.table_name)
                .where('id', id, operator='=')
                .execute()
                .fetch_all()
        )

    def update_entity(self, entity):
        return (
            self.update(self.table_name)
                .set('field', entity.field)
                .where('id', entity.id, operator='=')
                .execute()
                .fetch_one()
        )
