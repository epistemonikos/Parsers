__author__ = 'fmosso'
from bs4 import BeautifulSoup
import json
import re


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
    resp['abstract'] = {}
    abstract = soup.body.find('div','abstract svAbstract ')
    c={}
    if abstract:
        for titles, texts in zip(abstract.find_all('h4'), abstract.find_all('p')):
            c[titles.get_text()] = texts.get_text()
        resp['abstract'] = c
    # get the doi
    resp['doi'] = soup.body.find('dd','doi').get_text()
    #get journal
    resp['journal'] = soup.body.find('div','publicationHead').find('span').get_text()
    #get keyword
    k =[]
    for keywords in soup.body.find('ul','keyword').find_all('li'):
        k.append(keywords.find('span').get_text())
    resp['keywords'] = k
    #get name
    resp['name'] = soup.body.find('h1','svTitle').get_text()
    #get reference
    resp['references'] = []
    r =[]
    for groupofreferences in soup.body.find_all('ol','references'):
        for references in groupofreferences.find_all('ul', 'reference'):
            ref ={}
            #get doi if they have
            doi = references.find('li','source')
            if doi and doi.find('a'):
                ref['doi'] = doi.find('a').get_text()
            #try to get doi from external link
            else:
                for external_link in references.find('li','external refPlaceHolder').find_all('div'):
                   if external_link.get_text() == 'CrossRef':
                        ref['doi'] = external_link.a['href']
            #get name
            if references.find('li','title'):
                 ref['name'] = references.find('li','title').p.get_text()
            #get authors
            if references.find('li','author') :
                ref['authors'] = references.find('li','author').get_text()
            #get link to science direct
            if references.find('li','referenceLabel') and references.find('li','referenceLabel').a:
                ref['science direct'] = references.find('li','referenceLabel').a['href']
            #get source from reference
            if references.find('li','source') and references.find('li','source').p:
                ref['source'] = references.find('li','source').p.contents[0]
            r.append(ref)
    resp['references'] = r
    #get the volume
    volume = soup.body.find('p','volIssue')
    resp['volume'] = volume.a.get_text()
    #get date
    resp['date'] = re.search(r', (.*),', volume.contents[1]).group(1)
    #get cited articules
    listcitedarticules = soup.body.find('ol',{'id':'citedByList'})
    ca = []
    if listcitedarticules:
        for articules in listcitedarticules.find_all('ol', 'articles'):
            citedarticules = {}
            citedarticules['name'] = articules.find('li', 'artTitle').a['title']
            citedarticules['ref'] = articules.find('li', 'artTitle').a['href']
            citedarticules['source'] = articules.find('li', 'srcTitle').get_text()
            ca.append(citedarticules)
    resp['cited articules'] = ca
    json_data = json.dumps(resp)
    print (json_data)
parser()