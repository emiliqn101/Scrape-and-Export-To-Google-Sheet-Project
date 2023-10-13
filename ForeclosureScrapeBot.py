import os
import requests
import json
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import requests
import json
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
from io import BytesIO
import os
import requests
import shutil
import pyautogui
import time
from selenium.webdriver.common.keys import Keys
import subprocess
from selenium.webdriver.common.action_chains import ActionChains
import csv
from bs4 import BeautifulSoup
import re


# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1pWSRX4EQaWBC4cYhImQ85wOK3Cyxmpg2fqp03v1AZWQ'
RANGE_NAME = 'Sheet1!A5'
names = []
urls = []
adresses = []
citys = []
states = []
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)
input("Have you logged in your foreclosure account? (Send Any Key To Continue): ")
cityname = input("Enter City Name: ")

# Function to authenticate with Google Sheets API
def authenticate_google_sheets():
    creds = None
    token_path = 'token.json'

    # Load the service account info from your JSON key file
    with open('webscraper-401215-16495de93ca3.json', 'r') as f:
        service_account_info = json.load(f)

    # Create a credentials object directly from the service account info
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

    # Check if the credentials are valid, refresh if necessary
    if not creds.valid:
        creds.refresh(Request())

    # Save the credentials to a file for future use
    with open(token_path, 'w') as token:
        token.write(json.dumps(service_account_info))

    return creds

# Function to update Google Sheet with data
def update_google_sheet(data):
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Define the starting cell for each type of data
    name_range = 'Sheet1!A1:A' + str(1 + len(data[0]))
    address_range = 'Sheet1!B1:B' + str(1 + len(data[1]))
    city_range = 'Sheet1!C1:C' + str(1 + len(data[2]))
    state_range = 'Sheet1!D1:D' + str(1 + len(data[3]))

    # Define the data for each range
    data_to_update = [
        {
            'range': name_range,
            'values': [[name] for name in data[0]]
        },
        {
            'range': address_range,
            'values': [[address] for address in data[1]]
        },
        {
            'range': city_range,
            'values': [[city] for city in data[2]]
        },
        {
            'range': state_range,
            'values': [[state] for state in data[3]]
        }
    ]

    # Specify the valueInputOption as "RAW" or "USER_ENTERED"
    value_input_option = "RAW"

    # Update the Google Sheet with the data
    try:
        result = sheet.values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={
                'valueInputOption': value_input_option,
                'data': data_to_update
            }
        ).execute()
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")



# Function to scrape data from the website
def scrape_foreclosure_data():
    resultsamm = driver.find_element(By.XPATH,'/html/body/div[3]/div[4]/div[1]/div[1]/div[1]/div/div/div[1]/strong').text
    indexsearch = 0
    if int(resultsamm)>=100:
        indexsearch = int(resultsamm)/100
    else:
        indexsearch = 2
    for i in range(1,round(indexsearch)):
        driver.get('https://www.foreclosure.com/listing/search?q='+cityname+'&ps=100&pg=1&o=pad&ob=asc&loc='+cityname+'&view=list&')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        elem = soup.find_all(class_='contViewDetails')
        for element in elem:
            link = element.find('a')['href']  # This extracts the 'href' attribute of the 'a' tag within the element
            urls.append(link)
        print(urls)
        for i in range(0,len(urls)-1):
            print("Item: "+str(len(names)+1))
            time.sleep(0.5)
            try:
                driver.get('https://www.foreclosure.com'+ urls[i])
            except Exception as f:
                print(f)
                break
            time.sleep(0.5)
            try:
                names.append("Defendant Name: "+driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[8]/ul[1]/li[3]/span[2]').text)
            except:
                try:
                    names.append("Trustee Name: "+driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[7]/ul[3]/li[3]/span[2]').text)
                except:  
                    try:
                        names.append("Trustee Name: "+driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[6]/ul[3]/li[1]/span[2]').text)
                    except:
                        names.append('N/A')
            try:
                adresses.append(driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[1]/div[1]/div[2]/h1[1]/span').text)
            except:
                adresses.append("N/A")
            try:
                citys.append((driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[1]/div[1]/div[2]/h1[2]/span').text).split(",")[0])
            except:
                citys.append("N/A")
            try:
                states.append((driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[1]/div[1]/div[2]/h1[2]/span').text).split(",")[1])
            except:
                states.append("N/A")
            print('Names: ',names)
            print("Address: ", adresses)
            print("City's: ",citys)
            print("Sate's: ",states)
            driver.back()
            time.sleep(0.5)

    data = [names, adresses, citys, states]  # Create a list of lists

    return data


# URL of the website
url = 'https://www.foreclosure.com/listing/search?q=Louisville,%20KY&lc=preforeclosure&pg=1&o=pad&ob=asc&loc=Louisville,%20KY&view=list&'

# Scrape data from the website
scraped_data = scrape_foreclosure_data()

# Update Google Sheet with the scraped data
update_google_sheet(scraped_data)
