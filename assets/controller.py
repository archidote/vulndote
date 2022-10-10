
import requests
import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime

# TOKEN FROM /.ENV file 

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPEN_CVE_API_USERNAME = os.getenv('OPEN_CVE_API_USERNAME')
OPEN_CVE_API_PASSWORD = os.getenv('OPEN_CVE_API_PASSWORD')
GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY = os.getenv('GITHUB_TOKEN_READ_ONLY_PUBLIC_REPOSITORY')

OPEN_CVE_API_URL = "https://www.opencve.io/api/cve/"
OPEN_CVE_API_URL_PARAMS = "https://www.opencve.io/api/cve?"
CVE_NOT_FOUND = "CVE was not found."
VENDOR_OR_PRODUCT_NOT_FOUND = "Vendor or product was not found."
NO_CVE_HAVE_BEEN_REGISTERED_TODAY_FOR = "No CVE have been registered Today for "

session = requests.Session()
session.auth = (OPEN_CVE_API_USERNAME, OPEN_CVE_API_PASSWORD)
auth = session.post('https://www.opencve.io/api/')

database_path = os.path.expanduser("~")+"/databases_projects/vulndote/vulndote.db" #  /home/$USER/databases_projects/vulndote/vulndote.db
dbConnection = sqlite3.connect(database_path,check_same_thread=False)
cursor = dbConnection.cursor()


today = now = datetime.now()
today = now.strftime("%Y-%m-%d")
todayHS = now.strftime("%Y-%m-%d %H:%M:%S")

currentYear = now.strftime("%Y")


