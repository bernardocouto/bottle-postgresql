from samples.advanced.sources.commons.converter import ObjectConverter
from samples.advanced.sources.domains.entity import EntityModel, EntityRepository


class EntityBusiness:

    @staticmethod
    def delete_entity(id):
        with EntityRepository() as repository:
            entity = repository.select_entity_by_id(id)
            entity = EntityModel(
                ObjectConverter({
                    'id': entity.get('id'),
                    'field': entity.get('field')
                })
            )
            repository.delete_entity(entity)

    @staticmethod
    def insert_entity(field):
        entity = EntityModel(
            ObjectConverter({
                'field': field
            })
        )
        with EntityRepository() as repository:
            return repository.insert_entity(entity)

    @staticmethod
    def select_entity_all():
        with EntityRepository() as repository:
            return repository.select_entity_all()

    @staticmethod
    def update_entity(id, field):
        with EntityRepository() as repository:
            entity = repository.select_entity_by_id(id)
            entity.field = field
            return repository.update_entity(entity)
