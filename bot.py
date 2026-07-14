import asyncio
import re
from datetime import timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот-напоминалка.\n"
        "Напиши мне: напомни через 10 минут купить хлеб"
    )


@dp.message(F.text.func(lambda text: text.lower().startswith("напомни через")))
async def set_reminder(message: Message):
    pattern = r"напомни через (\d+) (минут|минуту|минуты|час|часа|часов) (.+)"
    match = re.match(pattern, message.text, re.IGNORECASE)

    if not match:
        await message.answer("Не понял формат. Пример: напомни через 10 минут купить хлеб")
        return

    amount = int(match.group(1))
    unit = match.group(2)
    task_text = match.group(3)

    if "час" in unit:
        delay_seconds = amount * 3600
    else:
        delay_seconds = amount * 60

    await message.answer(f"Хорошо! Напомню через {amount} {unit}: «{task_text}»")

    asyncio.create_task(send_reminder(message.chat.id, task_text, delay_seconds))


async def send_reminder(chat_id: int, text: str, delay: int):
    await asyncio.sleep(delay)
    await bot.send_message(chat_id, f"⏰ Напоминание: {text}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())