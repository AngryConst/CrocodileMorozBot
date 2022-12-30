import requests
from lxml import html
import json

# Parse specific website to get tosts
def parseTosts():
    urls = []
    urls.append("https://pozdravok.com/toast/prazdnik/noviy-god/")
    tosts = []

    # going through all pages with tosts if there are more than one
    print("Hello")
    while True:
        r = requests.get(urls[-1])
        # print( r.text)
        with open("test.html", "wb") as outputFile:
            outputFile.write(r.text.encode("cp1251"))

        # Example of html
        # <link rel="next" title="Следующая - тосты на Новый год" href="/toast/prazdnik/noviy-god/2.htm" />
        tree = html.fromstring(r.text)
        linkNext = tree.xpath(
            '//link[@rel = "next"]/@href'
        )  # link tag with the attribute rel equial "next" - checking if other pages exist

        tostOnPage = tree.xpath('//p[@class = "sfst"]/text()')  # Get all tost text
        tostOnPageBegin = tree.xpath(
            '//p[@class = "sfst"]'
        )  # Get the beginning of tosts to split the text
        tostCount = len(tostOnPage)
        tostIndexes = []
        index = 0

        # Find all indexes where the new tost is started
        for currentTost in tostOnPageBegin:
            for i in range(index, tostCount):
                if currentTost.text == tostOnPage[i]:
                    index = i
                    tostIndexes.append(index)
                    ++index
                    break

        # Combine separate lines into tosts
        prev = 0
        indexesLength = len(tostIndexes)
        for i in range(0, indexesLength):
            lastIndex = tostIndexes[i + 1] if (i + 1) != indexesLength else tostCount
            tost = ""
            split4Lines = 1
            for j in range(tostIndexes[i], lastIndex):
                print(split4Lines)
                tost = (
                    tost + tostOnPage[j] + ("\n\n" if (split4Lines % 4 == 0) else "\n")
                )
                split4Lines = split4Lines + 1

            tosts.append(tost)

        # Check if website has another pages with tosts
        if len(linkNext) > 0:
            urls.append(urls[0] + linkNext[0].split("/")[-1])
            print(urls[-1])
        else:
            break

    return tosts


# Returns tosts from file, parse website if empty
def getTosts():
    tosts = []
    pathName = "./resources/tosts.json"
    with open(pathName, "r", encoding="utf-8") as j:
        try:
            tosts = json.load(j)
        except:
            tosts = []

    if len(tosts) == 0:
        tostsId = open(pathName, "w", encoding="utf-8")
        tosts = parseTosts()
        json.dump(tosts, tostsId, ensure_ascii=False, indent=4)

    return tosts
