from assets.controller import * 
from assets.functions import * 
import html 

def cveSearch(cveCode,statusCode) : 
    
    cveCode = cveReformated(cveCode)
    
    if timeOutAPI() == True : 
        return "Api is not reachable at the moment"
    
    response = session.get('https://www.opencve.io/api/cve/'+cveCode+'')
    data = response.json() 
    
    if statusCode == 0 : 
        if "message" in data : 
            return CVE_NOT_FOUND
        else :
            cveInfo = ""
            cveInfo += "<b>CVE ID</b> : "+data["id"]+"\n"
            cveInfo += "<b>CVSS</b> "+cvssScale((data["id"]))+"\n"
            cveInfo += "<b>Summary</b> : "+html.escape(data["summary"],quote=True)+"\n"
            cveInfo += "<b>Updated</b> : "+formatDateAndTime(data["updated_at"])+"\n\n"
            cveInfo += "<u>Published</u> : "+formatDateAndTime(data["created_at"])+"\n"
            return cveInfo
    else :    
        if "message" in data : 
            return CVE_NOT_FOUND
        else :
            cveInfo = cveCommonInfo(data)
            return cveInfo
        
    
def cvssScale(cve): 
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 
    print (data)
    if data["cvss"]["v2"] != None or data["cvss"]["v3"] != None : # Sometimes a CVSS score could not be fetched, if the CVE has been revoked or rejected for any reasons
        if data["cvss"]["v3"] != None :
            if data["cvss"]["v3"] < 4 : 
                return "v3 : "+str(data["cvss"]["v3"])+" 🔵"
            elif data["cvss"]["v3"] < 7 : 
                return "v3 : "+str(data["cvss"]["v3"])+" 🟠" 
            elif data["cvss"]["v3"] < 9 : 
                return "v3 : "+str(data["cvss"]["v3"])+" 🔴"
            else : 
                return "v3 : "+str(data["cvss"]["v3"])+" ⚫"
        else : 
            if data["cvss"]["v2"] < 4 : 
                return "v2 : "+str(data["cvss"]["v2"])+" 🔵"
            elif data["cvss"]["v2"] < 7 : 
                return "v2 : "+str(data["cvss"]["v2"])+" 🟠" 
            elif data["cvss"]["v2"] < 9 : 
                return "v2 : "+str(data["cvss"]["v2"])+" 🔴"
            else : 
                return "v2 : "+str(data["cvss"]["v2"])+" ⚫"
    else : 
        return ": CVSS score is not available."

def cveReferences(cve) :
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 

    print (data)
    if "message" in data : 
        return CVE_NOT_FOUND
        
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
        return CVE_NOT_FOUND
        
    else :
        if  len(data["vendors"]) == 0 : 
            return "No products is impacted by "+cve
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
        return CVE_NOT_FOUND
        
    else :
        if data["cvss"]["v3"] :
 
            output = "<b>CVE</b> : "+data["id"]+"\n"
            output +=  "<b>CVSS version</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["version"]+"\n\n"
            output +=  "<b>Attack Vector</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["attackVector"]+"\n"
            output +=  "<b>Attack complexity </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["attackComplexity"])+"\n"
            output +=  "<b>Raw CVSS Vector</b> : \n\n"
            output +=  ""+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["vectorString"]+"\n\n"
            
            output +=  "<u><b>Impact</b></u> : \n"
            output +=  "<b>    Integrity</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["integrityImpact"]+"\n"
            output +=  "<b>    Availibility</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["availabilityImpact"]+"\n"
            output +=  "<b>    Confidentiality</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["confidentialityImpact"]+"\n"
            output +=  "<b>    Impact Score : </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["impactScore"])+"\n\n"
            
            output += "<u><b>Others Metrics</b></u> : \n"
            output +=  "<b>    Severity </b> : "+data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["baseSeverity"]+"\n"
            output +=  "<b>    Privileges required ? </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["privilegesRequired"])+"\n"
            output +=  "<b>    User interaction ? </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["cvssV3"]["userInteraction"])+"\n"
            output +=  "<b>    Exploitability Score ? </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV3"]["exploitabilityScore"])+"\n\n"
            
            output +=  "<i>If you don't understand terms</i> : /terminology"

            
        else : # V2

            output = "<b>CVE</b> : "+data["id"]+"\n"
            output +=  "<b>CVSS version</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV2"]["cvssV2"]["version"]+"\n\n"
            output +=  "<b>Attack Vector</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV2"]["cvssV2"]["accessVector"]+"\n"
            output +=  "<b>Attack Complexity</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV2"]["cvssV2"]["accessComplexity"]+"\n\n"
            output +=  "<b>Raw CVSS Vector</b> : \n\n"
            output +=  ""+data["raw_nvd_data"]["impact"]["baseMetricV2"]["cvssV2"]["vectorString"]+"\n\n"
            
            output +=  "<u><b>Impact</b></u> : \n"
            output +=  "<b>    Integrity</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV2"]["cvssV2"]["integrityImpact"]+"\n"
            output +=  "<b>    Availibility</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV2"]["cvssV2"]["availabilityImpact"]+"\n"
            output +=  "<b>    Confidentiality</b> : "+data["raw_nvd_data"]["impact"]["baseMetricV2"]["cvssV2"]["confidentialityImpact"]+"\n"
            output +=  "<b>    Impact Score : </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV2"]["impactScore"])+"\n\n"
            
            output +=  "<u><b>Attack Vectors</b></u> : \n"
            output +=  "<b>    Severity</b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV2"]["severity"])+"\n"
            output +=  "<b>    Authentification ? </b> : "+data["raw_nvd_data"]["impact"]["baseMetricV2"]["cvssV2"]["authentication"]+"\n"
            output +=  "<b>        Obtain All Privileges ? </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV2"]["obtainAllPrivilege"])+"\n"
            output +=  "<b>        Obtain All Privileges ? </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV2"]["obtainUserPrivilege"])+"\n"
            output +=  "<b>        Obtain All Privileges ? </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV2"]["obtainOtherPrivilege"])+"\n"
            output +=  "<b>        Obtain All Privileges ? </b> : "+str(data["raw_nvd_data"]["impact"]["baseMetricV2"]["userInteractionRequired"])+"\n\n"
            
            output +=  "<i>If you don't understand terms</i> : /terminology"

        return output
    
def cveCommonInfo(data) :
               
    cveInfo = ""
    cveInfo += "<b>CVE ID</b> : "+data["id"]+"\n"
    cveInfo += "<b>CVSS</b> "+cvssScale((data["id"]))+"\n"
    cveInfo += "<b>Summary</b> : "+html.escape(cutSummary(data["summary"]),quote=True)+"\n"
    cveInfo += "<b>Updated</b> : "+formatDateAndTime(data["updated_at"])+"\n"
    cveInfo += "<u>Published</u> : "+formatDateAndTime(data["created_at"])+"\n\n"
    cveIdFormated=data["id"].replace("-", "_")
    cveInfo += "ℹ️ : /Cve@"+cveIdFormated+"\n\n"
    return cveInfo

def cutSummary(summary) :

    if len(summary) > 400 :
        return summary[:400]+"(...)"
    else :
        return summary
