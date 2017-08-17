from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB__PORT = 27017
DB_NAME = 'newsweb'

client = MongoClient("%s:%d" %(MONGO_DB_HOST, MONGO_DB__PORT))

def get_db(db=DB_NAME):
    db = client[db]
    return db
