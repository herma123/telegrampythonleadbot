from telebot import types

Base = types.ReplyKeyboardMarkup(resize_keyboard=True)
Base.add("Submit a Request")
Base.add("Respond to a Request")
Base.add("Check Request Status")
Base.add("Register as a Contractor")