import sqlite3
from assets.functions import *

def checkIfUserIsAlreadyASubscriber(tableName,chat_id): 
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT chat_id FROM {tableName} WHERE chat_id={chat_id}""")
    check = cursor.fetchall()
    if len(check) != 0:
        return True 
        # User already exist 
    else :
        # User does not exist 
        return False

def insertSubscriber(chat_id,asset,vendor,APIRequest) : 
    
    print (chat_id,asset,asset)
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""INSERT OR IGNORE INTO subscriber_{asset}_alerts(chat_id,vendor,APIRequest) VALUES ({chat_id},'{vendor}','{APIRequest}')""")
    conn.commit()
    conn.close()
    
    return 0

def deleteSubscriber(asset, chat_id) : 

    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    if checkIfUserIsAlreadyASubscriber("subscriber_"+asset+"_alerts",chat_id) == True : 
        cursor.execute(f"""DELETE FROM subscriber_{asset}_alerts WHERE chat_id = {chat_id}""")
        conn.commit()
        conn.close()
        return "You have been unsubsribed from "+asset+" alert !"
    else : 
        return "You can't unbsubsribe if you are not subscribed 😊"

