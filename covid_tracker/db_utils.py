from dotenv import load_dotenv
from os import getenv
from psycopg2 import connect


load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')

con = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
cur = con.cursor()

query = "select * from population"
cur.execute(query)

records = cur.fetchall()

pop_en = ''
pop_ru = ''
pop_all = ''

for row in records:
    pop_ru = row[1]
    pop_en = row[2]
    pop_all = row[3]


cur.close()
con.close()