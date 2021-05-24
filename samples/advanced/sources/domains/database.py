from samples.advanced.sources.log import get_logger
from samples.advanced.sources.utils import environment

import bottle_postgresql

logger = get_logger(__name__)


class Database(bottle_postgresql.Database):

    def __init__(self, table_name, configuration=None):
        if configuration:
            super(Database, self).__init__(configuration)
        else:
            super(Database, self).__init__()
        self.table_name = table_name

    @staticmethod
    def configuration():
        configuration_dict = {
            'database': environment.DATABASE_NAME,
            'host': environment.DATABASE_HOST,
            'max_connection': environment.DATABASE_MAX_CONNECTION,
            'password': environment.DATABASE_PASSWORD,
            'port': environment.DATABASE_PORT,
            'print_sql': environment.DATABASE_PRINT_SQL,
            'username': environment.DATABASE_USERNAME
        }
        bottle_postgresql.Configuration.instance(configuration_dict=configuration_dict, configuration_file=None)
