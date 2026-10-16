import telebot, json, data
from telebot import types
from buttons import Base


Token = data.read_data("config.json")["Token"]
bot = telebot.TeleBot(Token)
db = data.read_data("data.json")


def check_user(data, userId):
	return userId in data

def check_user_question(data, userId):

	if check_user(data, userId):
		return data[userId]["question"] != None
	return False




@bot.message_handler(content_types=['text'])
def get_text_messages(message):


		if message.text == "/start":

			bot.send_message(message.chat.id, "Это тестовый LeadBot - вы оформляете заявку(заказ), отправляете исполнителю. Исполнитель сразу получает данную заявку(заказ) напрямую. Исполнитель отправляет вам ответ (положительный/отрицательный/уточняющий).\n\n/add - Написать заявку(заказ).\n/answer (Для исполнителя) - Исполнитель отправляет ответ на заявку заказчику.\n/check - Проверка своей заявки.\n/registration - Зарегистрироваться исполнителем. ", reply_markup =  Base)
			if not check_user(db, str(message.from_user.id)):
				db[str(message.from_user.id)] = {
					"username": message.from_user.username,
					"status": 0,
					"question": None,
					"admin": 0
				}
				print(f"{message.from_user.id} новый пользователь!")


		if check_user(db, str(message.from_user.id)) and (message.text != "/start"):

			if message.text in ["/add", "Отправить заявку"]:

				if not check_user_question(db, str(message.from_user.id)):
					bot.send_message(message.chat.id, "Следующим сообщением введите текст для заявки(заказа).", reply_markup = types.ReplyKeyboardRemove())
					db[str(message.from_user.id)]["status"] = 1
				else:
					bot.send_message(message.chat.id, "Вы уже отправили заявку на рассмотрение.")


			elif message.text in ["/answer", "Ответить на зявку"]:
				if db[str(message.from_user.id)]["admin"] == 1:
					bot.send_message(message.chat.id, "Следующим сообщением введите id пользователя которому желаете ответить.", reply_markup = types.ReplyKeyboardRemove())
					db[str(message.from_user.id)]["status"] = 2
				else:
					bot.send_message(message.chat.id, "Вы не являетесь исполнителем, чтобы отвечать на заявки.")


			elif message.text in ["/registration", "Зарегистрироваться исполнителем"]:

				if db[str(message.from_user.id)]["admin"] == 0:
					bot.send_message(message.chat.id, "Следующим сообщением для регистрации введите токен бота.", reply_markup = types.ReplyKeyboardRemove())
					db[str(message.from_user.id)]["status"] = 3
				else:
					bot.send_message(message.chat.id, "Вы уже являетесь исполнителем.")


			elif message.text in ["/check", "Проверка заявки"]:

				if check_user_question(db, str(message.from_user.id)):
					bot.send_message(message.chat.id, f"Ваша заявка:\n\n{db[str(message.from_user.id)]['question']}")
				else:
					bot.send_message(message.chat.id, "Вы еще не отправляли заявку.")


			else:


				if db[str(message.from_user.id)]["status"] == 1:

					bot.send_message(message.chat.id, "Заявка была отправлена исполнителю.", reply_markup = Base)
					db[str(message.from_user.id)]["question"] = message.text
					for x in db:
						if db[x]["admin"] == 1:
							bot.send_message(int(x), f"Исполнитель, новая заявка от {message.from_user.id}(@{message.from_user.username}):\n\n{message.text}")
					db[str(message.from_user.id)]["status"] = 0


				elif db[str(message.from_user.id)]["status"] == 2:

					if check_user_question(db, str(message.text)):
						bot.send_message(message.chat.id, "Следующим сообщением введите ответ на данную заявку.")
						db[str(message.from_user.id)]["question_user_id"] = message.text
						db[str(message.from_user.id)]["status"] = 4
					else:
						bot.send_message(message.chat.id, "Данный пользователь не отправлял заявку.", reply_markup = Base)
						db[str(message.from_user.id)]["status"] = 0


				elif db[str(message.from_user.id)]["status"] == 3:

					if message.text == Token:
						bot.send_message(message.chat.id, "Вы успешно стали исполнителем.", reply_markup = Base)
						db[str(message.from_user.id)]["admin"] = 1
						db[str(message.from_user.id)]["status"] = 0
					else:
						bot.send_message(message.chat.id, "Неверный токен", reply_markup = Base)
						db[str(message.from_user.id)]["status"] = 0


				elif db[str(message.from_user.id)]["status"] == 4:

					bot.send_message(db[str(message.from_user.id)]["question_user_id"], f"Вы получили ответ на заявку от исполнителя: \n\n{message.text}")
					bot.send_message(message.chat.id, "Вы отправили ответ на заявку пользователю.", reply_markup = Base)
					question_id = db[str(message.from_user.id)]["question_user_id"]
					try: db[question_id]["question"] = None
					except: print("question_id is None")
					db[str(message.from_user.id)]["question_user_id"] = None
					db[str(message.from_user.id)]["status"] = 0

		data.write_data("data.json", db)






bot.polling(none_stop=True, interval=0)