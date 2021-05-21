from dbutils.pooled_db import PooledDB

import errno
import json
import os
import psycopg2
import psycopg2.extras
import pystache

__author__ = 'Bernardo Couto'
__author_email__ = 'bernardocouto.py@gmail.com'
__version__ = '1.0.0'

QUERIES_DIRECTORY = os.path.realpath(os.path.curdir) + '/queries/'


class Configuration(object):

    __instance__ = None

    def __init__(self, configuration_dict=None, configuration_file=None):
        if configuration_dict:
            self.data = configuration_dict
        elif configuration_file:
            if not os.path.exists(configuration_file):
                raise ConfigurationNotFoundException()
            with open(configuration_file, 'r') as file:
                try:
                    self.data = json.loads(file.read())
                except json.decoder.JSONDecoderError as exception:
                    raise ConfigurationInvalidException(exception)
        self.data = {
            'dbname': str(self.data['database']),
            'host': str(self.data['host']),
            'maxconnections': int(self.data['max_connection']),
            'password': str(self.data['password']),
            'port': int(self.data['port']),
            'print_sql': bool(self.data['print_sql']),
            'user': str(self.data['username'])
        }
        self.print_sql = self.data.pop('print_sql') if 'print_sql' in self.data else False
        self.pool = PooledDB(psycopg2, **self.data)

    @staticmethod
    def instance(configuration_dict=None, configuration_file='/etc/bottle_postgresql/configuration.json'):
        if Configuration.__instance__ is None:
            Configuration.__instance__ = Configuration(configuration_dict, configuration_file)
        return Configuration.__instance__


class ConfigurationInvalidException(Exception):

    pass


class ConfigurationNotFoundException(Exception):

    pass


class CursorWrapper(object):

    def __init__(self, cursor):
        self.cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def close(self):
        self.cursor.close()

    def fetch_all(self):
        return [DictWrapper(row) for row in self.cursor.fetchall()]

    def fetch_many(self, size):
        return [DictWrapper(row) for row in self.cursor.fetchmany(size)]

    def fetch_one(self):
        row = self.cursor.fetchone()
        if row is not None:
            return DictWrapper(row)
        else:
            self.close()
        return row

    def next(self):
        row = self.fetch_one()
        if row is None:
            raise StopIteration()
        return row

    def row_count(self):
        return self.cursor.rowcount


class Database(object):

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is None and exception_value is None and exception_traceback is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.disconnect()

    def __init__(self, configuration=None):
        self.configuration = Configuration.instance() if configuration is None else configuration
        self.connection = self.configuration.pool.connection()
        self.print_sql = self.configuration.print_sql

    def delete(self, table):
        return DeleteBuilder(self, table)

    def disconnect(self):
        self.connection.close()

    def execute(self, sql, parameters=None, skip_load_query=False):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if self.print_sql:
            print('Query: {} - Parameters: {}'.format(sql, parameters))
        if skip_load_query:
            sql = sql
        else:
            sql = self.load_query(sql, parameters)
        cursor.execute(sql, parameters)
        return CursorWrapper(cursor)

    def insert(self, table):
        return InsertBuilder(self, table)

    def update(self, table):
        return UpdateBuilder(self, table)

    @staticmethod
    def load_query(query_name, parameters=None):
        try:
            with open(QUERIES_DIRECTORY + query_name + '.sql') as file:
                query = file.read()
            if not parameters:
                return query
            else:
                return pystache.render(query, parameters)
        except IOError as exception:
            if exception.errno == errno.ENOENT:
                return query_name
            else:
                raise exception

    def paging(self, sql, page=0, parameters=None, size=10, skip_load_query=True):
        if skip_load_query:
            sql = sql
        else:
            sql = self.load_query(sql, parameters)
        sql = '{} limit {} offset {}'.format(sql, size + 1, page * size)
        data = self.execute(sql, parameters, skip_load_query=True).fetch_all()
        last = len(data) <= size
        return Page(page, size, data[:-1] if not last else data, last)

    def select(self, table):
        return SelectBuilder(self, table)


