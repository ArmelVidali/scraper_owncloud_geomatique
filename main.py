from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")


driver = webdriver.Firefox()

driver.get('http://owncloud.master-geomatique.org/index.php/login')

input_element = driver.find_element(
    By.CSS_SELECTOR, "#user")

input_element.send_keys(word["be"])
