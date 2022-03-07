from numpy import product
from controller import * 
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def cveSearch(cveCode) : 
    
    if timeOutAPI() == True : 
        return "Api is not reachable at the moment"
    
    response = session.get('https://www.opencve.io/api/cve/'+cveCode+'')
    data = response.json() 

    
    if "message" in data : 
        return "CVE has'nt been found."
        
    else :
        cve = "" 
        cve += "<strong>CVE ID</strong> : "+data["id"]+"\n"
        cve += "<strong>CVSS</strong> : "+cvssScale((data["id"]))+"\n"
        cve += "<strong>Summary</strong> : "+data["summary"]+"\n"
        cve += "<strong>Published/Updated</strong> : "+data["updated_at"]+"\n\n"
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
        return "CVE has'nt been found."
        
    else :
        cve = "" 
        cve += "<strong>CVE ID</strong>: "+data["id"]+"\n\n"
        for i in range(len(data["raw_nvd_data"]["cve"]["references"]["reference_data"])) :
            cve += ""+str(i)+" : "+data["raw_nvd_data"]["cve"]["references"]["reference_data"][i]["refsource"]+" : 🔗 <a href='"+data["raw_nvd_data"]["cve"]["references"]["reference_data"][i]["url"]+"'>Link</a>\n"
        return cve 

def vulnerableProductsOrVendors(cve) : 
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 

    
    if "message" in data : 
        return "CVE has'nt been found."
        
    else :
        cve = "" 
        cve += "<strong>CVE ID</strong>: "+data["id"]+"\n\n"
        for key in data["vendors"] :
            cve += "➡️<strong>"+key+"</strong> : \n"
            for v in data["vendors"][key] : 
                product = ""
                product += ''.join(v)
                cve += "    🔹"+product+"\n"
        return cve 
            
def moreInfo(cve) :
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 

    
    if "message" in data : 
        return "CVE has'nt been found."
        
    else :
        impact = "CVE : "+data["id"]+"\n"
        impact += "CVSS version : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["version"]+"\n\n"
        impact += "Attack Vector : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["attackVector"]+"\n"
        impact += "Attack Complexity : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["attackComplexity"]+"\n"
        impact += "Raw CVSS Vector: \n"
        impact += "➡️"+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["vectorString"]+"\n\n"
        impact += "Attack Complexity : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["attackComplexity"]+"\n"
        impact += "Availibility Impact : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["availabilityImpact"]+"\n"
        impact += "Privileges ? : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["privilegesRequired"]+"\n"
        impact += "Confidentiality : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["confidentialityImpact"]+"\n\n"
        impact += "Impact Score : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["impactScore"])+"\n"
        impact += "Exploitability Score : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["exploitabilityScore"])+"\n"
        
        return impact 
                
def terminology() : 
    
    terms = """ 
TERMINOLOGY : 

CVE : Common Vulnerabilities and Exposures
CVSS : Common Vulnerability Scoring System (0->10)
CVSS-Vector : AV:N/AC:L/Au:N/C:N/I:N/A:P
    More info cvss-vector (v2): https://www.first.org/cvss/v2/guide 
    More info cvss-vector (v3): https://www.first.org/cvss/calculator/3.0
CWE : Common Weakness Enumeration
    More Info : https://fr.wikipedia.org/wiki/Common_Weakness_Enumeration
CPE : Common Platform Enumeration
    More info : https://en.wikipedia.org/wiki/Common_Platform_Enumeration
    
    """
    return terms

def cveReformated(cveNotFormated) : 
    
    cveReFormated = cveNotFormated
    cveReFormated = cveReFormated.replace("_", "-")
    cveReFormated = cveReFormated.replace("/Cve@", "")
    
    return cveReFormated

def timeOutAPI() : # TO-DO
    try : 
        r = session.get("https://www.opencve.io/")
        return False
    except : 
        return True # Api can't be reached ! 

# print (impact("CVE-2021-29987"))
# print(cveReferences("CVE-2021-29987"))
# print (vulnerableProductsOrVendors("CVE-2017-0144"))
# print (timeOutAPI())