import telebot
from telebot import *
from time import time
from todayCVE import * 
from controller import * 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from todayCVE import *

bot = telebot.TeleBot(telegramBotToken, parse_mode=None)

help = """
HELP //

/cve 
/last_cve_list
/today_cve_for_a_product
/terminology
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	bot.reply_to(message, "Hey "+message.from_user.first_name+"👋 Welcome to vulndote bot ! tap /help to know supported command 😊", reply_markup=markup)
 
@bot.message_handler(commands=['cve'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup = telebot.types.ForceReply()
	bot.reply_to(message, "Enter a CVE code :", reply_markup=markup)
 
@bot.message_handler(commands=['last_cve_list'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	b1 = InlineKeyboardButton(text='/critical')
	b2 = InlineKeyboardButton(text='/high')
	b3 = InlineKeyboardButton(text='/medium')
	b4 = InlineKeyboardButton(text='/low')
	markup.add(b1, b2, b3, b4)
	bot.reply_to(message, "dsqqsd",reply_markup=markup)
 
@bot.message_handler(commands=['critical','high','medium','low'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    asset = message.text 
    asset = asset.replace('/','')
    cve = cveTodaySortedByCVSS(asset)
    print (cve)
    if len(cve) > 4095:
        for x in range(0, len(cve), 4095): # Allow vulndote to send big GLOBAL message (split in x messages)
            bot.reply_to(message, text=cve[x:x+4095],reply_markup=markup, parse_mode="markdown")     
    else : 
        print (1)
        bot.reply_to(message, cve, reply_markup=markup, parse_mode="markdown")

@bot.message_handler(commands=['cve_sorted_today_asset'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup = telebot.types.ForceReply()
	bot.reply_to(message, "eEnter a Vendor :", reply_markup=markup, parse_mode="markdown")
 
@bot.message_handler(commands=['terminology'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	bot.reply_to(message,terminology(), reply_markup=markup, parse_mode="markdown")
 
###########################################################################################################

@bot.message_handler(func=lambda m: True)
def which_reply(message):
	if message.reply_to_message == None : 
		bot.reply_to(message,help)
	else :
		if message.reply_to_message.text == "Enter a CVE code :" : 
			markup = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Products Affected', callback_data = 'Products_Affected')
			b2 = InlineKeyboardButton(text='References', callback_data = 'References')
			markup.add(b1, b2)
			bot.reply_to(message, cveSearch(message.text), reply_markup=markup, parse_mode="markdown")
		elif message.reply_to_message.text == "eEnter a Vendor :" : 
			markup = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Critical', callback_data = 'Critical')
			b2 = InlineKeyboardButton(text='High', callback_data = 'High')
			b3 = InlineKeyboardButton(text='Medium', callback_data = 'Medium')
			b4 = InlineKeyboardButton(text='Low', callback_data = 'Low')
			markup.add(b1, b2, b3, b4)
			bot.reply_to(message,cveTodaySortedByVendor(message.text), reply_markup=markup, parse_mode="markdown")
   
@bot.callback_query_handler(func=lambda call: call.data != 'check_group') # Buttons fetch reply value 
def callback_inline(call):

	if call.data == "Critical":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"critical"), reply_markup=call.message.reply_markup, parse_mode="markdown")
		bot.answer_callback_query(call.id, "Loading... ")
	if call.data == "High":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"high"), reply_markup=call.message.reply_markup, parse_mode="markdown")
		bot.answer_callback_query(call.id, "Loading...")
	if call.data == "Medium":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"medium"), reply_markup=call.message.reply_markup, parse_mode="markdown")
		bot.answer_callback_query(call.id, "Loading...")
	if call.data == "Low":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"low"), reply_markup=call.message.reply_markup, parse_mode="markdown")
		bot.answer_callback_query(call.id, "Loading...")
	if call.data == "More_Info":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveTodaySortedByVendorAndCVSS(call.message.reply_to_message.text,"low"), reply_markup=call.message.reply_markup, parse_mode="markdown")
		bot.answer_callback_query(call.id, "Loading...")
	if call.data == "Products_Affected":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=vulnerableProductsOrVendors(call.message.reply_to_message.text), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Loading...")
	if call.data == "References":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=cveReferences(call.message.reply_to_message.text), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Loading...")

bot.infinity_polling() # Bot Exec
