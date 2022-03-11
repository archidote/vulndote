import telebot
from telebot import *
from assets.todayCVE import * 
from assets.controller import * 
from assets.functions import * 
from assets.PoCExploits import * 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(telegramBotToken, parse_mode="HTML")

help = """
HELP MENU //

/cve 
/today_cve_list
/today_cve_sorted_by_asset
/terminology
/subscribe
"""

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
# 	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	bot.reply_to(message, "Hey "+message.from_user.first_name+"👋 Welcome to vulndote bot ! tap /help to know supported command 😊", reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    test="Checkmk <=2.0.0p19 contains a Cross Site Scripting (XSS) vulnerability. While creating or editing a user attribute, the Help Text is subject to HTML injection, which can be triggered for editing a user."
    bot.reply_to(message,test, reply_markup=markup)
 
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
        b1 = InlineKeyboardButton(text='Products Affected',callback_data='Products_Affected')
        b2 = InlineKeyboardButton(text='References', callback_data='References')
        b3 = InlineKeyboardButton(text='More info', callback_data='More_Info')
        b4 = InlineKeyboardButton(text='Exploits ?', callback_data='Available_Exploits')
        markup.add(b1, b2, b3, b4)
        bot.reply_to(message, cveSearch(reFormatedCVE), reply_markup=markup)


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
        send_text = 'https://api.telegram.org/bot' + telegramBotToken + '/sendMessage?chat_id=' + str(message.chat.id) + '&text=' + "Loading..."
        requests.get(send_text)
        cve = cveTodaySortedByCVSS(asset)
        if len(cve) > 4096 :
            for x in range(0, len(cve), 4096): # Allow vulndote to send big GLOBAL message (split in x messages)
                bot.reply_to(message, text=cve[x:x+4096],reply_markup=markup)
        else : 
            bot.reply_to(message, cve, reply_markup=markup)


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
	bot.reply_to(message,terminology(), reply_markup=markup,disable_web_page_preview=True)
 
###########################################################################################################
@bot.message_handler(func=lambda m: True)
def which_reply(message):
    if message.reply_to_message == None:
        bot.reply_to(message, help)
    else:
        if message.reply_to_message.text == 'Enter a CVE code :':
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text='Products Affected',callback_data='Products_Affected')
            b2 = InlineKeyboardButton(text='References',callback_data='References')
            b3 = InlineKeyboardButton(text='More info',callback_data='More_Info')
            b4 = InlineKeyboardButton(text='Exploits ?',callback_data='Available_Exploits')
            markup.add(b1, b2, b3, b4)
            bot.reply_to(message, cveSearch(message.text),
                         reply_markup=markup)
        elif message.reply_to_message.text == 'eEnter a Vendor :':
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text='Critical',callback_data='Critical')
            b2 = InlineKeyboardButton(text='High', callback_data='High')
            b3 = InlineKeyboardButton(text='Medium',callback_data='Medium')
            b4 = InlineKeyboardButton(text='Low', callback_data='Low')
            markup.add(b1, b2, b3, b4)
            bot.reply_to(message, cveTodaySortedByVendor(message.text),
                         reply_markup=markup)
   
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
            disable_web_page_preview=True
        )
    if call.data == "More_Info":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=moreInfo(cveReformated(call.message.reply_to_message.text)),
            reply_markup=call.message.reply_markup,
        )
    if call.data == "Available_Exploits":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=(searchPoCExploitWithSploitus(cveReformated(call.message.reply_to_message.text))),
            reply_markup=call.message.reply_markup,disable_web_page_preview=True
        )

bot.infinity_polling()  # Bot Exec
