import logging
import asyncio
import nest_asyncio
import os
from g4f.client import Client

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["TOKEN"])
dp = Dispatcher()

nest_asyncio.apply()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = f"Привет, **@{message.from_user.username}**! Напиши мне текст, а я его подправлю."
    await message.answer(text, parse_mode="Markdown")

@dp.message()
async def handle_message(message: Message):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Привет! Проверь мой текст на наличие грамматических ошибок: \"{message.text}\""}, {"role": "system", "content": "Отвечай таким шаблоном и никак иначе: \"Исправленные слова:\n\nПравила, которые стоит вам прочесть:\", если ты не нашёл ошибки, то скажи об этом."}]
    )
    await message.answer(response.choices[0].message.content)   

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())