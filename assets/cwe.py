import requests
from assets.controller import *
from assets.controller import * 
from bs4 import BeautifulSoup

def cweSortedByYear(year) : 
    
    
    
    previousYear = year - 1
    year = str(year)
    
    response = requests.get("https://cwe.mitre.org/top25/archive/"+year+"/"+year+"_cwe_top25.html")
    
    if response.status_code == 404 :
        return "CWE aren't available for "+year
        
    soup = BeautifulSoup(response.text, 'html.parser')
    arrays = soup.findAll('table', attrs={"id":"Detail","style":"margin-left:auto; margin-right:auto;"})
    
    output = "🎯 CWE for :"+year+" 📝 \n"
    output += "Most Dangerous Software Weaknesses\n\n"
    tupleToStr = ""
    i = 0
    
    for _array in arrays:
        rows = _array.findAll('tr')
        i = i + 1
        if i == 2 : 
            break
        for row in rows :
            subrows = row.findAll('td')
            j = 1
            for subrow in subrows :
                if j == 1 : 
                    output += "\n"
                    tupleToStr = "".join(subrow.text)
                    output += "Rank : "+tupleToStr+"\n"
                if j == 2 : 
                    tupleToStr = "".join(subrow.text)
                    output += "ID : "+tupleToStr+"\n"
                if j == 3 : 
                    tupleToStr = "".join(subrow.text)+"\n"
                    output += "Name : "+tupleToStr
                if j == 4 : 
                    tupleToStr = "".join(subrow.text)+"\n"
                    output += "Score : "+tupleToStr
                if j == 5 : 
                    tupleToStr = "".join(subrow.text)+"\n"
                    output += str(previousYear)+" Rank Change : "+tupleToStr
                j = j + 1
        
        output += "\nCheck CWE for the previous year ? /Cwe@"+str(previousYear)+"\n"
    
    return output

def cwe_info(cwe) : 
    
    response = session.get('https://www.opencve.io/api/cwe/'+cwe+'')
    data = response.json()  
    if "id" in data : 
        _return = "" 
        _return += "ID : "+data["id"]+"\n"
        _return += "Name : "+data["name"]+"\n"
        _return += "Description : "+data["description"]+"\n"
        return _return
    else :
        return "CWE does not exist."
