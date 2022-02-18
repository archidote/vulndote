from controller import * 

def cvssScale(cve): 
    
    response = session.get('https://www.opencve.io/api/cve/'+cve+'')
    data = response.json() 

    if data["cvss"]["v3"] < 4 : 
        return ""+str(data["cvss"]["v3"])+" 🟢"
    elif data["cvss"]["v3"] < 7 : 
        return ""+str(data["cvss"]["v3"])+" 🟡" 
    elif data["cvss"]["v3"] < 9 : 
        return ""+str(data["cvss"]["v3"])+" 🟠"
    else : 
        return ""+str(data["cvss"]["v3"])+" 🔴"

def cveSearch(cveCode) : 
    
    response = session.get('https://www.opencve.io/api/cve/'+cveCode+'')
    data = response.json() 

    
    if "message" in data : 
        return "CVE has'nt been found."
        
    else : 
        cve = ""
        cve += "<b>CVE ID</b> : "+data["id"]+"\n"
        cve += "<b>CVSS</b> : "+cvssScale((data["id"]))+"\n"
        cve += "<b>Summary</b> : "+data["summary"]+"\n"
        cve += "<b>Published/Updated</b> : "+data["updated_at"]+"\n\n"
        
        return cve 
