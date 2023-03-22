from config import *
import logging
from logger import init_logger
import requests


init_logger('main')
logger = logging.getLogger("main")


def fill_database(client, data_to_insert):
    db = client[f'{DBNAME}']
    coll = db.COLNAME
    logger.info('Create database succesfully!')
    data_to_insert['_id'] = data_to_insert['id']
    del data_to_insert['id']
    url = data_to_insert['siteUrl']
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except Exception:
        return 'WRONG URL'
    if response.status_code != OK:
        return 'WRONG URL'
    coll.insert_one(data_to_insert)
    logger.info('Inserted data succesfully!')


def get_from_db(client):
    db = client[f'{DBNAME}']
    coll = db.COLNAME
    res = coll.find()
    logger.info('Get from database!')
    return res


def update_db(client, id_from_user, new_data):
    db = client[f'{DBNAME}']
    coll = db.COLNAME
    url = new_data['siteUrl']
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except Exception:
        return 'WRONG URL'
    if response.status_code != OK:
        return 'WRONG URL'
    result_to_user = coll.update_one({"_id": id_from_user}, {"$set": new_data})
    logger.info(f"Updated document with ID {id_from_user}")
    return result_to_user.modified_count


def delete_from_db(client, id_from_user):
    db = client[f'{DBNAME}']
    coll = db.COLNAME
    result_to_user = coll.delete_one({"_id": id_from_user})
    logger.info(f"Deleted document with ID {id_from_user}")
    return result_to_user.deleted_count
