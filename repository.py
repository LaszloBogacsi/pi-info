from psycopg2.pool import SimpleConnectionPool

from applicationConfig import Config

database_config = Config.get_database_config()
get_pool = SimpleConnectionPool(1, 5,
                                host=database_config['host'],
                                database=database_config['database'],
                                user=database_config['user'],
                                password=database_config['password'])
