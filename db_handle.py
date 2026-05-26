import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["telegram_db"]

messages = db["messages"]


len_db = messages.count_documents({})
print(len_db)

chat = {
    "_id": len_db +1 ,
  "Date": "23 May, 2026",
  "Time": "01:42:19 PM, Saturday",
  "Message": "yooo",
  "Reply": "[System]: User: yooo"
 }

 

for msg in messages.find():
    print(msg)
