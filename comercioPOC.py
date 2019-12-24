# importing packages
from globals import months
import numpy as np
import json
import requests
from bs4 import BeautifulSoup

def poc(person):
    articleData = []
    scrape(person, "elcomercio", 2, articleData);
    scrape(person, "peru21", 1, articleData);
    scrape(person, "publimetro", 1, articleData);
    scrape(person, "gestion", 1, articleData);
    scrape(person, "depor", 1, articleData);
    scrape(person, "trome", 1, articleData);

    return articleData;

def scrape(person, site, ld_index, articleData):

    if (site == "depor"):
        site += ".com"
    else:
        site += ".pe"

    first_name = person.split()[0]
    last_name = person.split()[1]

    i = 1
    while (i <= 1):
        r = requests.get('https://' + site + '/buscar/' + first_name + '+' + last_name + '/todas/descendiente/' + str(i) + '/?query=' + first_name + '+' + last_name)
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
            if ((first_name + " " + last_name) in title_text):
                newDict = {}
                newDict["title"] = title_text
                newDict["link"] = "http://" + site + title.find('a')['href']
                articleData.append(newDict)
                number_of_articles += 1

        for n in np.arange(n_start, len(articleData)):
            articleReq = requests.get(articleData[n]["link"])
            article_content = articleReq.content
            soup_article = BeautifulSoup(article_content, 'html5lib')
            jsonData = json.loads(soup_article.find_all('script', type='application/ld+json')[ld_index].text, strict=False)

            description = jsonData["description"]
            articleData[n]["description"] = description

            date = jsonData["datePublished"]
            year = date[0:4]
            month = months.get(date[5:7])
            day = date[8:10]
            dateFinal = day + " de " + month + " de " + year
            articleData[n]["date"] = dateFinal

            diary = jsonData["publisher"]["name"]
            articleData[n]["diary"] = diary

            articleBody = jsonData["articleBody"]
            articleData[n]["body"] = articleBody

        n_prev = n + 1

        i += 1

    # for i in range(len(articleData)):
    #     print(articleData[i]["title"])

# poc("cena navideña")
