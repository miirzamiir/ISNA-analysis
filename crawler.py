import json
import requests
import khayyam 
from bs4 import BeautifulSoup

BASE_URL = 'https://www.isna.ir'
date = str(khayyam.JalaliDate.today()).split('-')

title = []
link = []
abstract = []
news = []
lis = []
ps = []

"""
ISNA sorts news by their release time and the date should be declared in the url. This script is written in the way that
every time it runs, we get the news of that day and days before; but the data in data.json file is static. 
"""
for i in range(1, 20):
    url = f'https://www.isna.ir/archive?pi={i}&ms=0&dy={date[2]}&mn={date[1]}&yr={date[0]}'
    res = requests.get(url=url)    
    soup = BeautifulSoup(res.text, 'html.parser')

    divs = soup.find_all('div', attrs={'class': 'desc'})
    for div in divs:
      lis.append(div.findChildren('a', recursive=True)[0])
      ps.append(div.findChildren('p', recursive=True))

link = [BASE_URL+li.get('href') for li in lis]
title = [li.getText() for li in lis]
for p in ps:
  try:
    abstract.append(p[0].getText())
  except:
    abstract.append('')

for l, t, a in zip(link, title, abstract):
    paragraphs = []
    tag = []
    res = requests.get(url=l)    
    soup = BeautifulSoup(res.text, 'html.parser')
    div = soup.find('div', attrs={'class': 'item-text'})
    tags = soup.findAll('a', attrs={'rel': 'Tag'})
    try:
        ps = div.findChildren('p', recursive=False)
    except:
        continue
    for p in ps: 
        paragraphs.append(p.getText())
    for tg in tags:
        tag.append(tg.getText())
    news.append({'title': t, 'link': l, 'abstract': a, 'paragraphs': paragraphs, 'tag': tag})

with open('data2.json', 'w+', encoding='utf-8') as file:
    json.dump(news, file)