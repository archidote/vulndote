from datetime import timezone
from assets.controller import * 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
               
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
    cveReFormated = cveReFormated.replace("/unfav@", "")
    
    return cveReFormated

def cweReformated(cveNotFormated) : 
    
    cveReFormated = cveNotFormated
    cveReFormated = cveReFormated.replace("/Cwe@", "")
    
    return cveReFormated

def cveFormatedForRegex(cveNotFormated) : 
    
    cveReFormated = cveNotFormated
    cveReFormated = cveReFormated.replace("-", "_")
    
    return cveReFormated

def summaryRegex(summary) :
    sum = summary.replace("&amp;", "and")
    return sum 

def timeOutAPI() : 
    try : 
        r = session.get("https://www.opencve.io/")
        return False
    except : 
        return True # Api can't be reached ! 

def hello(chat_id,first_name,started_bot_date): 
    
    cursor.execute(f"""INSERT OR IGNORE INTO user(id,first_name,started_bot_date) VALUES ({chat_id},'{first_name}','{started_bot_date}')""")
    dbConnexion.commit()
    return 0

def getVendorOrProduct(chat_id): 
    
    cursor.execute(f"""SELECT vendor FROM subscriber_vendor_alerts WHERE chat_id = {chat_id}""")
    dbConnexion.commit()
    vendor = cursor.fetchall()
    return vendor[0][0] 

def formatDate(rawDate) : # Facto possible avec les deux fonctions ci-desssous
    
    res = rawDate.split("T")[0]
    return res

def formatDateAndTime(date) : 
    
    d = datetime.fromisoformat(date[:-1]).astimezone(timezone.utc)
    return d.strftime('%Y-%m-%d at %H:%M:%S')
