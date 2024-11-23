from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ''  # переменная API-адреса

bot = Bot(token=api)  # переменная бота

dp = Dispatcher(bot, storage=MemoryStorage())  # переменная диспетчера


@dp.message_handler(commands=['start'])  # реагирование на команду
async def priv(message):
    await message.answer('Привет! Я - бот, помогающий твоему здоровью.')


@dp.message_handler()  # реагирование на любое сообщение
async def any(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':  # запуск программы бота
    executor.start_polling(dp, skip_updates=True)  # исполнитель
