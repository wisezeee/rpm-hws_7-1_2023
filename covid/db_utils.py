from config import *
from views import list_to_view
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv


load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


class InvalidQuery(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)
        self.message = msg

    def __str__(self):
        classname = self.__class__.__name__
        return f'{classname} error: {self.message}'


class DbHandler:

    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()

    @classmethod
    def get_data(cls, req_conds: dict = None) -> dict:
        try:
            cls.db_cursor.execute(cls.query_request(SELECTOR, req_conds) if req_conds else SELECTOR)
        except Exception as error:
            countries = []
            print(f'Database attribute typing error: {error}')
        else:
            countries = cls.db_cursor.fetchall()
        return {
            'number': len(countries),
            'rendered_counries': list_to_view(countries)
        }

    @classmethod
    def is_valid_token(cls, username: str, req_token: str):
        cls.db_cursor.execute(GET_TOKEN.format(username=username))
        db_token = cls.db_cursor.fetchone()
        if db_token:
            return db_token[0] == req_token
        return False

    @classmethod
    def compose_insert(cls, insert_data: dict):
        keys = tuple(insert_data.keys())
        values = [insert_data[key] for key in keys]
        attrs = ', '.join(keys)
        values = ', '.join([str(val) if isinstance(val, int) else f"'{val}'" for val in values])
        cls.db_cursor.execute(cls.query_request(
            SELECTOR, {
                "name": insert_data["name"],
                "continent": insert_data["continent"]
            }))
        if cls.db_cursor.fetchall():
            print('This country already exists')
            return ''
        return INSERT.format(table='country', keys=attrs, values=values)

    @classmethod
    def update(cls, data: dict, where: dict) -> bool:
            to_join = []
            for data_key, data_val in data.items():
                if data_key == 'name' and str(data_val).isdigit():
                    raise InvalidQuery('Country should not be a number')
                if data_key == 'population' and not str(data_val).isdigit():
                    raise InvalidQuery('population should be a number!')
                if data_key == 'population' and data_val <= 0:
                    raise InvalidQuery('population should be more than zero or zero!')
                if isinstance(data_val, (int, float)):
                    to_join.append(f"{data_key}={data_val}")
                else:
                    to_join.append(f"{data_key}='{data_val}'")
            req = ', '.join(to_join)
            try:
                cls.db_cursor.execute(cls.query_request(UPDATE.format(request=req), where))
            except Exception:
                return False
            cls.db_connection.commit()
            return True

    @classmethod
    def insert(cls, country_data: dict):
        keys = tuple(country_data.keys())
        values = [country_data[key] for key in keys]
        attrs = ', '.join(keys)
        values = ', '.join([str(val) if isinstance(val, int) else f"'{val}'" for val in values])
        cls.db_cursor.execute(cls.query_request(SELECTOR, country_data))
        select_result = cls.db_cursor.fetchone()
        if select_result:
            country_id = select_result[0]
            return BAD_REQUEST, f'Record already exists, id={country_id}'
        request = INSERT.format(table='country', keys=attrs, values=values)

        try:
            cls.db_cursor.execute(request)
        except Exception as error:
            print(f'{__name__} error: {error}')
            return INTERNAL_ERROR, f'db execute error: {error}'
        cls.db_connection.commit()
        insert_result = cls.db_cursor.fetchone()
        if insert_result:
            country_id = insert_result[0]
            return CREATED, str(country_id)
        return INTERNAL_ERROR, 'db insert failed'

    @classmethod
    def delete(cls, req_conds: dict) -> bool:
        try:
            cls.db_cursor.execute(cls.query_request(DELETE, req_conds))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @staticmethod
    def query_request(request: str, req_conds: dict):
        conditions = []
        for attr, value in req_conds.items():
            to_add = f'{attr}={value}' if isinstance(value, int) else f"{attr}='{value}'"
            conditions.append(to_add)
        return '{0} WHERE {1}'.format(request, ' AND '.join(conditions))
