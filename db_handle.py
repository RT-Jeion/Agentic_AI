import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["telegram_db"]

all_col = db.list_collection_names()

print(all_col)

for cols in all_col:
    user = db[cols]
    for chat in user.find():
        print(chat)