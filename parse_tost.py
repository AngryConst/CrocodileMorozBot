import requests
from lxml import html
import json

def parseTosts():
  urls = []
  urls.append('https://pozdravok.com/toast/prazdnik/noviy-god/')
  tosts = []

  while True:
    r = requests.get( urls[-1] )
    #print( r.text)
    with open('test.html', 'wb') as outputFile:
      outputFile.write(r.text.encode('cp1251'))

    #<link rel="next" title="Следующая - тосты на Новый год" href="/toast/prazdnik/noviy-god/2.htm" />
    #movie_desc = item_lxml.xpath('.//div[@class = "nameRus"]/a/text()')[0]
    tree = html.fromstring(r.text)
    linkNext = tree.xpath('//link[@rel = "next"]/@href') # link тег с атрибутом rel равным "next" - проверяем есть ли ещё страницы

    tostOnPage = tree.xpath('//p[@class = "sfst"]/text()') # Get all tost text
    tostOnPageBegin = tree.xpath('//p[@class = "sfst"]') # Get the beginning of tosts to split the text
    tostCount = len(tostOnPage)
    tostIndexes = []
    index = 0

    for currentTost in tostOnPageBegin:
      for i in range(index, tostCount):
        #print(currentTost.text)
        #print(tostOnPage[i])
        if currentTost.text == tostOnPage[i]:
          index = i
          tostIndexes.append(index)
          ++index
          break

    #print( tostIndexes )

    prev = 0
    indexesLength = len(tostIndexes)
    for i in range(0, indexesLength):
      lastIndex = tostIndexes[i+1] if (i+1) != indexesLength else tostCount
      tost = ""
      split4Lines = 1
      for j in range(tostIndexes[i], lastIndex):
        print(split4Lines)
        tost = tost + tostOnPage[j] + ('\n\n' if (split4Lines%4 == 0) else '\n')
        split4Lines = split4Lines + 1

      tosts.append( tost )

    for line in tosts:
      print(line)

    if len(linkNext) > 0:
      urls.append(urls[0] + linkNext[0].split('/')[-1])
      print(urls[-1])
    else:
        break

  return tosts

def readTosts():
  pathName = "./resources/tosts.json"
  tostsId = open(pathName, "w")
  json.dump(parseTosts(), tostsId, ensure_ascii=False, indent=4)

readTosts()