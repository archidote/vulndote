from assets.controller import *

def checkIfUserIsAlreadyASubscriber(tableName,chat_id):
    
    cursor.execute(f"""SELECT chat_id FROM {tableName} WHERE chat_id={chat_id}""")
    check = cursor.fetchall()
    if len(check) != 0:
        return True 
        # User already exist 
    else :
        # User does not exist 
        return False

def insertSubscriber(chat_id,asset,vendor,api_request) : 
    
    cursor.execute(f"""SELECT chat_id FROM subscriber_vendor_alerts WHERE chat_id = {chat_id} ;""")
    results = cursor.fetchall()
    dbConnexion.commit()
    if len(results) == 0 :
        cursor.execute(f"""INSERT OR IGNORE INTO subscriber_{asset}_alerts(chat_id,vendor,api_request,refresh_date) VALUES ({chat_id},'{vendor}','{api_request}','{today}')""")
        dbConnexion.commit()
    else : 
        cursor.execute(f"""UPDATE subscriber_{asset}_alerts SET vendor = '{vendor}',api_request = '{api_request}',refresh_date = '{today}' WHERE chat_id = {chat_id}""")
        dbConnexion.commit()
    dbConnexion.commit()

def deleteSubscriber(asset, chat_id) : 

    if checkIfUserIsAlreadyASubscriber("subscriber_"+asset+"_alerts",chat_id) == True : 
        cursor.execute(f"""DELETE FROM subscriber_{asset}_alerts WHERE chat_id = {chat_id}""")
        dbConnexion.commit()
        
        return "You have been unsubsribed from "+asset+" alert !"
    else : 
        return "You can't unbsubsribe if you are not subscribed 😊"

