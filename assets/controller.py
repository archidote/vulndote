
from datetime import datetime
import requests
import os
import sqlite3

OPEN_CVE_API_USERNAME = os.environ.get('OPEN_CVE_API_USERNAME')
OPEN_CVE_API_PASSWORD = os.environ.get('OPEN_CVE_API_PASSWORD')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY = os.environ.get('GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY')
OPEN_CVE_API_URL = "https://www.opencve.io/api/cve/"
OPEN_CVE_API_URL_PARAMS = "https://www.opencve.io/api/cve?"
CVE_NOT_FOUND = "CVE was not found."
VENDOR_OR_PRODUCT_NOT_FOUND = "Vendor or product was not found."

session = requests.Session()
session.auth = (OPEN_CVE_API_USERNAME, OPEN_CVE_API_PASSWORD)
auth = session.post('https://www.opencve.io/api/')

dbConnexion = sqlite3.connect('assets/vulndote.db',check_same_thread=False)
cursor = dbConnexion.cursor()

today = now = datetime.now()
today = now.strftime("%Y-%m-%d")
todayHS = now.strftime("%Y-%m-%d %H:%M:%S")

currentYear = now.strftime("%Y")


