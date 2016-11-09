__author__ = 'fmosso'
from bs4 import BeautifulSoup
import json
import re

STANDARDJSON= {"references" : None,"keywords":None ,'cited_articules' : None ,"language": None, "authors":None, "abstract": None, "ids": {"embase": None, "doi": None, "pubmed": None}, "title":None, "publication_type": {"issue": None, "pagination": None, "cited_medium": None, "year": None, "title": None, "volume": None, "ISSN": None, "type": None}}


def parser():
    soup = BeautifulSoup(open('sciencedirect.html'), 'html.parser')
    resp = STANDARDJSON

    # get the authors
    def addAuthors(author):
         c= {}
         c = author
         resp['authors'].append(c)
    if soup.body.find('ul', 'authorGroup noCollab svAuthor'):
        resp['authors'] = []
        for author in soup.body.find('ul', 'authorGroup noCollab svAuthor').find_all('li'):
         addAuthors(author.a['data-fn']+" "+author.a['data-ln'])
    elif  soup.body.find('div', 'article-author-list'):
        resp['authors'] = []
        for author in soup.body.find('div', 'article-author-list').find_all('span','author-name'):
            addAuthors(author.a.get_text()[1:])
    # get the abstract
    abstract = soup.body.find('div','abstract svAbstract ')
    c={}
    if abstract:
        for titles, texts in zip(abstract.find_all('h4'), abstract.find_all('p')):
            c[titles.get_text()] = texts.get_text()
        resp['abstract'] = c
    # get the doi
    if soup.body.find('dd','doi'):
        resp['ids']['doi'] = soup.body.find('dd','doi').get_text()
    elif soup.body.find('p','article-doi'):
        resp['ids']['doi'] = soup.body.find('p','article-doi').a['href']
    #get journal
    if soup.body.find('div','publicationHead'):
        resp['publication_type']['title'] = soup.body.find('div','publicationHead').find('span').get_text()
    elif soup.body.find('p','journal-title'):
        resp['publication_type']['title'] = soup.body.find('p','journal-title').a.get_text()
    #get keyword
    if soup.body.find('ul','keyword'):
      k =[]
      for keywords in soup.body.find('ul','keyword').find_all('li'):
          k.append(keywords.find('span').get_text())
      resp['keywords'] = k
    #get name
    if soup.body.find('h1','svTitle'):
        resp['title'] = soup.body.find('h1','svTitle').get_text()
    elif soup.body.find('h1','article-title'):
        resp['title'] = soup.body.find('h1','article-title').get_text()
    #get reference
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
    if r:
        resp['references'] = r
    #get the volume

    if soup.body.find('p','volIssue'):
        volume = soup.body.find('p','volIssue')
    elif soup.body.find('p','journal-volume'):
        volume = soup.body.find('p','journal-volume')
    print (volume)
    if volume:
        #get volume
        resp['publication_type']['volume'] = volume.a.get_text().split(',')[0]
        #get issue
        resp['publication_type']['issue'] = volume.a.get_text().split(',')[1]
        #get pagination
        resp['publication_type']['pagination'] =  volume.contents[1].split(',')[2]
        #get date
        resp['publication_type']['year'] = re.search(r', (.*),', volume.contents[1]).group(1)


    #get cited articules
    listcitedarticules = soup.body.find('ol',{'id':'citedByList'})
    if listcitedarticules:
        ca = []
        for articules in listcitedarticules.find_all('ol', 'articles'):
            citedarticules = {}
            citedarticules['name'] = articules.find('li', 'artTitle').a['title']
            citedarticules['ref'] = articules.find('li', 'artTitle').a['href']
            citedarticules['source'] = articules.find('li', 'srcTitle').get_text()
            ca.append(citedarticules)
        resp['cited_articules'] = ca
    json_data = json.dumps(resp)
    print (json_data)
parser()