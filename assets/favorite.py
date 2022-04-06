
import sqlite3
from assets.controller import * 

def favorite(cve_id,chat_id) :         
            
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""INSERT OR IGNORE INTO favorite_cve(cve_id,date_fav,user_id) VALUES ('{cve_id}','{today}',{chat_id})""")
    conn.commit()
    conn.close()
    return "saved as a fav"
    
    # return "CVE :"+cve_id+" was favorised. \n /favorised to list all your favorised CVE"

def listFavoriteCVE(chat_id) : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM favorite_cve WHERE user_id = {chat_id};""")
    results = cursor.fetchall()

    favList = ""
    for cve in results:
        favList += "📍"+cve[1]+"  -  🗓️ - "+cve[2]+"\n    ℹ️ : /Cve@"+cve[1].replace("-", "_")+"\n\n"
    return favList

def isThisCVEIsFavorised(chat_id,cve) : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT cve_id,user_id FROM favorite_cve WHERE user_id = {chat_id} AND cve_id = '{cve}';""")
    results = cursor.fetchall()
    conn.commit()
    conn.close()

    if len(results) == 0 : 
        return "CVE is not registered as a fav asset."
    else : 
        fav = ""
        for cve in results:
            fav += "You have already favorised this cve."        
        return fav
    
def unfav(chat_id,cve) : # Faire une deuxième req select après pour vérifier si la a bien été viré de la table ou non (favorite_cve) condition if else et vérifier la longueur du tableau results
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM favorite_cve WHERE user_id = {chat_id} AND cve_id = '{cve}';""")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    print (results)
    return "CVE :"+cve+" was removed from your fav list."