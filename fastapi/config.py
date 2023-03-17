from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
import logging


logger = logging.getLogger("main")
load_dotenv()

DBNAME = getenv('DBNAME')
COLNAME = getenv('COLNAME')
TOKEN = getenv('TOKEN')
HOST = getenv('HOST')
PORT = getenv('PORT')
try:
  APP_PORT = int(getenv('APP_PORT'))
except (ValueError, TypeError) as err:
  logger.info(f'WRONG PORT!\n{err}')
else:
  APP_PORT=8000


QUERY = """
  {
    Page {
      media {
        siteUrl
        title {
          english
          native
        }
        description
      }
    }
  }
"""

URL = 'https://graphql.anilist.co'


CLIENT = MongoClient(f'mongodb://{HOST}:{PORT}/')



MESSAGE = "Media {0} successfully"

OK = 200

NOT_FOUND = 404

TIMEOUT = 3