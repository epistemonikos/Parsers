import json
from bs4 import BeautifulSoup

def hindawi_parser(file):
    """
        this function parse and get relevant information from hindawi html pages.
        :params file: html file
    """
    soup = BeautifulSoup(open(file, encoding='utf-8'), 'html.parser')
    resp = {}

    # Extraer nombre
    title = soup.findAll(attrs={'name' : 'dc.title'})
    if title:
        resp["title"] = title[0]['content']

    # Extraer abstract
    resp["abstract"] = get_abstract(soup)

    #Extraer ids
    resp["ids"] = get_identifiers(soup)

    #Extraer publication info
    resp["publication_info"] = get_publication_info(soup)

    # Extraer Autores
    resp["authors"] = get_authors(soup)

    return json.dumps(resp)

def get_publication_info(soup):
    """
        this function get publication information from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = {}
    # Extraer Paginas
    page_ini = soup.findAll(attrs={'name': 'citation_firstpage'})
    page_end = soup.findAll(attrs={'name': 'citation_lastpage'})
    if page_ini:
        resp["page_ini"] = page_ini[0]['content']
    if page_end:
        resp["page_end"] = page_end[0]['content']

    # Extraer Año
    year = soup.findAll(attrs={'name': 'citation_year'})
    if year:
        resp["year"] = year[0]['content']

    # Extraer Volume
    volume = soup.findAll(attrs={'name': 'citation_volume'})
    if volume:
        resp["volume"] = volume[0]['content']

    # Extraer Journal
    journal = soup.findAll(attrs={'name': 'citation_journal_title'})
    if journal:
        resp["journal"] = journal[0]['content']

    # Extraer Publisher
    publisher = soup.findAll(attrs={'name': 'dc.publisher'})
    if publisher:
        resp["publisher"] = publisher[0]['content']

    return resp

def get_identifiers(soup):
    """
        this function get identifiers from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = {}
    # Extraer DOI
    article_doi = soup.findAll(attrs={'name': 'citation_doi'})
    if article_doi:
        resp["doi"] = article_doi[0]['content']

    # Extraer Issue
    issue = soup.findAll(attrs={'name': 'dcterms.issued'})
    if issue:
        resp["issue"] = issue[0]['content']
    # Extraer PubmedID
    pubmedId = soup.findAll(attrs={'name': 'citation_pmid'})
    if pubmedId:
        resp["pubmed"] = pubmedId[0]['content']

    # Extraer ISSN
    issn = soup.findAll(attrs={'name': 'citation_issn'})
    if issn:
        resp["issn"] = issn[0]['content']

    return resp

def get_authors(soup):
    """
        this function get authors from html.
        :params soup: instance of BeautifulSoup class
    """
    resp = []
    authors = soup.findAll(attrs={'name': 'dc.creator'})
    for a in authors:
        resp.append(a['content'].strip())
    return resp

def get_abstract(soup):
    """
        this function get abstract from html.
        :params soup: instance of BeautifulSoup class
    """
    description = soup.findAll(attrs={'name': 'dc.description'})
    return description[0]['content']



print(hindawi_parser("Specificity in Rehabilitation of Word Production_ A Meta-Analysis and a Case Study.xhtml"))