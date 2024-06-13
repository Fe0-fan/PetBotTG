import telebot
import time
import random

TOKEN = ("token")
bot = telebot.TeleBot(TOKEN)

class Pet:
    def __init__(self, name):
        self.name = name
        self.happiness = 50
        self.hunger = 50
        self.tiredness = 50
        self.health = 100
        self.coins = 0

    def __str__(self):
        return f"Имя: {self.name}\nСчастье: {self.happiness}\nГолод: {self.hunger}\nУсталость: {self.tiredness}\nЗдоровье: {self.health}\nМонеты: {self.coins}"

pets = {}
pet_jobs = {}

def get_pet(chat_id):
    pet = pets.get(chat_id)
    if not pet:
        bot.send_message(chat_id, "Сначала заведите питомца! /start")
        return None
    return pet

@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Давай заведем питомца! Как ты его назовешь?")
    bot.register_next_step_handler(message, set_pet_name)

def set_pet_name(message):
    chat_id = message.chat.id
    pet_name = message.text
    pets[chat_id] = Pet(pet_name)
    bot.send_message(chat_id, f"Отлично! Твой питомец {pet_name} готов. Что ты хочешь сделать?")
    show_actions(message)

def show_actions(message):
    chat_id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Покормить"), telebot.types.KeyboardButton("Поиграть"))
    markup.add(telebot.types.KeyboardButton("Поспать"), telebot.types.KeyboardButton("Погладить"))
    markup.add(telebot.types.KeyboardButton("Проверить состояние"), telebot.types.KeyboardButton("Работать"))
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_action(message):
    chat_id = message.chat.id
    pet = get_pet(chat_id)
    if not pet:
        return

    if message.text == "Покормить":
        pet.hunger -= random.randint(10, 20)
        pet.happiness += random.randint(5, 15)
        bot.send_message(chat_id, f"{pet.name} с удовольствием поел!")
        pet.hunger = max(0, pet.hunger - 10)
    elif message.text == "Поиграть":
        pet.tiredness += random.randint(10, 20)
        pet.happiness += random.randint(10, 25)
        bot.send_message(chat_id, f"{pet.name} весело поиграл!")
    elif message.text == "Поспать":
        pet.tiredness -= random.randint(20, 30)
        pet.hunger += random.randint(5, 10)
        bot.send_message(chat_id, f"{pet.name} сладко спал!")
        pet.hunger = max(0, pet.hunger - 5)
    elif message.text == "Погладить":
        pet.happiness += random.randint(15, 25)
        bot.send_message(chat_id, f"{pet.name} доволен!")
    elif message.text == "Проверить состояние":
        bot.send_message(chat_id, str(pet))
    elif message.text == "Работать":
        pet_jobs[chat_id] = time.time()
        bot.send_message(chat_id, f"{pet.name} начал работать!")
    else:
        bot.send_message(chat_id, "Неизвестное действие.")

    bot.send_message(chat_id, str(pet))
    show_actions(message)

bot.polling(none_stop=True)

while True:
    for chat_id, job_time in list(pet_jobs.items()):
        if time.time() - job_time >= 60:
            pet = pets[chat_id]
            pet.coins += 50
            bot.send_message(chat_id, f"{pet.name} заработал 50 монет!")
            pet_jobs.pop(chat_id)

    time.sleep(1)
