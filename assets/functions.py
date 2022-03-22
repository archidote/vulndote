from numpy import product
from assets.controller import * 
from datetime import *
import urllib3
import sqlite3
import html 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def cveSearch(cveCode) : 
    
    if timeOutAPI() == True : 
        return "Api is not reachable at the moment"
    
    response = session.get('https://www.opencve.io/api/cve/'+cveCode+'')
    data = response.json() 

    
    if "message" in data : 
        return "CVE not found."
        
    else :
        cve = "" 
        cve += "<strong>CVE ID</strong> : "+data["id"]+"\n"
        cve += "<strong>CVSS</strong> : "+cvssScale((data["id"]))+"\n"
        cve += "<strong>Summary</strong> : "+html.escape(data["summary"],quote=True)+"\n"
        cve += "<strong>Published/Updated</strong> : "+formatDateAndTime(data["updated_at"])+"\n\n"
        return cve 

def cvssScale(cve): 
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 

    if data["cvss"]["v3"] < 4 : 
        return ""+str(data["cvss"]["v3"])+" 🔵"
    elif data["cvss"]["v3"] < 7 : 
        return ""+str(data["cvss"]["v3"])+" 🟠" 
    elif data["cvss"]["v3"] < 9 : 
        return ""+str(data["cvss"]["v3"])+" 🔴"
    else : 
        return ""+str(data["cvss"]["v3"])+" ⚫"

def cveReferences(cve) :
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 

    
    if "message" in data : 
        return "CVE not found."
        
    else :
        cve = "" 
        cve += "<strong>CVE ID</strong>: "+data["id"]+"\n\n"
        num = 1
        for i in range(len(data["raw_nvd_data"]["cve"]["references"]["reference_data"])) :
            cve += ""+str(num)+" : "+data["raw_nvd_data"]["cve"]["references"]["reference_data"][i]["refsource"]+" : 🔗 <a href='"+data["raw_nvd_data"]["cve"]["references"]["reference_data"][i]["url"]+"'>Link</a>\n"
            num = num + 1  
        return cve 

def vulnerableProductsOrVendors(cve) : 
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 

    
    if "message" in data : 
        return "CVE not found."
        
    else :
        cve = "" 
        cve += "<strong>CVE ID</strong>: "+data["id"]+"\n\n"
        for key in data["vendors"] :
            cve += "📦<strong> "+key+"</strong> : \n"
            for v in data["vendors"][key] : 
                product = ""
                product += ''.join(v)
                cve += "    🔹"+product+"\n"
        return cve 
            
def moreInfo(cve) :
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 

    
    if "message" in data : 
        return "CVE not found."
        
    else :
        impact = "<b>CVE</b> : "+data["id"]+"\n"
        impact += "<b>CVSS version</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["version"]+"\n\n"
        impact += "<b>Attack Vector</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["attackVector"]+"\n"
        impact += "<b>Attack Complexity</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["attackComplexity"]+"\n"
        impact += "<b>Raw CVSS Vector</b> : \n\n"
        impact += ""+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["vectorString"]+"\n\n"
        impact += "<b>Attack Complexity</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["attackComplexity"]+"\n"
        impact += "<b>Availibility Impact</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["availabilityImpact"]+"\n"
        impact += "<b>Privileges required ?</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["privilegesRequired"]+"\n"
        impact += "<b>Confidentiality</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["confidentialityImpact"]+"\n\n"
        impact += "<b>Impact Score</b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["impactScore"])+"\n"
        impact += "<b>Exploitability Score</b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["exploitabilityScore"])+"\n\n"
        impact += "<i>If you don't understand terms</i> : /terminology"
        
        return impact 
                
def terminology() : 
    
    terms = """ 

<b>CVE</b> : Common Vulnerabilities and Exposures
    ℹ️  <a href="https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures">🔗 Link</a>
<b>CVSS</b> : Common Vulnerability Scoring System (0->10)
    ℹ️  <a href="https://en.wikipedia.org/wiki/Common_Vulnerability_Scoring_System">🔗 Link</a>
<b>CVSS-Vector</b> : AV:N/AC:L/Au:N/C:N/I:N/A:P
    ℹ️ cvss-vector (v2): <a href="https://www.first.org/cvss/v2/guide">🔗 Link</a>
    ℹ️ cvss-vector (v3): <a href="https://www.first.org/cvss/calculator/3.0">🔗 Link</a>
<b>CWE</b> : Common Weakness Enumeration
    ℹ️ <a href="https://en.wikipedia.org/wiki/Common_Weakness_Enumeration">🔗 Link</a>
<b>CPE</b> : Common Platform Enumeration
    ℹ️ <a href="https://en.wikipedia.org/wiki/Common_Platform_Enumeration">🔗 Link</a>
    """
    return terms

def cveReformated(cveNotFormated) : 
    
    cveReFormated = cveNotFormated
    cveReFormated = cveReFormated.replace("_", "-")
    cveReFormated = cveReFormated.replace("/Cve@", "")
    
    return cveReFormated

def timeOutAPI() : 
    try : 
        r = session.get("https://www.opencve.io/")
        return False
    except : 
        return True # Api can't be reached ! 

def hello(chat_id,first_name,started_bot_date): 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    cursor.execute(f"""INSERT OR IGNORE INTO user(id,first_name,started_bot_date) VALUES ({chat_id},'{first_name}','{started_bot_date}')""")
    conn.commit()
    conn.close()
    
    return 0

def favorite(cve_id,chat_id) :         
            
    today = date.today()
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
    

    
def formatDateAndTime(date) : 
    d = datetime.fromisoformat(date[:-1]).astimezone(timezone.utc)
    return d.strftime('%Y-%m-%d at %H:%M:%S')
# print (impact("CVE-2021-29987"))
# print(cveReferences("CVE-2021-29987"))
# print (vulnerableProductsOrVendors("CVE-2017-0144"))
# print (timeOutAPI())
