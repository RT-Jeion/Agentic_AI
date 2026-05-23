import os
import subprocess
import tempfile
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile

from user_tools import user_check

Token = os.getenv("TELEGRAM_BOT_TOKEN" )
host_url = os.getenv("WEBHOOK_URL")
webhook_path = "/rt_bot"
webhook_url = f"{host_url}{webhook_path}"

bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def convert_to_voice_note(source_path: str) -> Path:
    source = Path(source_path)
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
        output_path = Path(temp_file.name)

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-vn",
            "-c:a",
            "libopus",
            "-b:a",
            "64k",
            str(output_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return output_path


@dp.message(CommandStart())
async def cmd_start_handle(message: types.Message) -> None:
    text = "[System]: User used /start command..."
    reply = "[System]: Replied /start command response"
    user = message.chat
    

    await message.bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker")
    await message.answer_animation(FSInputFile("images/soul-society-aizen.gif"), caption="Welcome.....\nSo You are Finally here... As I planned...")
    
    user_check(user=user, text=text, reply=reply)


@dp.message(Command("waguri"))
async def cmd_waguri_handle(message: types.Message) -> None:
    text = "[System]: User used /waguri command..."
    reply = "[System]: Replied /waguri command response"
    user = message.chat


    await message.bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker")
    await message.answer_animation(FSInputFile("images/waguri.gif"), caption="..........")
    voice_path = convert_to_voice_note("images/unya.webm")
    try:
        await message.answer_voice(FSInputFile(voice_path))
    finally:
        voice_path.unlink(missing_ok=True)
    
    user_check(user=user, text=text, reply=reply)

@dp.message(Command("status"))
async def cmd_status_handle(message: types.Message) -> None:
    text = "[System]: User used /status command..."
    reply = "[System]: Replied /status command response"
    user = message.chat

    await message.bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker")
    await message.answer_animation(FSInputFile("images/higuruma-jjk.gif"), caption="It's Under Development....")
    
    user_check(user=user, text=text, reply=reply)


@dp.message(Command("about"))
async def cmd_about_handle(message: types.Message) -> None:
    text = "[System]: User used /about command..."
    reply = "[System]: Replied /about command response"
    user = message.chat

    await message.bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker")
    await message.answer_animation(FSInputFile("images/khaby_lame.gif"), caption="Here is the info about the Bot...")
    
    user_check(user=user,text=text, reply=reply)


@dp.message()
async def msg_handle(message: types.Message) -> None:
    text = message.text
    reply = f"[System]: User texted {text}"
    user = message.chat

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await message.answer(reply)

    user_check(user,text, reply)