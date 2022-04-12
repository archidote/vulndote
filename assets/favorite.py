
import sqlite3
import datetime as dt
from assets.controller import *
from assets.functions import cveFormatedForRegex 

def favorite(cve_id,chat_id) :         
            
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""INSERT OR IGNORE INTO favorite_cve(cve_id,date_fav,user_id) VALUES ('{cve_id}','{today}',{chat_id})""")
    conn.commit()
    conn.close()
    return cve_id+" was added to your fav list. 📒\n/favorised"


def listFavoriteCVE(chat_id) : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM favorite_cve WHERE user_id = {chat_id};""")
    results = cursor.fetchall()

    favList = ""
    for cve in results:
        favList += "📍"+cve[1]+"  -  🗓️ - "+cve[2]+"\n    ℹ️ : /Cve@"+cve[1].replace("-", "_")+"\n\n"
    favList += "<b><i>Sorted CVE by </i></b>: "
    return favList


def listFavoriteCVESortedByYear(chat_id) : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT cve_id, date_fav FROM favorite_cve WHERE user_id = {chat_id};""")
    results = cursor.fetchall()
    year = datetime.today().strftime('%Y')
    rows = results
    output = "Favorite CVEs for : "+year+"\n\n"
    for row in rows:  
        if year in row[1]:
            output += ""+row[0]+" -  ⭐ on ("+row[1]+")\n"
            output += "    ℹ️ : /Cve@"+cveFormatedForRegex(row[0])+"\n\n"
    return output

def listFavoriteCVESortedByThisMonth (chat_id) : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT cve_id, date_fav FROM favorite_cve WHERE user_id = {chat_id};""")
    results = cursor.fetchall()
    month = datetime.today().strftime('%Y-%m')
    rows = results
    output = "Favorite CVEs for : "+month+"\n\n"
    for row in rows:  
        if month in row[1]:
            output += ""+row[0]+" -  ⭐ on ("+row[1]+")\n"
            output += "    ℹ️ : /Cve@"+cveFormatedForRegex(row[0])+"\n\n"
    return output

def listFavoriteCVESortedByPreviousMonth (chat_id) : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT cve_id, date_fav FROM favorite_cve WHERE user_id = {chat_id};""")
    results = cursor.fetchall()
    previousMonth = (dt.date.today().replace(day=1) - dt.timedelta(days=1)).strftime("%m")
    year = datetime.today().strftime('%Y')
    yearParsedWithPreviousMonth = year+"-"+previousMonth
    if previousMonth == "12": 
        now = dt.datetime.now()
        last_year = now.year - 1
        yearParsedWithPreviousMonth = str(last_year)+"-"+previousMonth
    rows = results
    output = "Favorite CVEs for : "+yearParsedWithPreviousMonth+"\n\n"
    for row in rows:  
        if yearParsedWithPreviousMonth in row[1]:
            output += ""+row[0]+" -  ⭐ on ("+row[1]+")\n"
            output += "    ℹ️ : /Cve@"+cveFormatedForRegex(row[0])+"\n\n"
    return output

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
    conn.commit()
    conn.close()
    return cve+" was removed from your fav list."
