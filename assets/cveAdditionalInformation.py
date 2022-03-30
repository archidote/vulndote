from assets.controller import * 
from assets.functions import * 

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