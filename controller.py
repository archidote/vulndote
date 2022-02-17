import requests
import os

oldURLApi = "https://cve.circl.lu/api/"
vulndoteUser = os.environ.get('vulndoteUser')
vulndotePassword = os.environ.get('vulndotePassword')
telegramBotToken= os.environ.get('telegramBotToken')

# print (vulndoteUser)
# print (vulndotePassword)

session = requests.Session()
session.auth = (vulndoteUser, vulndotePassword)
auth = session.post('https://www.opencve.io/api/')