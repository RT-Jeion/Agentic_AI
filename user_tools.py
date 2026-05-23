import json
from datetime import  datetime
import os
from pathlib import Path

def user_check(user, text, reply):

    # users info
    user_id = str(user.id)
    user_name = str(user.username)
    name = user.full_name
    location = f"users/{user_name}.json"

    #time
    now = datetime.now()
    date = now.strftime("%d %b, %Y")
    time = now.strftime("%I:%M:%S %p, %A")
    
    # loads users.json
    try:
        with open("users.json", "r") as usr:
            print("[System]: Loading Users data from users.json")
            users = json.load(usr)
            print("[System]: Successfully Users data loaded...")

    except (json.JSONDecodeError, OSError):
        print("[System]: users.json not found.. empty list passed...")
        users = {}

    # loads users dir....
    users_dir = Path("users")

    if not os.path.exists(users_dir):
        print(f"[System]: Existing {users_dir} dir Not Found. Creating new dir...")
        users_dir.mkdir(parents=True, exist_ok=True)

    try:
        with open(location) as f:
            print(f"[System]: {user_name}'s chats data loading from {location}")
            chats = json.load(f)
            print("Chats Successfully loaded....")
    except:
        print(f"[System]: Cannot find {location}")
        chats = []

    chat = {
        "Date": date,
        "Time": time,
        "Message": text,
        "Reply": reply
    }
    chats.append(chat)

    # write to users chats
    try:
        with open(location, 'w') as f:
            print("Writting to:", location)
            json.dump(chats, f, indent=1)
            print("Successfully written...")
    except OSError:
        print("Falled to write", location)


    if user_id in users:
        print("User Name:", user_name)
        print("User Already exists.....")
        print("user Text:", text)
        print("System Reply:", reply)

        return False


    print("New user found....")
    print(f"User name: {user_name}")
    print("Full Name:", name)
    print("user Text:", text)
    print("System Reply:", reply)

    users[user_id] = {
        "User Name": user_name,
        "Full Name": name,
        "Location": location,
        "Started": {
            "Date": date,
            "Time": time
        }
    }

    try:
        with open("users.json", 'w') as usr:
            print("Writing to: users.json")
            
            json.dump(users, usr, indent=1)
            print("Successfully written")
    except OSError:
        print("Failed to write users.json")

    return True
