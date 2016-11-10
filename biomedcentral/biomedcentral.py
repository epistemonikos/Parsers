import json
from bs4 import BeautifulSoup

def biomed_parser(file):
    """
        this function parse and get relevant information from biomedcentral html pages.
        :params file: html file
    """
    soup = BeautifulSoup(open(file, encoding='utf-8'), 'html.parser')
    resp = {}

    # Extraer nombre
    title = soup.findAll(attrs={'name': 'citation_title'})
    if title:
        resp["title"] = title[0]['content']

    # Extraer Abstract
    resp["abstract"] = get_abstract(soup)

    #Extraer ids
    resp["ids"] = get_identifiers(soup)

    #Extraer publication info
    resp["publication_info"] = get_publication_info(soup)


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
    pages = soup.body.find('span', 'ArticleCitation_Pages')
    if pages:
        resp["pages"] = pages.contents[0].strip()

    # Extraer Año
    year = soup.body.find('span', 'ArticleCitation_Year')
    if year:
        resp["year"] = year.text.strip()

    # Extraer Volume
    volume = soup.body.find('span', 'ArticleCitation_Volume')
    if volume:
        resp["volume"] = volume.text.strip()  # tiene <strong> entremedio :C

    # Extraer Journal
    journal = soup.body.find('span', 'JournalTitle')
    if journal:
        resp["journal"] = journal.text.strip()


    return resp

def get_identifiers(soup):
    """
        this function get identifiers from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = {}
    # Extraer DOI
    article_doi = soup.body.find('p', 'ArticleDOI')
    if article_doi:
        resp["doi"] = article_doi.text[4:].strip()
    # Extraer Issue
    issue = soup.body.find('span', 'ArticleCitation_Issue')
    if issue:
        resp["issue"] = issue.text.strip()

    return resp


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

def get_abstract(soup):
    """
        this function get abstract from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = []
    abstract = soup.body.find('section', 'Abstract')
    sections = abstract.find_all('div', 'AbstractSection')
    if sections:
        a = {}
        for s in sections:
            a[s.h3.text.strip()] = s.p.text.strip()
        resp = a
    else:
        resp = abstract.p.text.strip()
    return resp

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

print(biomed_parser("biomedcentral.html"))