from bs4 import BeautifulSoup
import json
import re

#Funcion que limpia texto
def trim_string(str):
   s = re.sub('\s+', ' ', str)
   return s.strip()


def parser():
    #objeto que contiene todo el html
    soup = BeautifulSoup(open('jamanetwork.html'), 'html.parser')
    #variable que contiene el json final
    resp = {}
    #extraer ano y mes
    c= {}
    c['year']= soup.body.find('span','year').get_text().strip()
    c['month'] = soup.body.find('span','month').get_text().strip()
    resp['date'] = c
    #extraer doi
    doi = soup.body.find(id="scm6MainContent_lblClientName").get_text().strip()
    resp['doi'] = doi[doi.index("doi:")+4:len(doi)-1]
    #extraer abstract
    abstract = soup.body.find_all('span', 'Abstract 0')[0].find_all('p')
    if len(abstract) > 1 :
        c = {}
        for sec in abstract:
            c[sec.strong.get_text()] = sec.span.get_text()
        resp['abstract'] = c
    else:
        resp['abstract'] = abstract.get_text()
    #extraer titulo
    title = soup.body.find(id='scm6MainContent_lblArticleTitle').get_text()
    resp['title'] = trim_string(title)

    #extraer autores
    authors = soup.body.find_all('span', 'authorNames')[0].get_text()
    resp['authors'] = authors.split(';')
    #extraer referencias
    references = soup.body.find_all('div', 'refContent')
    resp['references'] = []
    for r in references:
        c= {}
        c['text'] = trim_string(r.contents[0])
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
    #generar Json
    json_data = json.dumps(resp)
    #debug Json
    print json_data
parser()


