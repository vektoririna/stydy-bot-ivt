from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from config import admin_id, GROUPS
from main import bot, dp

from States import Test

from database import test, search_id, writing_student, student_group, give_schedule, give_tasks
from menu import menu


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


# запуск
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # проверка id пользователя в базе данных
    user = search_id(message.chat.id)
    if user is not None:
        await message.answer(f"Привет, {user[0]}!\n")
    else:
        await message.answer(f"Привет!\nЯ бот-помощник!\nДавай знакомиться!\nЖми /new")


# знакомство
@dp.message_handler(Command("new"), state=None)
async def new_user(message: types.Message):
    await message.answer("Что бы я мог помогать, мне нужно узнать тебя:\n"
                         "Вопрос №1. \n\n"
                         "Имя:")
    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def new_user_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(
        {"name": answer}
    )
    await message.answer("Вопрос №2. \n\n"
                         "Фамилия:")
    await Test.next()


@dp.message_handler(state=Test.Q2)
async def new_user_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(
        {"surname": answer}
    )
    await message.answer("Вопрос №3. \n\n"
                         "К какой группе ты относишься:", reply_markup=menu)
    await Test.next()


@dp.message_handler(state=Test.Q3)
async def new_user_q3(message: types.Message, state: FSMContext):
    # Достаем переменные
    data = await state.get_data()

    user_id = message.chat.id
    name = data.get('name')
    surname = data.get('surname')
    group = GROUPS.get(message.text)

    new_user_list = (user_id, surname, name, group)
    # print(new_user_list)
    writing_student(new_user_list)
    await message.answer("Приятно познакомиться!\n", reply_markup=ReplyKeyboardRemove())

    await state.finish()


# выдача расписания
@dp.message_handler(commands=['schedule'])
async def echo(message: types.Message):
    id_group = student_group(message.chat.id)
    text = give_schedule(id_group[0])
    await message.answer(text=text)


# выдача заданий
@dp.message_handler(commands=['tasks'])
async def echo(message: types.Message):
    id_group = student_group(message.chat.id)
    text = give_tasks(id_group[0])
    await message.answer(text=text)


# help
@dp.message_handler(commands=['help'])
async def echo(message: types.Message):
    text = ''' /schedule - расписание твоей группы\n/tasks - задания твоей группы'''
    await message.answer(text=text)


@dp.message_handler()
async def echo(message: types.Message):
    text = f'Ты написал: {message.text}'
    await message.answer(text=text)

