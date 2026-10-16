from telebot import types

Base = types.ReplyKeyboardMarkup(resize_keyboard=True)
Base.add("Отправить заявку")
Base.add("Ответить на зявку")
Base.add("Проверка заявки")
Base.add("Зарегистрироваться исполнителем")