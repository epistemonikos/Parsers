__author__ = 'fmosso'
from bs4 import BeautifulSoup
import json


def parser():
    soup = BeautifulSoup(open('sciencedirect.html'), 'html.parser')
    resp = {}

    # get the authors
    authors = soup.body.find('ul', 'authorGroup noCollab svAuthor')
    resp['authors'] = []
    for author in authors.find_all('li'):
        c= {}
        c = author.a['data-fn']+" "+author.a['data-ln']
        resp['authors'].append(c)
    references = soup.body.find_all('div', 'refContent')
    citations = []

    # get the abstract
    abstract = soup.body.find('div','abstract svAbstract ')
    resp['abstract'] = {}
    c={}
    for titles, texts in zip(abstract.find_all('h4'), abstract.find_all('p')):
        c[titles.get_text()] = texts.get_text()
    resp['abstract'] = c
    # get the doi
    resp['doi'] = soup.body.find('dd','doi').get_text()
    #get journal
    resp['journal'] = soup.body.find('div','publicationHead').find('span').get_text()


    resp['references'] = []
    for r in references:
        c= {}
        c['text'] = r.contents[0].strip()
        pubmed = r.find('span', 'pubmedLink')
        if pubmed:
            c['pubmed'] = pubmed.a['href']
        crossrefdoi = r.find('span', 'crossrefDoi')
        if crossrefdoi:
            c['crossrefdoi'] = crossrefdoi.a['href']
        link = r.a
        if link and not pubmed and  not crossrefdoi:
            c['link'] = link['href']
        resp['references'].append(c)
    json_data = json.dumps(resp)
    print (json_data)
parser()