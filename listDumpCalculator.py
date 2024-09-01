from listDump import *
print("Number of chapters in web novel so far:")
print(len(chapterScrape), "\n")
print("Number of words in web novel so far:")
print(sum(chapterScrape), "\n")
print("Number of pages in web novel so far:")
print(sum(chapterScrape)/500)