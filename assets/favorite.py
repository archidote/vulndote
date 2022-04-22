
import sqlite3
import datetime as dt
from assets.controller import *
from assets.cveAdditionalInformation import cvssScale
from assets.functions import cveFormatedForRegex 

def favorite(cve_id,chat_id) :         
    
    cvss = cvssScale(cve_id)

    cursor.execute(f"""INSERT OR IGNORE INTO favorite_cve(cve_id,date_fav,user_id,cvss) VALUES ('{cve_id}', '{today}', {chat_id}, '{cvss}');""")
    dbConnexion.commit()
    return cve_id+" was added to your fav list. 📒\nTap /favorised to show your fav list."


def listFavoriteCVE(chat_id) : 
    
    cursor.execute(f"""SELECT * FROM favorite_cve WHERE user_id = {chat_id};""")
    dbConnexion.commit()
    results = cursor.fetchall()

    favList = ""
    for cve in results:
        favList += "📍"+cve[1]+"  -  🗓️ - "+cve[2]+"\n"
        favList += "    CVSS : "+cve[4]+"\n"
        favList += "    ℹ️ : /Cve@"+cveFormatedForRegex(cve[1])+"\n\n"
    favList += "<b><i>Sorted CVE by </i></b>: "
    return favList


def listFavoriteCVESortedByYear(chat_id) : 
    
    cursor.execute(f"""SELECT cve_id, date_fav, cvss FROM favorite_cve WHERE user_id = {chat_id};""")
    dbConnexion.commit()
    results = cursor.fetchall()
    year = datetime.today().strftime('%Y')
    rows = results
    output = "Favorite CVEs for : "+year+"\n\n"
    for row in rows:  
        if year in row[1]:
            output += ""+row[0]+" -  ⭐ on ("+row[1]+")\n"
            output += "    CVSS : "+row[2]+"\n"
            output += "    ℹ️ : /Cve@"+cveFormatedForRegex(row[0])+"\n\n"
    return output

def listFavoriteCVESortedByThisMonth (chat_id) : 
    
    cursor.execute(f"""SELECT cve_id, date_fav, cvss FROM favorite_cve WHERE user_id = {chat_id};""")
    results = cursor.fetchall()
    month = datetime.today().strftime('%Y-%m')
    rows = results
    output = "Favorite CVEs for : "+month+"\n\n"
    for row in rows:  
        if month in row[1]:
            output += ""+row[0]+" -  ⭐ on ("+row[1]+")\n"
            output += "    CVSS : "+row[2]+"\n"
            output += "    ℹ️ : /Cve@"+cveFormatedForRegex(row[0])+"\n\n"
    return output

def listFavoriteCVESortedByPreviousMonth (chat_id) : 
    
    cursor.execute(f"""SELECT cve_id, date_fav, cvss FROM favorite_cve WHERE user_id = {chat_id};""")
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
            output += "    CVSS : "+row[2]+"\n"
            output += "    ℹ️ : /Cve@"+cveFormatedForRegex(row[0])+"\n\n"
    return output

def isThisCVEIsFavorised(chat_id,cve) : 
    
    cursor.execute(f"""SELECT cve_id,user_id FROM favorite_cve WHERE user_id = {chat_id} AND cve_id = '{cve}';""")
    results = cursor.fetchall()
    dbConnexion.commit()
    
    if len(results) == 0 : 
        return "CVE is not registered as a fav asset."
    else : 
        fav = ""
        for cve in results:
            fav += "You have already favorised this cve."        
        return fav
    
def unfav(chat_id,cve) : # Faire une deuxième req select après pour vérifier si la a bien été viré de la table ou non (favorite_cve) condition if else et vérifier la longueur du tableau results
    
    cursor.execute(f"""SELECT cve_id,user_id FROM favorite_cve WHERE user_id = {chat_id} AND cve_id = '{cve}';""")
    results = cursor.fetchall()
    dbConnexion.commit()
    if len(results) == 0 :
        return cve+" is not registered in your fav list.\n Fav it ? ➡️ :/Cve@"+cveFormatedForRegex(cve)+"\n\n"
    else : 
        cursor.execute(f"""DELETE FROM favorite_cve WHERE user_id = {chat_id} AND cve_id = '{cve}';""")
        dbConnexion.commit()
        return cve+" was removed from your fav list."
        
