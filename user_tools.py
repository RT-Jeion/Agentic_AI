from datetime import  datetime
from pymongo import MongoClient


def user_check(user, text, reply):

    #creating database (Mongodb)
    client = MongoClient("mongodb://localhost:27017")
    db = client["telegram_db"]

    # all users data collection
    all_users_db = db['all_users_info']


    # users info
    user_id = int(user.id)
    username = user.username
    name = user.full_name
    db_name = name

    #time
    now = datetime.now()
    date = now.strftime("%d %b, %Y")
    time = now.strftime("%I:%M:%S %p, %A")
    
    # creating per user collection
    #per user collection
    user_db = db[db_name]

    user_info = dict({
        "_id": user_id,
        "User Name": username,
        "Full Name": name,
        "Bot Started": {
            "Date": date,
            "Time": time
        },
        "Database Name":db_name
    })

    user_chat_count = user_db.count_documents({})


    user_chat = {
        "_id": user_chat_count + 1,
        "Time": time,
        "Date": date,
        "Message": text,
        "Reply": reply
    }
    print("="*30)
    print(f"{username} Messaged.....")
    print('User ID:', user_id)
    print("Name:", name)
    print("Message:", text)
    print("Replied:", reply)

    user_db.insert_one(user_chat)
    print(f"User's Chat updated.\nDatabase Name: [{db_name}]")

    user_exist = all_users_db.find_one({"_id": user_id})
    if user_exist:
        print("User Already Existed.....")
        return False

    print("It's a New User..")
    all_users_db.insert_one(user_info)
    print("New User's info added to ['all_users_info'] database")
    return True
    
