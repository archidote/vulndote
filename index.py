import telebot
from telebot import *
from time import time 
from assets.search import * 
from todayCVE import * 
from controller import * 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from todayCVE import *

bot = telebot.TeleBot(telegramBotToken, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	bot.reply_to(message, "Hey "+message.from_user.first_name+"👋 Welcome to vulndote bot ! tap /help to know supported command 😊", reply_markup=markup)

@bot.message_handler(commands=['cve_today_vendor_product'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup = telebot.types.ForceReply()
	bot.reply_to(message, "Enter a Vendor/Product", reply_markup=markup)
 
 
###########################################################################################################

@bot.message_handler(func=lambda m: True)
def which_reply(message):
	if message.reply_to_message == None : 
		bot.reply_to(message, cveSearch(message.text))
	else :
		if message.reply_to_message.text == "Enter a Vendor/Product" : # Warning, here the sentence must be the same that the previous one for the answser context !!!
			markup = InlineKeyboardMarkup()
			bot.reply_to(message, cveTodaySortedByVendor(message.text), reply_markup=markup)
  
bot.infinity_polling() # Bot Exec
