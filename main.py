# Action chains are neat for chaining actions for if the thing you want to click is hidden behind a closed shadow root.
from selenium.webdriver.common.action_chains import ActionChains
# The By class allows you too look for elements by their traits (class, id, etc.).
from selenium.webdriver.common.by import By
# Just like selenium, except it can't be detected by cloudflare's bot blockers.
from undetected_chromedriver import Chrome

# # This part deals with finding the number of current chapters.
# This url is the url for the info page of the book Shadow Slave.
url = "https://www.lightnovelworld.com/novel/shadow-slave-05122222"

# I chose to use chrome as the webdriver because internet searches told me to, but you can supposedly use other browsers as well.
driver = Chrome()

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



# # This part deals with counting the number of words in each chapter.
# A number can be added to this incomplete url to be directed to a chapter for that number.
urlChapterBase = "https://www.lightnovelworld.com/novel/shadow-slave-1365/chapter-"

# Searches through each chapter in a for loop starting with the first, and counts the number of spaces and html paragraphs, as this added together should be the number of words.
wordCountList = []
for i in range(1, chapters+1):
    driver.get(urlChapterBase + str(i))

    # The loop ensures that it actually gets the word count from the page, as selenium/undetected_chromedriver has a tendency to note down the word count for the cloudflare check (0).
    run = True
    while run:
        # I first tried having a counter tick up for each loop, and then try checking off the box when the counter got too high, being a sign that the cloudflare got triggered, but an easier AND faster method I found was to just use a try clause, which will give an error if the cloudflare wasn't triggered, and has the unintended effect of instantly clicking the cloudflare's checkbox and leaving no room for accidentally clicking too soon and getting the program stuck.
        try:
            checkBox = driver.find_element(By.ID, "qhVO3")
            action = ActionChains(driver)
            # I set an action sequence to look for the general area of the checkbox (it's inside 2 closed shadow roots, so it's a pain to find the exact location of), and then calculated the general area where the box you have to click is, and offset the click by as much. I think it might be prone to error with different resolutions, so if the program gets stuck on the checkbox, try adjusting the offset (you can find the resolution of the checkbox area by looking for the above ID and clicking on it with the inspect tool).
            action.move_to_element_with_offset(checkBox, xoffset=-428, yoffset=0).click().perform()
        except:
            pass
        page = driver.page_source

        # The only part of the web page with the paragraph name is the actual content of the chapter, which made finding the start of the chapter really easy.
        chapterStart = page.find("<p>")
        # This div is always at the end of the chapter, so finding the start of it will find the end of the chapter content.
        chapterEnd = page.find('<div class="chapternav skiptranslate">')
        # Spaces + "line breaks" (ends of paragraphs) should equate to the number of words, tho spelling mistakes where words are combined or split and dashes like " - " might give a not 100% correct number.
        spaces = page[chapterStart:chapterEnd].count(" ")
        # I could've looked for <p>s as well, as every end of a paragraph needs a beginning, but for satisfaction's sake, I looked for the ends of each paragraph.
        lineBreaks = page[chapterStart:chapterEnd].count("</p>")
        wordCount = spaces + lineBreaks

        # This is the part that looks for whether the word count isn't 0 (the program working as intended).
        if wordCount != 0:
            wordCountList.append(wordCount)
            run = False

    # # This part is a dev tool to see how the page code is formatted.
    # with open("infodump2.txt", "w", encoding="utf-8") as infodump2:
    #     infodump2.write(page)

# The list allows you to see the number of words in each chapter.
print(wordCountList)

# As it's not a physical book, the number of pages has to be calculated using a rule of thumb (one page being 500 words). This is not 100% accurate, obviously, but that's what you get for trying to find the number of pages of a book *without pages*. Calculating the number of pages from the number of characters might be more accurate, but like I think this way is good enough.
print("Number of words in web novel so far:")
print(sum(wordCountList), "\n")
print("Number of pages in web novel so far:")
print(sum(wordCountList)/500)

# Exits the chrome window.
driver.quit()