import datetime as dt
from assets.controller import *
from assets.cveAdditionalInformation import cvssScale
from assets.functions import cveFormatedForRegex 

def favorite(cve_id,chat_id) :         
    
    cvss = cvssScale(cve_id)

    cursor.execute(f"""INSERT OR IGNORE INTO favorite_cve(cve_id,date_fav,user_id,cvss) VALUES ('{cve_id}', '{today}', {chat_id}, '{cvss}');""")
    dbConnexion.commit()
    return cve_id+" was added to your fav list. 📒\nTap /favorised to show your fav list."


def checkRowForFavorite(rows,Datetime) : 
    output = "Favorite CVEs for : "+Datetime+"\n\n"
    for row in rows:  
        if Datetime in row[1] or Datetime == "notSorted" :
            output += ""+row[0]+" -  ⭐ on ("+row[1]+")\n"
            output += "    CVSS : "+row[2]+"\n"
            output += "    ℹ️ : /Cve@"+cveFormatedForRegex(row[0])+"\n\n"            
    return output

def listFavoriteCVE(chat_id,t) : 
    
    cursor.execute(f"""SELECT cve_id, date_fav, cvss FROM favorite_cve WHERE user_id = {chat_id};""")
    dbConnexion.commit()
    rows = cursor.fetchall()
    
    if t == "Fav_Sorted_By_This_Year" : 
        Datetime = datetime.today().strftime('%Y')
        return checkRowForFavorite(rows,Datetime)
    elif t == "Fav_Sorted_By_This_Month" :
        Datetime = datetime.today().strftime('%Y-%m')
        return checkRowForFavorite(rows,Datetime)
    elif t == "Fav_Sorted_By_Last_Month" :
        previousMonth = (dt.date.today().replace(day=1) - dt.timedelta(days=1)).strftime("%m")
        year = datetime.today().strftime('%Y')
        yearParsedWithPreviousMonth = year+"-"+previousMonth
        if previousMonth == "12": 
            now = dt.datetime.now()
            last_year = now.year - 1
            yearParsedWithPreviousMonth = str(last_year)+"-"+previousMonth
            return checkRowForFavorite(rows,yearParsedWithPreviousMonth)
        else : 
            return checkRowForFavorite(rows,yearParsedWithPreviousMonth)
    else : # Not sorted by year
        return checkRowForFavorite(rows,"notSorted")

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
        
