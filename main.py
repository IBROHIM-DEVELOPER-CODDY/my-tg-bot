import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.exceptions import TelegramRetryAfter

# Bot tokeningiz
API_TOKEN = '8458722464:AAHACZTZRAgR-jlC1fPJj2m2a1CvFkymf1g'

# Bot va Dispatcher obyektlarini yaratish
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer("Salom! Menga telefon raqamini yuboring (masalan: +998901234567), men uni kontakt ko'rinishida yuboraman.")

@dp.message()
async def send_contact_handler(message: Message):
    phone_number = message.text.strip()
    
    # Raqamni tekshirish (faqat raqamlar va + belgisi bormi)
    if phone_number.replace('+', '').isdigit():
        try:
            # Telegramga so'rov yuborishdan oldin juda qisqa tanaffus 
            # Bu botga ketma-ket yuklama tushishini kamaytiradi
            await asyncio.sleep(0.5) 

            await message.answer_contact(
                phone_number=phone_number,
                first_name="Kontakt"
            )
        except TelegramRetryAfter as e:
            # Agar baribir limitdan oshib ketsa, bot o'chib qolmasligi uchun
            logging.error(f"Limit oshib ketdi! {e.retry_after} soniya kutish kerak.")
            await message.answer(f"Xabar yuborish limiti oshdi. Iltimos, {e.retry_after} soniyadan keyin qayta urinib ko'ring.")
        except Exception as e:
            logging.error(f"Kutilmagan xato: {e}")
    else:
        await message.answer("Iltimos, to'g'ri telefon raqami yuboring.")

async def main():
    # Bot obyektini yaratish
    bot = Bot(token=API_TOKEN)
    
    # Eski xabarlarni tozalash (Bot o'chiq turganda kelgan xabarlarga javob qaytarmasligi uchun)
    await bot.delete_webhook(drop_pending_updates=True)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")