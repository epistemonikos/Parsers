import json
from bs4 import BeautifulSoup

def humankinetics_parser(file):
    """
        this function parse and get relevant information from biomedcentral html pages.
        :params file: html file
    """
    soup = BeautifulSoup(open(file, encoding='utf-8'), 'html.parser')
    resp = {}

    # Extraer nombre
    title = soup.findAll(attrs={'name' : 'dc.Title'})
    if title:
        resp["title"] = title[0]['content']

    # Extraer Description
    resp["abstract"] = get_abstract(soup)

    #Extraer ids
    resp["ids"] = get_identifiers(soup)

    #Extraer publication info
    resp["publication_info"] = get_publication_info(soup)

    # Extraer Autores
    resp["authors"] = get_authors(soup)

    # Extraer keywords
    resp["keywords"] = get_keywords(soup)


    return json.dumps(resp)

def get_publication_info(soup):
    """
        this function get publication information from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = {}
    # Extraer Paginas
    pages = soup.body.find('div', 'citationFormat')
    if pages:
        aux = pages.text.strip()
        ini = aux.index('Pages:')
        end = aux.index('doi:')
        resp["pages"] = aux[(ini+7):end]

    # Extraer Volume
    volume = soup.find('div', 'citationFormat')
    if volume:
        aux = volume.text.strip()
        ini = aux.index('Volume:')
        end = aux.index('Issue:')
        resp["volume"] = aux[(ini+7):end]

    # Extraer Journal
    journal = soup.findAll(attrs={'name' : 'citation_journal_title'})

    if journal:
        resp["journal"] = journal[0]['content']


    return resp

def get_identifiers(soup):
    """
        this function get identifiers from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = {}
    # Extraer DOI
    article_doi = soup.findAll(attrs={'scheme': 'doi'})
    if article_doi:
        resp["doi"] = article_doi[0]['content']
    return resp

def get_authors(soup):
    """
        this function get authors from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = []
    authors = soup.findAll(attrs={'name': 'dc.Creator'})
    for a in authors:
        resp.append(a['content'].strip())
    return resp

def get_abstract(soup):
    """
        this function get abstract from html.
        :params soup: instance of BeautifulSoup class
    """
    description = soup.findAll(attrs={'name': 'dc.Description'})
    return description[0]['content']

def get_keywords(soup):
    """
        this function get keywords from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = []
    keywords = soup.findAll(attrs={'name': 'keywords'})[0]['content']
    keys = keywords.split(',')
    for k in keys:
        resp.append(k.strip())
    return resp


print(humankinetics_parser("Postoperative Rehabilitation after Hip Resurfacing_ A Systematic Review_ Journal of Sport Rehabilitation_ Vol 25, No 2.html" ))