import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
from aiogram.exceptions import TelegramRetryAfter

# 1. Bot sozlamalari
API_TOKEN = '8458722464:AAHACZTZRAgR-jlC1fPJj2m2a1CvFkymf1g'

# 2. Obyektlarni yaratish
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = FastAPI()

# --- HANDLERLAR ---

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer("Salom! Menga telefon raqamini yuboring, men uni kontakt ko'rinishida yuboraman.")

@dp.message()
async def send_contact_handler(message: Message):
    # Matn bo'lmasa ishlamaydi (rasm, stiker va h.k.)
    if not message.text:
        return

    phone_number = message.text.strip()
    
    # Raqam ekanligini tekshirish
    if phone_number.replace('+', '').isdigit():
        try:
            await message.answer_contact(
                phone_number=phone_number,
                first_name="Kontakt"
            )
        except TelegramRetryAfter as e:
            await message.answer(f"Limit oshdi. Iltimos, {e.retry_after} soniya kuting.")
        except Exception as e:
            logging.error(f"Xato yuz berdi: {e}")
    else:
        await message.answer("Iltimos, to'g'ri telefon raqami yuboring (masalan: +998901234567).")

# --- VERCEL VA WEBHOOK QISMI ---

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Telegram xabarlarini qabul qilish uchun endpoint"""
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def index():
    """Bot holatini tekshirish uchun"""
    return {"message": "Bot is running...", "status": "active"}

# Muhim: Vercel-da asyncio.run() yoki polling ishlatilmaydi.