class DictWrapper(dict):

    def __getattr__(self, item):
        if item in self:
            if isinstance(self[item], dict) and not isinstance(self[item], DictWrapper):
                self[item] = DictWrapper(self[item])
            return self[item]
        raise AttributeError('{} is not a valid attribute'.format(item))

    def __init__(self, data):
        self.update(data)

    def __setattr__(self, key, value):
        self[key] = value

    def as_dict(self):
        return self


class Migration(object):

    pass


class Page(dict):

    def __init__(self, page_number, page_size, data, last):
        self['data'] = self.data = data
        self['last'] = self.last = last
        self['page_number'] = self.page_number = page_number
        self['page_size'] = self.page_size = page_size


class SQLBuilder(object):

    def __init__(self, database, table):
        self.database = database
        self.parameters = {}
        self.table = table
        self.where_conditions = []

    def execute(self):
        return self.database.execute(self.sql(), self.parameters, True)

    def sql(self):
        pass

    def where_all(self, data):
        for value in data.keys():
            self.where(value, data[value])
        return self

    def where_build(self):
        if len(self.where_conditions) > 0:
            conditions = ' and '.join(self.where_conditions)
            return 'where {}'.format(conditions)
        else:
            return ''

    def where(self, field, value, constant=False, operator='='):
        if constant:
            self.where_conditions.append('{} {} {}'.format(field, operator, value))
        else:
            self.parameters[field] = value
            self.where_conditions.append('{0} {1} %({0})s'.format(field, operator))
        return self


class DeleteBuilder(SQLBuilder):

    def sql(self):
        return 'delete from {} {}'.format(self.table, self.where_build())


class InsertBuilder(SQLBuilder):

    def __init__(self, database, table):
        super(InsertBuilder, self).__init__(database, table)
        self.constants = {}

    def set(self, field, value, constant=False):
        if constant:
            self.constants[field] = value
        else:
            self.parameters[field] = value
        return self

    def set_all(self, data):
        for value in data.keys():
            self.set(value, data[value])
        return self

    def sql(self):
        if len(set(list(self.parameters.keys()) + list(self.constants.keys()))) == len(self.parameters.keys()) + len(self.constants.keys()):
            columns = []
            values = []
            for field in self.constants:
                columns.append(field)
                values.append(self.constants[field])
            for field in self.parameters:
                columns.append(field)
                values.append('%({})s'.format(field))
            return 'insert into {} ({}) values ({}) returning *'.format(self.table, ', '.join(columns), ', '.join(values))
        else:
            raise ValueError('There are repeated keys in constants and values')


class SelectBuilder(SQLBuilder):

    def __init__(self, database, table):
        super(SelectBuilder, self).__init__(database, table)
        self.select_fields = ['*']
        self.select_group_by = []
        self.select_order_by = []
        self.select_page = ''

    def fields(self, *fields):
        self.select_fields = fields
        return self

    def group_by(self, *fields):
        self.select_group_by = fields
        return self

    def order_by(self, *fields):
        self.select_order_by = fields
        return self

    def paging(self, page=0, size=10):
        self.select_page = 'limit {} offset {}'.format(size + 1, page * size)
        data = self.execute().fetch_all()
        last = len(data) <= size
        return Page(page, size, data[:-1] if not last else data, last)

    def sql(self):
        group_by = ', '.join(self.select_group_by)
        if group_by != '':
            group_by = 'group by {}'.format(group_by)
        order_by = ', '.join(self.select_order_by)
        if order_by != '':
            order_by = 'order by {}'.format(order_by)
        return 'select {} from {} {} {} {} {}'.format(
            ', '.join(self.select_fields),
            self.table,
            self.where_build(),
            group_by,
            order_by,
            self.select_page
        )


class UpdateBuilder(SQLBuilder):

    def __init__(self, database, table):
        super(UpdateBuilder, self).__init__(database, table)
        self.statements = []

    def set(self, field, value, constant=False):
        if constant:
            self.statements.append('{} = {}'.format(field, value))
        else:
            self.statements.append('{0} = %({0})s'.format(field))
            self.parameters[field] = value
        return self

    def set_all(self, data):
        for value in data.keys():
            self.set(value, data[value])
        return self

    def set_build(self):
        if len(self.statements) > 0:
            statements = ', '.join(self.statements)
            return 'set {}'.format(statements)
        else:
            return ''

    def sql(self):
        return 'update {} {} {}'.format(self.table, self.set_build(), self.where_build())
