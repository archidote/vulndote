import requests
import os

oldURLApi = "https://cve.circl.lu/api/"
vulndoteUser = os.environ.get('vulndoteUser')
vulndotePassword = os.environ.get('vulndotePassword')
telegramBotToken = os.environ.get('telegramBotToken')
GITHUB_ACCESS_TOKEN = os.environ.get('gihtubArchidoteTokenReadPublicRepos')

session = requests.Session()
session.auth = (vulndoteUser, vulndotePassword)
auth = session.post('https://www.opencve.io/api/')