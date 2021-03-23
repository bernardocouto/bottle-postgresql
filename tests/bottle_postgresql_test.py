from bottle_postgresql import Configuration, Database, Page

import unittest

CONFIGURATION = Configuration.instance(configuration_file='configurations/configuration.json')


class BottlePostgreSQLTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.database = Database(CONFIGURATION)
        with cls.database as connection:
            (
                connection
                .execute(
                    '''
                        create table if not exists test (
                            id bigserial not null,
                            name varchar(100),
                            description varchar(255),
                            constraint test_primary_key primary key (id)
                        )
                    ''',
                    skip_load_query=True
                )
            )

    @classmethod
    def tearDownClass(cls):
        cls.database = Database(CONFIGURATION)
        with cls.database as connection:
            (
                connection
                .execute('drop table if exists test', skip_load_query=True)
            )

    def setUp(self):
        self.database = Database(CONFIGURATION)

    def tearDown(self):
        pass

    def test_delete(self):
        pass

    def test_find_all(self):
        with self.database as connection:
            tests = (
                connection
                .select('test')
                .fields('id', 'name', 'description')
                .execute()
                .fetch_all()
            )

    def test_find_all_with_filter(self):
        with self.database as connection:
            test = (
                connection
                .execute('test.find_all_with_filter', parameters={'id': 100})
                .fetch_one()
            )
            self.assertEqual(test, None)
            test = (
                connection
                .execute('test.find_all_with_filter', parameters={'name': 'Test Name'})
                .fetch_all()
            )
            self.assertEqual(len(test), 0)

    def test_find_all_with_paging(self):
        with self.database as connection:
            tests = (
                connection
                .select('test')
                .fields('id', 'name', 'description')
                .paging(0, 1)
            )

    def test_find_by_id(self):
        with self.database as connection:
            test = (
                connection
                .select('test')
                .fields('id', 'name', 'description')
                .where('id', 1, operator='=')
            )

    def test_find_by_id_with_file(self):
        with self.database as connection:
            test = (
                connection
                .execute('test.find_by_id', parameters={'id': 1})
                .fetch_one()
            )

    def test_insert(self):
        with self.database as connection:
            test = (
                connection
                .insert('test')
                .set('name', 'Test Name')
                .set('description', 'Test Description')
                .execute()
                .fetch_one()
            )
            self.assertEqual(test['name'], 'Test Name')
            self.assertEqual(test['description'], 'Test Description')

    def test_insert_with_file(self):
        with self.database as connection:
            test = (
                connection
                .execute('test.save', {'name': 'Test Name', 'description': 'Test Description'})
                .fetch_one()
            )
            self.assertEqual(test['name'], 'Test Name')
            self.assertEqual(test['description'], 'Test Description')


if __name__ == '__main__':
    unittest.main
