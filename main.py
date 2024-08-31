from bs4 import BeautifulSoup
from selenium import webdriver
url = "https://www.lightnovelworld.com/novel/shadow-slave-05122222"
driver = webdriver.Chrome()

page = driver.get(url)

driver.quit()