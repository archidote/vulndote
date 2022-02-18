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
 
@bot.message_handler(commands=['cve_sorted'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup = telebot.types.ForceReply()
	bot.reply_to(message, "eEnter a Vendor :", reply_markup=markup)
 
 
###########################################################################################################

@bot.message_handler(func=lambda m: True)
def which_reply(message):
	if message.reply_to_message == None : 
		bot.reply_to(message, cveSearch(message.text))
	else :
		if message.reply_to_message.text == "Enter a Vendor/Product" : # Warning, here the sentence must be the same that the previous one for the answser context !!!
			markup = InlineKeyboardMarkup()
			bot.reply_to(message, cveTodaySortedByVendor(message.text), reply_markup=markup)
		elif message.reply_to_message.text == "eEnter a Vendor :" : # Warning, here the sentence must be the same that the previous one for the answser context !!!
			markup = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Critical', callback_data = 'Critical')
			b2 = InlineKeyboardButton(text='High', callback_data = 'High')
			b3 = InlineKeyboardButton(text='Medium', callback_data = 'Medium')
			b4 = InlineKeyboardButton(text='Low', callback_data = 'Low')
			markup.add(b1, b2, b3, b4)
			bot.reply_to(message,"Choose :",reply_markup=markup)
   
@bot.callback_query_handler(func=lambda call: call.data != 'check_group') # Buttons fetch reply value 
def callback_inline(call):

	if call.data == "Critical":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"Critical"), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, " Loading ... ")
	if call.data == "High":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"High"), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Loading...")
	if call.data == "Medium":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"Medium"), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Loading...")
	if call.data == "Low":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"Low"), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Loading...")

bot.infinity_polling() # Bot Exec
