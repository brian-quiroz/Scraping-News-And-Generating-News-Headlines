# importing packages
import numpy as np
import json
import requests
from bs4 import BeautifulSoup

def poc(person):
    class article:
        __title = ""
        __link = ""
        __description = ""
        __date = ""
        __diary = ""
        __body = ""

    dataDict = {"Titles": [], "Links": [], "Descriptions": [], "Dates": [], "Diaries": [], "ArticleBodies": []}

    months = {"01": "enero", "02": "febrero", "03": "marzo", "04": "abril", "05": "mayo", "06": "junio", "07": "juio", "08": "agosto", "09": "setiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"}

    scrape(person, "elcomercio", 2, dataDict, months);
    scrape(person, "peru21", 1, dataDict, months);
    scrape(person, "publimetro", 1, dataDict, months);
    scrape(person, "gestion", 1, dataDict, months);
    scrape(person, "depor", 1, dataDict, months);
    scrape(person, "trome", 1, dataDict, months);

    return dataDict;

def scrape(person, site, ld_index, dataDict, months):
    if (site == "depor"):
        site += ".com"
    else:
        site += ".pe"

    first_name = person.split()[0];
    last_name = person.split()[1];

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
        n_start = len(dataDict["Titles"])

        for title in coverpage_news:
            title_text = title.get_text()
            if ((first_name + " " + last_name) in title_text):
                dataDict["Titles"].append(title_text)
                dataDict["Links"].append("http://" + site + title.find('a')['href'])
                number_of_articles += 1

        for n in np.arange(n_start, len(dataDict["Titles"])):
            article = requests.get(dataDict["Links"][n])
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')
            jsonData = json.loads(soup_article.find_all('script', type='application/ld+json')[ld_index].text, strict=False)

            description = jsonData["description"]
            dataDict["Descriptions"].append(description)

            date = jsonData["datePublished"]
            year = date[0:4]
            month = months.get(date[5:7])
            day = date[8:10]
            dateFinal = day + " de " + month + " de " + year
            dataDict["Dates"].append(dateFinal)

            diary = jsonData["publisher"]["name"]
            dataDict["Diaries"].append(diary)

            articleBody = jsonData["articleBody"]
            dataDict["ArticleBodies"].append(articleBody)

        n_prev = n + 1

        i += 1

    # for key, val in dataDict.items():
    #     for n in reversed(np.arange(0, len(val))):
    #         print(str(n) + ": " + val[n])

# poc("cena navideña")
