from bs4 import BeautifulSoup
import json
import re

#Funcion que limpia texto
def trim_string(str):
   s = re.sub('\s+', ' ', str)
   return s.strip()


def parser(file):
    #objeto que contiene el html
    soup = BeautifulSoup(open(file, encoding = 'utf-8'), 'html.parser')
    #variable que contiene el json final
    resp = {}

    # extraer titulo
    title = soup.body.find(id='scm6MainContent_lblArticleTitle').get_text()
    resp['title'] = trim_string(title)

    #Extraer publication info
    resp['publication_info'] = get_publication_info(soup)

    # extraer referencias
    resp['references'] = get_references(soup)

    # extraer abstract
    resp['abstract'] = get_abstract(soup)

    #extraer identificadores
    resp['ids'] = get_identifiers(soup)

    #extraer autores
    authors = soup.body.find_all('span', 'authorNames')[0].get_text()
    resp['authors'] = authors.split(';')

    #generar Json
    return json.dumps(resp)


def get_abstract(soup):
    resp={}
    abstract = soup.body.find_all('span', 'Abstract 0')[0].find_all('p')
    if len(abstract) > 1:
        c = {}
        for sec in abstract:
            c[sec.strong.get_text()] = sec.span.get_text()
        resp = c
    else:
        resp = abstract.get_text()
    return resp

def get_identifiers(soup):
    resp={}
    # extraer doi
    doi = soup.body.find(id="scm6MainContent_lblClientName").get_text().strip()
    resp['doi'] = doi[doi.index("doi:") + 4:len(doi) - 1]
    return resp
def get_references(soup):
    resp = []
    references = soup.body.find_all('div', 'refContent')
    for r in references:
        c = {}
        c['text'] = trim_string(r.contents[0])
        pubmed = r.find('span', 'pubmedLink')
        if pubmed:
            c['pubmed'] = pubmed.a['href']
        crossrefdoi = r.find('span', 'crossrefDoi')
        if crossrefdoi:
            c['crossrefdoi'] = crossrefdoi.a['href']
        link = r.a
        if link and not pubmed and not crossrefdoi:
            c['link'] = link['href']
        resp.append(c)
    return resp

def get_publication_info(soup):
    resp = {}
    # extraer ano y mes
    resp['year'] = soup.body.find('span', 'year').get_text().strip()
    resp['month'] = soup.body.find('span', 'month').get_text().strip()

    return resp


print(parser('jamanetwork.html'))


