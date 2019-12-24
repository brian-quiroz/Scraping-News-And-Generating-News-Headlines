# importing packages
import numpy as np
import requests
from bs4 import BeautifulSoup

r1 = requests.get('https://elpais.com/elpais/inenglish.html')
coverpage = r1.content

soup1 = BeautifulSoup(coverpage, 'html5lib')

coverpage_news = soup1.find_all('h2', class_='articulo-titulo')

#print(coverpage_news[4].get_text())
#print(coverpage_news[4].find('a')['href'])

# Scraping the first 5 articles
number_of_articles = 5

# Empty lists for content, links, and titles
news_contents = []
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):
  if "inenglish" not in coverpage_news[n].find('a')['href']:
    continue

  link = coverpage_news[n].find('a')['href']
  list_links.append(link)

  title = coverpage_news[n].find('a').get_text()
  list_titles.append(title)

  article = requests.get(link)
  article_content = article.content
  soup_article = BeautifulSoup(article_content, 'html5lib')
  body = soup_article.find_all('script', class_='articulo-cuerpo')
  x = body[0].find_all('p')

  list_paragraphs = []
  for p in np.arange(0, len(x)):
    paragraph = x[p].get_text()
    list_paragraphs.append(paragraph)
    final_article = " ".join(list_paragraphs)

  news_contents.append(final_article)

for news in news_contents:
  print(news)
