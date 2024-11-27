from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''  # переменная API-адреса

bot = Bot(token=api)  # переменная бота

dp = Dispatcher(bot, storage=MemoryStorage())  # переменная диспетчера

kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать')], [KeyboardButton(text='Информация')]],
                         resize_keyboard=True)  # создание объекта клавиатуры с масштабируемыми кнопками


class UserStates(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


@dp.message_handler(commands=['Start'])  # хэндлер обработки запускающей команды
async def starter(message):
    await message.answer('Выберите действие', replay_markup=kb)  # вывод клавиатуры


@dp.message_handler(text=['Рассчитать'])  # хэндлер обработки запроса на расчёт калорий
async def set_age(message):
    await message.answer('Введите свой возраст в полных годах')  # встречный запрос возраста
    await UserStates.age.set()  # ожидание ввода возраста и сохранение его значения в соответствующий атрибут


@dp.message_handler(state=UserStates.age)  # хэндлер обработки, реагирующий на изменение атрибута возраста
async def set_growth(message, state):
    await state.update_data(age=message.text)  # сохранение возраста в локальной БД машины состояний
    await message.answer('Введите свой рост в сантиметрах')  # запрос роста
    await UserStates.growth.set()  # ожидание ввода роста и сохранение его в атрибут


@dp.message_handler(state=UserStates.growth)  # хэндлер обработки, реагирующий на изменение атрибута роста
async def set_weight(message, state):
    await state.update_data(growth=message.text)  # сохранение роста в локальной БД машины состояний
    await message.answer('Введите свой вес в килограммах')  # запрос веса
    await UserStates.weight.set()  # ожидание ввода веса и сохранение его в атрибут


@dp.message_handler(state=UserStates.weight)  # хэндлер обработки, реагирующий на изменение атрибута роста
async def send_calories(message, state):
    await state.update_data(weight=message.text)  # сохранение веса в локальной БД машины состояний
    data = await state.get_data()  # считывание всех атрибутов состояния
    Age = int(data.get('age'))
    Growth = int(data.get('growth'))
    Weight = int(data.get('weight'))
    norma = (10 * Weight) + (6.25 * Growth) - (5 * Age) + 5  # расчёт нормы калорий
    await message.answer(f'Ваша норма потребления - {str(norma)} Ккал')  # вывод результата расчёта
    await state.finish()


if __name__ == '__main__':  # запуск программы бота
    executor.start_polling(dp, skip_updates=True)  # исполнитель
