import logging  # Импортируем модуль для ведения логов
import asyncio  # Импортируем модуль для работы с асинхронным кодом
import nest_asyncio  # Импортируем библиотеку, позволяющую использовать asyncio в уже работающих циклах событий
import os  # Импортируем модуль для работы с операционной системой (например, для доступа к переменным окружения)
from g4f.client import Client  # Импортируем класс Client из библиотеки g4f для взаимодействия с API

from aiogram import Bot, Dispatcher, types  # Импортируем основные классы aiogram для работы с Telegram Bot API
from aiogram.filters import CommandStart  # Импортируем фильтр для обработки команды /start
from aiogram.types import Message  # Импортируем класс Message для работы с сообщениями

# Настраиваем уровень логирования на INFO
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота с токеном, который берется из переменных окружения
bot = Bot(token=os.environ["TOKEN"])
# Создаем диспетчер для обработки входящих сообщений
dp = Dispatcher()

# Применяем nest_asyncio для работы с асинхронным кодом в Jupyter или других средах, где уже запущен цикл событий
nest_asyncio.apply()

# Обрабатываем команду /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Формируем текст приветствия, используя имя пользователя
    text = f"Привет, @{message.from_user.username}! Напиши мне текст, а я его подправлю."
    # Отправляем ответ пользователю с текстом приветствия в формате Markdown
    await message.answer(text, parse_mode="Markdown")

# Обрабатываем все остальные сообщения
@dp.message()
async def handle_message(message: Message):
    # Создаем экземпляр клиента для работы с API g4f
    client = Client()
    # Отправляем запрос на создание завершения чата с моделью gpt-4o
    response = client.chat.completions.create(
        model="gpt-4o",  # Указываем модель, которую будем использовать
        messages=[  # Передаем список сообщений для контекста
            {"role": "user", "content": f"Привет! Проверь мой текст на наличие грамматических ошибок: "{message.text}""}, 
            {"role": "system", "content": "Отвечай таким шаблоном и никак иначе: "Исправленные слова:\n\nПравила, которые стоит вам прочесть:", если ты не нашёл ошибки, то скажи об этом."}
        ]
    )
    # Отправляем пользователю ответ от модели
    await message.answer(response.choices[0].message.content)   

# Основная асинхронная функция для запуска бота
async def main():
    # Запускаем опрос (polling) для получения обновлений от Telegram
    await dp.start_polling(bot)

# Проверяем, что этот файл запускается как основная программа
if __name__ == "__main__":
    # Запускаем основную функцию в асинхронном режиме
    asyncio.run(main())
