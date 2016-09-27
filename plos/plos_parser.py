#import json
from bs4 import BeautifulSoup
import re

def trim_string(str):
    s = re.sub('\s+', ' ', str)
    return s.strip()

def plos_parser():
    resp = {}
    soup = BeautifulSoup(open('plos.html', encoding="utf8"), 'html.parser')

    ##Searching for Abstract
    browser = soup.body.find_all('div', 'abstract')
    abstract = browser[0].p.text
    resp['abstract'] = trim_string(abstract)

    #Searching for Article info
    browser = soup.body.find_all('div', 'articleinfo')
    cita = trim_string(browser[0].p.text)
    cita = re.sub('Citation:', '', cita)
    resp['citation'] = cita


    #Searching for Title
    browser = soup.body.find_all('div', 'title-authors')
    title = trim_string(browser[0].h1.text)
    resp['title'] = title

    #Searching for Authors
    browser = soup.body.find_all('a', 'author-name')
    authors = []
    for node in browser:
        authors.append(re.sub(',$', '', trim_string(node.text)))
    resp['authors'] = authors

    #Searching DOI
    browser = soup.body.find_all('li', id='artDoi')[0]
    doi = re.sub('.*doi.org/', '', trim_string(browser.text))
    resp['doi'] = doi

    #Searching for Publish date
    browser = soup.body.find_all('li', id='artPubDate')[0]
    published = []
    published.append(trim_string(re.sub('Published:', '', browser.text)))


#     json_data = json.dumps(resp)
#     print(json_data)
plos_parser()