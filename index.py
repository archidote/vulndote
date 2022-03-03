from email import message
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
/today_cve_list
/today_cve_sorted_by_asset
/terminology
/subscribe
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	bot.reply_to(message, "Hey "+message.from_user.first_name+"👋 Welcome to vulndote bot ! tap /help to know supported command 😊", reply_markup=markup)
 
@bot.message_handler(commands=['cve'])
def send_welcome(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = telebot.types.ForceReply()
        bot.reply_to(message, "Enter a CVE code :", reply_markup=markup)
        
@bot.message_handler(regexp="^/Cve@*")
def send_welcome(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        reFormatedCVE = cveReformated(message.text)
        markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text='Products Affected', callback_data = 'Products_Affected')
        b2 = InlineKeyboardButton(text='References', callback_data = 'References')
        b3 = InlineKeyboardButton(text='More info', callback_data = 'More_Info')
        markup.add(b1, b2, b3)
        bot.reply_to(message, cveSearch(reFormatedCVE), reply_markup=markup, parse_mode="HTML")


@bot.message_handler(commands=['today_cve_list'])
def send_welcome(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = InlineKeyboardButton(text='/critical')
        b2 = InlineKeyboardButton(text='/high')
        b3 = InlineKeyboardButton(text='/medium')
        b4 = InlineKeyboardButton(text='/low')
        markup.add(b1, b2, b3, b4)
        bot.reply_to(message, "Choose :",reply_markup=markup)
 
@bot.message_handler(commands=['critical','high','medium','low'])
def send_welcome(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else :     
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asset = message.text 
        asset = asset.replace('/','')
        cve = cveTodaySortedByCVSS(asset)
        if len(cve) > 4095:
            for x in range(0, len(cve), 4095): # Allow vulndote to send big GLOBAL message (split in x messages)
                bot.reply_to(message, text=cve[x:x+4095],reply_markup=markup)
        else : 
            bot.reply_to(message, cve, reply_markup=markup,parse_mode="HTML")

@bot.message_handler(commands=['today_cve_sorted_by_asset'])
def send_welcome(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = telebot.types.ForceReply()
        bot.reply_to(message, "eEnter a Vendor :", reply_markup=markup)
 
@bot.message_handler(commands=['terminology'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	bot.reply_to(message,terminology(), reply_markup=markup)
 
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
			b3 = InlineKeyboardButton(text='More info', callback_data = 'More_Info')
			markup.add(b1, b2, b3)
			bot.reply_to(message, cveSearch(message.text), reply_markup=markup, parse_mode="HTML")
		elif message.reply_to_message.text == "eEnter a Vendor :" : 
			markup = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Critical', callback_data = 'Critical')
			b2 = InlineKeyboardButton(text='High', callback_data = 'High')
			b3 = InlineKeyboardButton(text='Medium', callback_data = 'Medium')
			b4 = InlineKeyboardButton(text='Low', callback_data = 'Low')
			markup.add(b1, b2, b3, b4)
			bot.reply_to(message,cveTodaySortedByVendor(message.text), reply_markup=markup, parse_mode="HTML")
   
@bot.callback_query_handler(
    func=lambda call: call.data != "check_group"
)  # Buttons fetch reply value
def callback_inline(call):

    if call.data == "Critical":
        bot.answer_callback_query(call.id, "Loading... ")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=cveTodaySortedByVendorAndCVSS(
                call.message.reply_to_message.text, "critical"
            ),
            reply_markup=call.message.reply_markup,
        )
    if call.data == "High":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=cveTodaySortedByVendorAndCVSS(
                call.message.reply_to_message.text, "high"
            ),
            reply_markup=call.message.reply_markup,
        )
    if call.data == "Medium":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=cveTodaySortedByVendorAndCVSS(
                call.message.reply_to_message.text, "medium"
            ),
            reply_markup=call.message.reply_markup,
        )
    if call.data == "Low":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=cveTodaySortedByVendorAndCVSS(
                call.message.reply_to_message.text, "low"
            ),
            reply_markup=call.message.reply_markup,
        )
    if call.data == "Products_Affected":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=vulnerableProductsOrVendors(cveReformated(call.message.reply_to_message.text)),
            reply_markup=call.message.reply_markup,
        )
    if call.data == "References":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=cveReferences(cveReformated(call.message.reply_to_message.text)),
            reply_markup=call.message.reply_markup,
        )
    if call.data == "More_Info":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=moreInfo(cveReformated(call.message.reply_to_message.text)),
            reply_markup=call.message.reply_markup,
        )


bot.infinity_polling()  # Bot Exec
