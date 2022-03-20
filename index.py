from datetime import date
import telebot
import datetime
from telebot import *
from assets.subscriber import checkIfUserIsAlreadyASubscriber, deleteSubscriber, insertSubscriber
from assets.todayCVE import * 
from assets.controller import * 
from assets.functions import * 
from assets.PoCExploits import * 
from assets.PoCExploits import * 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(telegramBotToken,parse_mode="HTML")

help = """
HELP MENU //

/cve 
/today_cve_list
/today_cve_sorted_by_asset
/subscribe
/favorised
/terminology
"""

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
# 	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	bot.reply_to(message, "Hey "+message.from_user.first_name+"👋 Welcome to vulndote bot ! tap /help to know supported command 😊", reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = date.today()
    hello(message.chat.id,message.from_user.first_name,today)
    bot.reply_to(message, "Hello", reply_markup=markup)
 
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
        b4 = InlineKeyboardButton(text='🔍 PoC on sploitus ?', callback_data='Available_Exploits_With_Sploitus')
        b5 = InlineKeyboardButton(text='🔍 PoC on Github ?', callback_data='Available_Exploits_Only_With_Github')
        b6 = InlineKeyboardButton(text='⭐', callback_data='Favorite')
        markup.add(b1, b2, b3, b4, b5, b6)
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
        var_data = bot.send_message(message.from_user.id,"Loading...⌛")
        cve = cveTodaySortedByCVSS(asset)
        if len(cve) > 4096 :
            for x in range(0, len(cve), 4096): # Allow vulndote to send big GLOBAL message (split in x messages)
                bot.reply_to(message, text=cve[x:x+4096],reply_markup=markup) # Message edit don't work for a big message, because the last message ate the previous's
        else : 
            bot.edit_message_text(cve, var_data.chat.id, var_data.message_id)

@bot.message_handler(commands=['today_cve_sorted_by_asset'])
def send_welcome(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = telebot.types.ForceReply()
        bot.reply_to(message, "eEnter a Vendor :", reply_markup=markup)
        
@bot.message_handler(commands=['subscribe'])
def send_welcome(message):
	markup = InlineKeyboardMarkup()	
	b1 = InlineKeyboardButton(text='Vendor', callback_data = 'subscribe_vendor_alerts')
	markup.add(b1)
	bot.reply_to(message, "Subscribe Menu :", reply_markup=markup)

@bot.message_handler(commands=['favorised'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.reply_to(message,listFavoriteCVE(message.chat.id), reply_markup=markup,disable_web_page_preview=True)
 
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
            b4 = InlineKeyboardButton(text='search Exploit with sploitus', callback_data='Available_Exploits_With_Sploitus')
            b5 = InlineKeyboardButton(text='search Exploit with sploitus', callback_data='Available_Exploits_Only_With_Github')
            markup.add(b1, b2, b3, b4, b5)
            bot.reply_to(message, cveSearch(message.text),
                         reply_markup=markup)
        elif message.reply_to_message.text == 'eEnter a Vendor :':
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text='Critical',callback_data='Critical')
            b2 = InlineKeyboardButton(text='High', callback_data='High')
            b3 = InlineKeyboardButton(text='Medium',callback_data='Medium')
            b4 = InlineKeyboardButton(text='Low', callback_data='Low')
            markup.add(b1, b2, b3, b4)
            cve = cveTodaySortedByVendor(message.text)
            if len(cve) > 4096 :
                for x in range(0, len(cve), 4096): # Allow vulndote to send big GLOBAL message (split in x messages)
                    bot.reply_to(message, text=cve[x:x+4096],reply_markup=markup)
            else : 
                bot.reply_to(message, cve, reply_markup=markup)
            
        elif message.reply_to_message.text == "Enter your a vendor/product name to be notifyed." : 
            api_request = cveTodaySortedByVendor(message.text)
            if api_request == "Vendor/Product hasn't been found." :
                bot.reply_to(message,"Vendor/Product hasn't been found. \n Try again : /subscribe")
            else : 
                insertSubscriber(str(message.chat.id),"vendor",message.text,api_request)
                bot.reply_to(message,"Subscribed to CVE alert for the following Vendor/Product :"+message.text+"")

   
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
        
    if call.data == "Available_Exploits_With_Sploitus":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=(searchPoCExploitWithSploitus(cveReformated(call.message.reply_to_message.text))),
            reply_markup=call.message.reply_markup,disable_web_page_preview=True
        )	
        
    if call.data == "Available_Exploits_Only_With_Github":
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=(searchPoCExploitOnlyWithGithub(cveReformated(call.message.reply_to_message.text))),
            reply_markup=call.message.reply_markup,disable_web_page_preview=True
        )	

    if call.data == "cancel":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
    if call.data == "subscribe_vendor_alerts":
        #print (call.message.json.message_id) # à revoir pour la facto
        check = checkIfUserIsAlreadyASubscriber("subscriber_vendor_alerts",str(call.message.chat.id))
        if check == True :
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text='Unsubscribe', callback_data = 'unsubscribe_vendor_alerts')
            markup.add(b1)
            bot.reply_to(call.message,"You are already subscribed.",reply_markup=markup)
        else : 
            markup = telebot.types.ForceReply()
            bot.reply_to(call.message, "Enter your a vendor/product name to be notifyed.", reply_markup=markup)

    if call.data == "unsubscribe_vendor_alerts":
        markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text='Yes', callback_data = 'unsubscribe_vendor_alerts_confirm')
        b2 = InlineKeyboardButton(text='No', callback_data = 'cancel')
        markup.add(b1, b2)
        bot.send_message(call.message.chat.id, text="Are you sure you want <b>unsubscribe</b> to <b>vendors/products</b> alerts?", reply_markup=markup)
        bot.answer_callback_query(call.id, "Are you sure?")
        
    if call.data == "Favorite":
        today = date.today()
        print(today)
        markup = InlineKeyboardMarkup()
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=(favorite(cveReformated(call.message.reply_to_message.text),today,call.message.chat.id)),
            reply_markup=call.message.reply_markup,disable_web_page_preview=True
        )

        
    if call.data == "unsubscribe_vendor_alerts_confirm":
        bot.answer_callback_query(call.id, "You unsubscribed to allergie alerts")
        bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=deleteSubscriber("vendor",call.message.chat.id))
bot.infinity_polling()  # Bot Exec
