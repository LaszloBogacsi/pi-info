import psycopg2
from flask import g, current_app
from psycopg2.pool import SimpleConnectionPool


def init_app_db(app):
    app.teardown_appcontext(close_db)
    init_db()


def get_db() -> SimpleConnectionPool:
    if 'pgdb' not in g:
        try:
            g.pgdb = SimpleConnectionPool(1, 3,
                                          host=current_app.config["PGDB_HOST"],
                                          database=current_app.config["PGDB_DATABASE"],
                                          user=current_app.config["PGDB_USER"],
                                          password=current_app.config["PGDB_PASSWORD"])
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)

    return g.pgdb


def close_db(e=None):
    pgdb = g.pop('pgdb', None)
    if pgdb is not None:
        print("closing database connection pool...")
        pgdb.closeall()


def init_db():
    pool = get_db()
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()
    print(db_version)

    try:
        with current_app.open_resource('pi_info/repository/schema.sql') as f:
            cursor.execute(f.read().decode('utf-8'))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cursor.close()
        conn.commit()
        conn.close()
        pool.putconn(conn)
