from unittest import result
import schedule, threading, telebot
import time as t
from telebot import *
from assets.cwe import cweSortedByYear
from assets.owasp import owaspTopTen
from assets.subscriber import checkIfUserIsAlreadyASubscriber, deleteSubscriber, insertSubscriber
from assets.cveToday import * 
from assets.controller import * 
from assets.functions import * 
from assets.cvePoCExploits import * 
from assets.cveAdditionalInformation import * 
from assets.favorite import * 
from assets.send_message import *
from assets.cve_alert import *
from telebot.types import *

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN,parse_mode="HTML")

help = """

ℹ️ HELP 🛟 Features that you can use :

Information about a CVE - Ex : CVE-2021-4034
/today
/today_vendor
/cwe
/owasp
/subscribe
/favorised
/terminology
/demo_yt
"""
# /week_vendor
# /month_vendor

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = date.today()
    hello(message.chat.id,message.from_user.first_name,today)
    bot.reply_to(message, "Hello 👋, welcome to Vulndote telegram bot !\nTap /help to know my abilities", reply_markup=markup)
        
@bot.message_handler(regexp="^CVE-*")
def cve_code_input(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        reFormatedCVE = cveReformated(message.text)
        cve_result = cveSearch(reFormatedCVE,0)
        if cve_result == CVE_NOT_FOUND : 
            bot.reply_to(message, CVE_NOT_FOUND)
        else : 
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text='💻/📦',callback_data='Products_Affected')
            b2 = InlineKeyboardButton(text='📖 Ref', callback_data='References')
            b3 = InlineKeyboardButton(text='ℹ️', callback_data='More_Info')
            b4 = InlineKeyboardButton(text='🔍 Search for PoC ?', callback_data='Available_Exploits_Only_With_Github')
            b5 = InlineKeyboardButton(text='⭐', callback_data='Favorite')
            markup.add(b1, b2, b3, b4, b5)
            bot.reply_to(message, cveSearch(reFormatedCVE,0), reply_markup=markup)
        
@bot.message_handler(regexp="^/Cve@*")
def catch_cve_on_the_fly(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        reFormatedCVE = cveReformated(message.text)
        markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text='💻/📦',callback_data='Products_Affected')
        b2 = InlineKeyboardButton(text='📖 Ref', callback_data='References')
        b3 = InlineKeyboardButton(text='ℹ️', callback_data='More_Info')
        b4 = InlineKeyboardButton(text='🔍 Search for PoC ?', callback_data='Available_Exploits_Only_With_Github')
        b5 = InlineKeyboardButton(text='⭐', callback_data='Favorite')
        markup.add(b1, b2, b3, b4, b5)
        bot.reply_to(message, cveSearch(reFormatedCVE,0), reply_markup=markup)

       
