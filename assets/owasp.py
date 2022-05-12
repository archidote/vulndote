import requests
from bs4 import BeautifulSoup


def owaspTopTen() : 
    
    response = requests.get("https://owasp.org/www-project-top-ten/")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    t = soup.find("section", {"id": "sec-main"})
    rows = t.findAll('li')
    
    output = "🎯 OWASP Top 10 📝\n\n"
    
    for row in rows :
        for subrow in row.findAll('a',href=True) :
            output += row.text+"\n\n"
            # output += row.text+"<a href=\""+subrow["href"]+"> Link </a>\"\n\n"
    return output 

