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

			bot.send_message(message.chat.id, "This is a test LeadBot. You can create a request (order) and send it to a contractor. The contractor receives your request (order) directly and immediately. The contractor can then reply with a positive, negative, or clarifying response.\n\n/add - Create a request (order).\n/answer (For contractors) - Send a response to the customer's request.\n/check - Check the status of your request.\n/registration - Register as a contractor.", reply_markup = Base)
			if not check_user(db, str(message.from_user.id)):
				db[str(message.from_user.id)] = {
					"username": message.from_user.username,
					"status": 0,
					"question": None,
					"admin": 0
				}
				print(f"{message.from_user.id} new user!")


		if check_user(db, str(message.from_user.id)) and (message.text != "/start"):

			if message.text in ["/add", "Submit a Request"]:

				if not check_user_question(db, str(message.from_user.id)):
					bot.send_message(message.chat.id, "In your next message, enter the text of your request (order).", reply_markup = types.ReplyKeyboardRemove())
					db[str(message.from_user.id)]["status"] = 1
				else:
					bot.send_message(message.chat.id, "You have already submitted a request for review.")


			elif message.text in ["/answer", "Respond to a Request"]:
				if db[str(message.from_user.id)]["admin"] == 1:
					bot.send_message(message.chat.id, "In your next message, enter the ID of the user you want to reply to.", reply_markup = types.ReplyKeyboardRemove())
					db[str(message.from_user.id)]["status"] = 2
				else:
					bot.send_message(message.chat.id, "You are not registered as a contractor and cannot respond to requests.")


			elif message.text in ["/registration", "Register as a Contractor"]:

				if db[str(message.from_user.id)]["admin"] == 0:
					bot.send_message(message.chat.id, "In your next message, enter the bot token to register as a contractor.", reply_markup = types.ReplyKeyboardRemove())
					db[str(message.from_user.id)]["status"] = 3
				else:
					bot.send_message(message.chat.id, "You are already registered as a contractor.")


			elif message.text in ["/check", "Check Request Status"]:

				if check_user_question(db, str(message.from_user.id)):
					bot.send_message(message.chat.id, f"Your request:\n\n{db[str(message.from_user.id)]['question']}")
				else:
					bot.send_message(message.chat.id, "You have not submitted a request yet.")


			else:


				if db[str(message.from_user.id)]["status"] == 1:

					bot.send_message(message.chat.id, "Your request has been sent to the contractor.", reply_markup = Base)
					db[str(message.from_user.id)]["question"] = message.text
					for x in db:
						if db[x]["admin"] == 1:
							bot.send_message(int(x), f"Contractor, you have received a new request from {message.from_user.id}(@{message.from_user.username}):\n\n{message.text}")
					db[str(message.from_user.id)]["status"] = 0


				elif db[str(message.from_user.id)]["status"] == 2:

					if check_user_question(db, str(message.text)):
						bot.send_message(message.chat.id, "In your next message, enter your response to this request.")
						db[str(message.from_user.id)]["question_user_id"] = message.text
						db[str(message.from_user.id)]["status"] = 4
					else:
						bot.send_message(message.chat.id, "This user has not submitted a request.", reply_markup = Base)
						db[str(message.from_user.id)]["status"] = 0


				elif db[str(message.from_user.id)]["status"] == 3:

					if message.text == Token:
						bot.send_message(message.chat.id, "You have successfully registered as a contractor.", reply_markup = Base)
						db[str(message.from_user.id)]["admin"] = 1
						db[str(message.from_user.id)]["status"] = 0
					else:
						bot.send_message(message.chat.id, "Invalid token.", reply_markup = Base)
						db[str(message.from_user.id)]["status"] = 0


				elif db[str(message.from_user.id)]["status"] == 4:

					bot.send_message(db[str(message.from_user.id)]["question_user_id"], f"You have received a response to your request from the contractor:\n\n{message.text}")
					bot.send_message(message.chat.id, "Your response has been sent to the user.", reply_markup = Base)
					question_id = db[str(message.from_user.id)]["question_user_id"]
					try: db[question_id]["question"] = None
					except: print("question_id is None")
					db[str(message.from_user.id)]["question_user_id"] = None
					db[str(message.from_user.id)]["status"] = 0

		data.write_data("data.json", db)






bot.polling(none_stop=True, interval=0)