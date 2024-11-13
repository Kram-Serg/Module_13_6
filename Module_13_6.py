from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api =''
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.row(button)
kb.insert(button2)

kb_inline = InlineKeyboardMarkup(resize_keyboard=True)
button_inline = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_inline2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_inline.row(button_inline)
kb_inline.insert(button_inline2)

class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)


@dp.callback_query_handler(text = 'calories')
async def set_gender(call):
    await call.message.answer('Укажите Ваш пол "m" или "w"')
    await call.answer()
    await UserState.gender.set()

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n'
                              'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.message_handler(state = UserState.gender)
async def set_age(message, state):
    await state.update_data(gender_user = message.text.lower())
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growht(message, state):
    await state.update_data(age_user = message.text)
    await message.answer('Введите свой рост в см')
    await UserState.growth.set()


@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_user = message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    global calories
    await state.update_data(weight_user = message.text)
    data = await state.get_data()
    if data['gender_user'] == 'm':
        calories = (10 * float(data['weight_user']) + 6.25
                    * float(data['growth_user']) -5 * float(data['age_user']) + 5)
    elif data['gender_user'] == 'w':
        calories =(10 * float(data['weight_user']) + 6.25
                   * float(data['growth_user']) - 5 * float(data['age_user']) - 161)
    await message.answer(f'Ваша суточная норма калорий составляет {calories}')
    await state.finish()

@dp.message_handler(commands=['start'])
async def star_massage(message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью', reply_markup=kb)

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)