@bot.message_handler(commands=['cwe'])
def cwe(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    previousYear = int(currentYear) - 1 
    bot.reply_to(message,cweSortedByYear(previousYear),reply_markup=markup)
    
@bot.message_handler(commands=['owasp'])
def owasp(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.reply_to(message,owaspTopTen(),reply_markup=markup)
    
    
@bot.message_handler(regexp="^/Cwe@*") # TO DO 
def CVEOnTheFly(message):
    reFormatedCWE = cweReformated(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.reply_to(message, cweSortedByYear(int(reFormatedCWE)), reply_markup=markup)
        
@bot.message_handler(commands=['today'])
def todayCVEList(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = InlineKeyboardButton(text='/critical')
        b2 = InlineKeyboardButton(text='/high')
        b3 = InlineKeyboardButton(text='/medium')
        b4 = InlineKeyboardButton(text='/low')
        markup.add(b1, b2, b3, b4)
        bot.reply_to(message, "Choose a level of criticity :",reply_markup=markup)
        
@bot.message_handler(commands=['critical','high','medium','low'])
def levelOfCriticity(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else :     
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asset = message.text 
        asset = asset.replace('/','')
        loading = bot.send_message(message.from_user.id,"⏳")
        cve = cveTodaySortedByCVSS(asset)
        if len(cve) > 4096 :
            for x in range(0, len(cve), 4096): # Allow vulndote to send big GLOBAL message (split in x messages)
                bot.reply_to(message, text=cve[x:x+4096],reply_markup=markup) # Message edit don't work for a big message, because the last message "ate" the previous's
        else : 
            bot.edit_message_text(cve, loading.chat.id, loading.message_id)

@bot.message_handler(commands=['today_vendor'])
def CVESortedByVendorOrProduct(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = telebot.types.ForceReply()
        bot.reply_to(message, "Enter a vendor or a product name :", reply_markup=markup)
         
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
	markup = InlineKeyboardMarkup()	
	b1 = InlineKeyboardButton(text='Vendor/Product', callback_data = 'subscribe_vendor_alerts')
	markup.add(b1)
	bot.reply_to(message, "Subscribe Menu :", reply_markup=markup)

@bot.message_handler(commands=['favorised'])
def favorised(message):
    markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text='This year',callback_data='Fav_Sorted_By_This_Year')
    b2 = InlineKeyboardButton(text='This Month',callback_data='Fav_Sorted_By_This_Month')
    b3 = InlineKeyboardButton(text='Last Month',callback_data='Fav_Sorted_By_Last_Month')
    markup.add(b1,b2,b3)
    CVEs = listFavoriteCVE(message.chat.id,"notSorted")
    loading = bot.send_message(message.from_user.id,"⏳")
    if len(CVEs) > 4096 :
        for x in range(0, len(CVEs), 4096): 
            bot.reply_to(message, text=CVEs[x:x+4096],reply_markup=markup) 
    else : 
        bot.edit_message_text(CVEs, loading.chat.id, loading.message_id,reply_markup=markup)

@bot.message_handler(regexp="^/unfav@*")
def unFavOntheFly(message):
    if timeOutAPI() == True : 
        bot.reply_to(message, "Api is not reachable at the moment")
    else : 
        reFormatedCVE = cveReformated(message.text)
        bot.reply_to(message,unfav(message.chat.id,reFormatedCVE),disable_web_page_preview=True)
        
 
@bot.message_handler(commands=['terminology'])
def terms(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	bot.reply_to(message,terminology(), reply_markup=markup, disable_web_page_preview=True)

###################################################################################################################
#                                             FETCH ANSWERS OF AN /action                                         #
###################################################################################################################   

@bot.message_handler(func=lambda m: True)
def which_reply(message):
    if message.reply_to_message == None:
        bot.reply_to(message, help)
    else:
        if message.reply_to_message.text == 'Enter a vendor or a product name :':
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text='Critical',callback_data='Critical')
            b2 = InlineKeyboardButton(text='High', callback_data='High')
            b3 = InlineKeyboardButton(text='Medium',callback_data='Medium')
            b4 = InlineKeyboardButton(text='Low', callback_data='Low')
            markup.add(b1, b2, b3, b4)
            loading = bot.reply_to(message,"⏳")
            cve = cveTodaySortedByVendor(message.text)
            if cve == NO_CVE_HAVE_BEEN_REGISTERED_TODAY_FOR+""+message.text :
                bot.edit_message_text(message_id=loading.id,chat_id=loading.chat.id, text=cve)
            elif cve == VENDOR_OR_PRODUCT_NOT_FOUND :
                bot.edit_message_text(message_id=loading.id,chat_id=loading.chat.id, text=cve)
            else :  
                if len(cve) > 4096 :
                    for x in range(0, len(cve), 4096): # Allow vulndote to send big GLOBAL message (split in x messages)
                        bot.reply_to(message, text=cve[x:x+4096], reply_markup=markup)
                else : 
                    bot.edit_message_text(message_id=loading.id,chat_id=loading.chat.id, text=cve, reply_markup=markup)

                    
        elif message.reply_to_message.text == "Enter your a vendor/product name to be notifyed." : 
            if cveTodaySortedByVendor(message.text) == VENDOR_OR_PRODUCT_NOT_FOUND :
                markup = InlineKeyboardMarkup()
                b1 = InlineKeyboardButton(text='Edit the vendor/product',callback_data='Edit_Vendor_Alerts')
                markup.add(b1)
                bot.reply_to(message,"❌ Vendor/Product hasn't been found. \n Try again : ", reply_markup=markup)
            else : 
                insertSubscriber(str(message.chat.id),"vendor",message.text,"")
                bot.reply_to(message,"Subscribed ✅ : "+message.text+"")
 
###################################################################################################################
#                                             BUTTON CALLBACK                                                     #
###################################################################################################################               
   
@bot.callback_query_handler(func=lambda call: call.data != "check_group")  # Buttons fetch reply value
def callback_inline(call):

    if call.data == "Critical" or call.data == "High" or call.data == "Medium" or call.data == "Low" :
        bot.answer_callback_query(call.id, "Loading... ")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=cveTodaySortedByVendorAndCVSS(
                call.message.reply_to_message.text, call.data
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
        check = checkIfUserIsAlreadyASubscriber("subscriber_vendor_alerts",str(call.message.chat.id))
        if check == True :
            markup = InlineKeyboardMarkup()
            b1 = InlineKeyboardButton(text='Unsubscribe', callback_data = 'unsubscribe_vendor_alerts')
            b2 = InlineKeyboardButton(text='Edit the vendor/product', callback_data = 'Edit_Vendor_Alerts')
            markup.add(b1,b2)
            bot.reply_to(call.message,"You are already subscribed to : <b>"+getVendorOrProduct(call.message.chat.id)+"</b>",reply_markup=markup)
        else : 
            markup = telebot.types.ForceReply()
            bot.reply_to(call.message, "Enter your a vendor/product name to be notifyed.", reply_markup=markup)

    if call.data == "unsubscribe_vendor_alerts":
        markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text='Yes', callback_data = 'unsubscribe_vendor_alerts_confirm')
        b2 = InlineKeyboardButton(text='No', callback_data = 'cancel')
        markup.add(b1, b2)
        bot.send_message(call.message.chat.id, text="⚠️ Are you sure you want <b>unsubscribe</b> to <b>vendors/products</b> alerts?", reply_markup=markup)
        bot.answer_callback_query(call.id, "Are you sure?")
        
    if call.data == "Favorite":
        
        bot.answer_callback_query(call.id, "Loading...")
        cveReformatedVar = cveReformated(call.message.reply_to_message.text)
        favorisedORNot = isThisCVEIsFavorised(call.message.chat.id,cveReformatedVar)
        
        if favorisedORNot == "You have already favorised this cve." :
            bot.reply_to(call.message,"You have already favorised "+cveReformatedVar+". \n➡️ Unfav it ?  /unfav@"+cveFormatedForRegex(cveReformatedVar)+"")
        else : 
            bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=(favorite(cveReformatedVar,call.message.chat.id)),
            reply_markup=call.message.reply_markup
            )
    
    if call.data == "Fav_Sorted_By_This_Year" or call.data == "Fav_Sorted_By_This_Month" or call.data == "Fav_Sorted_By_Last_Month" :
        bot.answer_callback_query(call.id, "Loading...")
        bot.edit_message_text(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            text=(listFavoriteCVE(call.message.chat.id,call.data)),
            reply_markup=call.message.reply_markup
            )
           
    if call.data == "Edit_Vendor_Alerts":
        markup = telebot.types.ForceReply()
        bot.reply_to(call.message, "Enter your a vendor/product name to be notifyed.", reply_markup=markup)

###################################################################################################################
#                                             BUTTON CALLBACK (confirm your action)                               #
###################################################################################################################   
        
    if call.data == "unsubscribe_vendor_alerts_confirm":
        bot.answer_callback_query(call.id, "Unsubscribed !")
        bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=deleteSubscriber("vendor",call.message.chat.id))

###################################################################################################################
#           SCHEDULE THE AUTO FETCHING API TO GET THE LATEST CVE FROM THE SUBSCRIBER'S VENDOR PREFERENCE          #
###################################################################################################################  
schedule.every(30).minutes.do(lambda: check_for_new_cve())

def schedule_api_fetching(): 
    while True:
        schedule.run_pending()
        t.sleep(1)

t1 = threading.Thread(target = schedule_api_fetching)
t1.start()

###################################################################################################################
#                                                   BOT EXEC                                                      #
################################################################################################################### 

bot.infinity_polling()