# Imports necessary libraries.
# Beautifulsoup is a library for processing html data among other things.
from bs4 import BeautifulSoup
# selenium and webdriver are webscraping libraries that simulate a human accessing the website.
from selenium import webdriver

# This url is the url for the info page of the book Shadow Slave.
url = "https://www.lightnovelworld.com/novel/shadow-slave-05122222"

# I chose to use chrome as the webdriver because internet searches told me to, but you can supposedly use other browsers as well.
driver = webdriver.Chrome()

# Opens a chrome session with the url of Shadow Slave, and extracts the html data.
driver.get(url)
page = driver.page_source

# Writes the html data to a txt file for dev use.
with open("infodump.txt", "w", encoding="utf-8") as infodump:
    infodump.write(page)

# Finds the index range of the line in which the number of chapters is written.
lineStart = page.find('<meta name="description')
lineEnd = page.find('<meta name="keywords')

# Extracts the number of chapters by checking if elements in the string are numbers.
chapters = ""
for i in range(lineStart,lineEnd):
    if page[i].isnumeric():
        chapters += page[i]
chapters = int(chapters)

# Exits the chrome window.
driver.quit()