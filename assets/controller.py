from datetime import datetime
from django import db
import requests
import os
import sqlite3

VULNDOTE_API_USERNAME = os.environ.get('VULNDOTE_API_USERNAME')
VULNDOTE_API_PASSWORD = os.environ.get('VULNDOTE_API_PASSWORD')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY = os.environ.get('GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY')


session = requests.Session()
session.auth = (VULNDOTE_API_USERNAME, VULNDOTE_API_PASSWORD)
auth = session.post('https://www.opencve.io/api/')

dbConnexion = sqlite3.connect('assets/vulndote.db',check_same_thread=False)
cursor = dbConnexion.cursor()

today = now = datetime.now()
today = now.strftime("%Y-%m-%d")

