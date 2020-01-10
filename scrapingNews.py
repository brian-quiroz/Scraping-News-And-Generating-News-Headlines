# importing packages
import numpy as np
import json
import requests
from bs4 import BeautifulSoup
import datetime
import sys

def scrapeNews(keywords, numPages, full):
    articleData = []
    numPages = int(numPages)
    scrape(articleData, keywords, "elcomercio", 2, numPages, full);
    scrape(articleData, keywords, "peru21", 1, numPages, full);
    scrape(articleData, keywords, "publimetro", 1, numPages, full);
    scrape(articleData, keywords, "gestion", 1, numPages, full);
    scrape(articleData, keywords, "depor", 1, numPages, full);
    scrape(articleData, keywords, "trome", 1, numPages, full);

    if (not full):
        filename = keywords.replace(' ', '') + ".txt"
        with open(filename, 'w') as f:
            for i in range(len(articleData)):
                f.write("\"" + articleData[i]["title"].replace("\n","") + "\"\n")
            f.close()
    else:
        articleData.sort(key=lambda x: datetime.datetime.strptime(x["date"], '%d/%m/%Y'), reverse=True)
        return {'name': keywords, 'content': articleData}

def scrape(articleData, keywords, site, ldIndex, numPages, full):

    if (site == "depor"):
        site += ".com"
    else:
        site += ".pe"

    i = 1
    while (i <= numPages):
        r = requests.get('https://' + site + '/buscar/' + keywords.replace(' ', '+') + '/todas/descendiente/' + str(i) + '/?query=' + keywords.replace(' ', '+'))
        coverpage = r.content
        soup = BeautifulSoup(coverpage, 'html5lib')
        coverpage_news = soup.find_all('h2', class_='story-item__content-title')

        if (len(coverpage_news) == 0):
            break

        print("Entrando a página " + str(i) + " de http://" + site)
        number_of_articles = 0
        n_start = len(articleData)

        for title in coverpage_news:
            title_text = title.get_text()
            if ((keywords in title_text) and (title_text not in [a["title"] for a in articleData])):
                newDict = {}
                newDict["title"] = title_text
                newDict["link"] = "http://" + site + title.find('a')['href']
                articleData.append(newDict)
                number_of_articles += 1

        if (full):
            for n in np.arange(n_start, len(articleData)):
                articleReq = requests.get(articleData[n]["link"])
                article_content = articleReq.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
                jsonData = json.loads(soup_article.find_all('script', type='application/ld+json')[ldIndex].text, strict=False)

                description = jsonData["description"]
                articleData[n]["description"] = description

                date = jsonData["datePublished"]
                year = date[0:4]
                month = date[5:7]
                day = date[8:10]
                dateStr = day + "/" + month + "/" + year
                articleData[n]["date"] = dateStr

                diary = jsonData["publisher"]["name"]
                articleData[n]["diary"] = diary

                articleBody = jsonData["articleBody"]
                articleData[n]["body"] = articleBody

        i += 1

def main():
    scrapeNews(sys.argv[1], sys.argv[2], False)

if __name__== "__main__":
  main()
