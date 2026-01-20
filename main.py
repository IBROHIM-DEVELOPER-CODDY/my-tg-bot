import logging
import re
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
from aiogram.exceptions import TelegramRetryAfter

API_TOKEN = "8458722464:AAHACZTZRAgR-jlC1fPJj2m2a1CvFkymf1g"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = FastAPI()

# ---------------- HANDLERLAR ----------------

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "📱 Nomer yubor yoki @username / t.me link tashla\n\n"
        "Misol:\n"
        "998901234567\n"
        "@username\n"
        "https://t.me/username"
    )

@dp.message()
async def main_handler(message: Message):
    if not message.text:
        return

    text = message.text.strip()

    # -------- USERNAME --------
    if text.startswith("@"):
        username = text[1:]
        await message.answer(f"👤 Akkaunt:\nhttps://t.me/{username}")
        return

    # -------- LINK --------
    if "t.me/" in text:
        await message.answer(f"👤 Akkaunt:\n{text}")
        return

    # -------- AUTO FORMAT PHONE --------
    digits = re.sub(r"\D", "", text)

    if digits.startswith("998") and len(digits) == 12:
        phone = f"+{digits}"
    elif len(digits) == 9:
        phone = f"+998{digits}"
    else:
        await message.answer("❌ Nomer noto‘g‘ri\nMasalan: 998901234567")
        return

    try:
        await message.answer_contact(
            phone_number=phone,
            first_name="Kontakt"
        )
    except TelegramRetryAfter as e:
        await message.answer(f"⏳ Limit oshdi, {e.retry_after} soniya kuting")
    except Exception as e:
        logging.error(e)
        await message.answer("❌ Xatolik yuz berdi")

# ---------------- WEBHOOK ----------------

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/")
async def index():
    return {"status": "active"}
