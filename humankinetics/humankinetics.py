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
    resp["description"] = get_description(soup)

    #Extraer ids
    resp["ids"] = get_identifiers(soup)

    #Extraer publication info
    resp["publication_info"] = get_publication_info(soup)

    # Extraer cita
    cite = soup.body.find(id='citethis-text')
    if cite:
        resp["citation"] = cite.contents[0].strip()

    # Extraer Autores
    resp["authors"] = get_authors(soup)

    # Extraer keywords
    resp["keywords"] = get_keywords(soup)
    # Extraer referencias
    resp["references"] = get_references(soup)

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
        aux = str.index(aux, beg='Pages:', end='doi')
        print(aux)
        resp["pages"] = aux


    # Extraer Volume
    volume = soup.findAll('div', 'citationFormat')
    if volume:
        aux = volume.text.strip()
        aux = str.index(aux, beg='Volume:', end='Pages')
        resp["volume"] = aux

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
    article_doi = soup.findAll({'scheme': 'doi'})
    if article_doi:
        resp["doi"] = article_doi[0]['content']
    return resp

def get_authors(soup):
    """
        this function get authors from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = []
    for a in soup.body.find_all('span', 'AuthorName'):
        resp.append(a.text.strip())
    return resp

def get_description(soup):
    """
        this function get abstract from html.
        :params soup: instance of BeautifulSoup class
    """
    description = soup.findAll('name', 'dc.Description')

    return description[0]['content']

def get_keywords(soup):
    """
        this function get keywords from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = []
    for k in soup.body.find_all('span', 'Keyword'):
        resp.append(k.text.strip())
    return resp

def get_references(soup):
    """
    this function get all references from html.
    :params soup: instance of BeautifulSoup class
    """
    resp = []
    for r in soup.body.find_all('cite', 'CitationContent'):
        c = {}
        c["citation"] = r.contents[0].strip()
        doi = r.find('span', 'OccurrenceDOI')
        if doi:
            c["doi"] = doi.a['href'][18:]
        pubmed = r.find('span', 'OccurrencePID')
        if pubmed:
            c["pubmed"] = pubmed.a['href']
        scholar = r.find('span', 'OccurrenceGS')
        if scholar:
            c["scholar"] = scholar.a["href"]
        resp.append(c)
    return resp

print(humankinetics_parser("Postoperative Rehabilitation after Hip Resurfacing_ A Systematic Review_ Journal of Sport Rehabilitation_ Vol 25, No 2.html" ))