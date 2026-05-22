import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Response, status
from contextlib import asynccontextmanager
import uvicorn

from tele_bot import bot, dp, webhook_url

# use the bot_setup lifespan to set/delete the webhook on startup/shutdown

@asynccontextmanager
async def bot_setup(app: FastAPI):
    print("Setting WEbhook to:", webhook_url)

    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=["message", "edited_message", "callback_query"],
        drop_pending_updates=True
    )
    
    yield

    print("Removing webhook or Shuting Down server...")
    await bot.delete_webhook()
    await bot.session.close()

# Create the FastAPI app after bot_setup is defined so lifespan can reference it
app = FastAPI(lifespan=bot_setup)

@app.post("/rt_bot")
async def call_rt_bot(request: Request):
    try:
        payload = await request.json()
        print("Received update", payload)

        asyncio.create_task(dp.feed_webhook_update(bot=bot, update=payload))

        return Response(status_code=status.HTTP_200_OK)
    
    except Exception as e:

        print("Error occurred:", e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
if __name__ == "__main__":
    uvicorn.run("webhk:app", host="0.0.0.0", port=2020, reload=True)