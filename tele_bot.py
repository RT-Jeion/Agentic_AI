import os
import json
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile

def ensure_ogg_opus(src_path: str = "images/unya.webm", dst_path: str = "images/unya2.ogg") -> str | None:
    """Ensure an OGG/OPUS version of the source audio exists.

    Returns the path to the OGG file on success, or None on failure.
    """
    if os.path.exists(dst_path):
        return dst_path

    try:
        from pydub import AudioSegment

        audio = AudioSegment.from_file(src_path)
        audio.export(dst_path, format="ogg", codec="libopus")
        return dst_path
    except Exception as e:
        print("Audio conversion failed:", e)
        return None

Token = os.getenv("TELEGRAM_BOT_TOKEN" )
host_url = os.getenv("WEBHOOK_URL")
webhook_path = "/rt_bot"
webhook_url = f"{host_url}{webhook_path}"

bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def user_check(user):

    user_id = str(user.id)
    user_name = user.username
    name = user.full_name
    users = {}
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as usr:
                users = json.load(usr)
        except (json.JSONDecodeError, OSError):
            users = {}

    if user_id in users:
        print("User Already exists.....")
        return False

    print("New user found....")
    users[user_id] = {
        "User Name": user_name,
        "Full Name": name
    }

    try:
        with open("users.json", 'w') as usr:
            json.dump(users, usr, indent=1)
    except OSError:
        print("Failed to write users.json")

    return True

@dp.message(CommandStart())
async def cmd_start_handle(message: types.Message) -> None:
    user_check(message.chat)

    await message.bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker")
    await message.answer_animation(FSInputFile("images/soul-society-aizen.gif"), caption="Welcome.....\nSo You are Finally here... As I planned...")


@dp.message(Command("waguri"))
async def cmd_waguri_handle(message: types.Message) -> None:
    user_check(message.chat)

    await message.bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker")
    await message.answer_animation(FSInputFile("images/waguri.gif"), caption="..........")
    await message.bot.send_chat_action(chat_id=message.chat.id, action="upload_voice")
    ogg_path = ensure_ogg_opus("images/unya.webm", "images/unya2.ogg")
    if ogg_path:
        await message.answer_voice(FSInputFile(ogg_path))
    else:
        # Fallback: send original file as audio if conversion failed
        await message.answer_audio(FSInputFile("images/unya.webm"))


@dp.message(Command("status"))
async def cmd_status_handle(message: types.Message) -> None:
    await message.bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker")
    await message.answer_animation(FSInputFile("images/higuruma-jjk.gif"), caption="It's Under Development....")
    user_check(message.chat)


@dp.message(Command("about"))
async def cmd_about_handle(message: types.Message) -> None:
    user_check(message.chat)
    await message.bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker")
    await message.answer_animation(FSInputFile("images/khaby_lame.gif"), caption="Here is the info about the Bot...")
    

@dp.message()
async def msg_handle(message: types.Message) -> None:
    user_check(message.chat)
    
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await message.answer_photo(FSInputFile("images/monkey_middle.jpg"), caption="Wait.. It's under development..and you got caught in aizen plan.. for the very start...")