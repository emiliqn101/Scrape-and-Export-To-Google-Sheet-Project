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

try:
    # Read the directory path from the text file
    with open('directory.txt', 'r') as file:
        txtdirectory = file.read().strip()

    # Command to change directory to the Chrome directory and launch Chrome with remote debugging
    combined_command = f'cd /d "{txtdirectory}" && chrome.exe --remote-debugging-port=9222'

    # Run the combined command
    subprocess.run(combined_command, shell=True, check=True)
except Exception as e:
    print(e)
