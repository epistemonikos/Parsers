import json
from bs4 import BeautifulSoup
import re


def trim_string(str):
    s = re.sub('\s+', ' ', str)
    return s.strip()


def plos_parser(file):
    soup = BeautifulSoup(open(file, encoding='utf-8'), 'html.parser')
    return {
        'title': get_title(soup),
        'publication_info': get_publication_info(soup),
        'citation': get_citation(soup),
        'ids': get_identifiers(soup),
        'authors': get_authors(soup),
        'abstract': get_abstract(soup),
        'keywords': get_keywords(soup),
#        'references': get_references(soup)
    }


def get_keywords(soup):
    keywords = soup.findAll(attrs={"name": "keywords"})
    if keywords:
        keywords = trim_string(keywords[0]['content']).split(',')
        keywords = [trim_string(r) for r in keywords]
    return keywords


def get_title(soup):
    title = soup.body.find_all('div', 'title-authors')
    if title:
        title = trim_string(title[0].h1.text)
    return title


def get_abstract(soup):
    abstract = soup.body.find_all('div', 'abstract')
    if abstract:
        abstract = trim_string(abstract[0].p.text)
    return abstract


def get_authors(soup):
    authors_info = soup.body.find_all('a', 'author-name')
    authors = []
    for a in authors_info:
        authors.append(re.sub(',$', '', trim_string(a.text)))
    return authors


def get_citation(soup):
    cita = soup.body.find_all('div', 'articleinfo')
    if cita:
        cita = trim_string(cita[0].p.text)
        cita = re.sub('Citation:', '', cita)
    return cita


def get_identifiers(soup):
    return {
        'doi': get_doi(soup),
        'pmid': get_pubmedID(soup),
        'issn': get_issn(soup),
        'url': get_url(soup)
    }


def get_url(soup):
    url = soup.findAll(attrs={"name": "citation_pdf_url"})
    if url:
        url = trim_string(url[0]['content'])
    return url


def get_doi(soup):
    doi = soup.body.find_all('li', id='artDoi')[0]
    if doi:
        doi = re.sub('.*doi.org/', '', trim_string(doi.text))
    return doi


def get_pubmedID(soup):
    return None


def get_issn(soup):
    issn = soup.findAll(attrs={"name": "citation_issn"})
    if issn:
        issn = trim_string(issn[0]['content'])
    return issn


def get_publication_info(soup):
    return {
        'journal': get_journal(soup),
        'year': get_year(soup),
        'volume': get_volume(soup),
        'issue': get_issue(soup),
        'pages': get_pages(soup)
    }


def get_journal(soup):
    journal = soup.body.find_all('h1', 'logo')
    if journal:
        journal = trim_string(journal[0].a.text)
    return journal


def get_year(soup):
    year = soup.findAll(attrs={"name": "citation_date"})
    if year:
        year = trim_string(year[0]['content'])
        year = re.search('\d{4}', year).group(0)
    return year


def get_volume(soup):
    volume = soup.findAll(attrs={"name": "citation_volume"})
    if volume:
        volume = trim_string(volume[0]['content'])
    return volume


def get_issue(soup):
    issue = soup.findAll(attrs={"name": "citation_issue"})
    if issue:
        issue = trim_string(issue[0]['content'])
    return issue


def get_pages(soup):
    page = soup.findAll(attrs={"name": "citation_firstpage"})
    if page:
        page = trim_string(page[0]['content'])
    return page


'''
    #Searching for References
    browser = soup.body.find_all('ol', 'references')[0]
'''

json_data = json.dumps(plos_parser("plos.html"))
print(json_data)
