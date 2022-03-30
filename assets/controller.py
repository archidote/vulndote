from datetime import datetime
import requests
import os

VULNDOTE_API_USERNAME = os.environ.get('VULNDOTE_API_USERNAME')
VULNDOTE_API_PASSWORD = os.environ.get('VULNDOTE_API_PASSWORD')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY = os.environ.get('GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY')


session = requests.Session()
session.auth = (VULNDOTE_API_USERNAME, VULNDOTE_API_PASSWORD)
auth = session.post('https://www.opencve.io/api/')
today = now = datetime.now()
today = now.strftime("%Y-%m-%d")