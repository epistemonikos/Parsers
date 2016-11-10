import json
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup


def wiley_parser(file):
    soup = BeautifulSoup(open(file, encoding='utf-8'), 'html.parser')
    return {
        'title': get_title(soup),
        'publication_info': get_publication_info(soup),
        'citation': get_citation(soup),
        'ids': get_identifiers(soup),
        'authors': get_authors(soup),
        'abstract': get_abstract(soup),
        'keywords': get_keywords(soup),
        'references': get_references(soup)
    }


def get_title(soup):
    title = soup.body.find('h1', 'article-header__title')
    if title:
        title = title.text.strip()
    return title


PUBLICATION_INFO = None


def get_publication_info(soup):
    return {
        'journal': get_journal(soup),
        'year': get_year(soup),
        'volume': get_volume(soup),
        'issue': get_issue(soup),
        'pages': get_pages(soup)
    }


def get_journal(soup):
    journal = soup.body.find('strong', 'journal-header__name-title')
    if journal:
        journal = journal.text.strip()
    return journal


def load_publication_info(soup):
    global PUBLICATION_INFO
    PUBLICATION_INFO = [x.strip() for x in
                        soup.body.find('p', 'issue-header__description').text.strip().split('\n')[1:]]


def get_year(soup):
    if not PUBLICATION_INFO:
        load_publication_info(soup)
    return PUBLICATION_INFO[1][-4:]


def get_volume(soup):
    if not PUBLICATION_INFO:
        load_publication_info(soup)
    return PUBLICATION_INFO[0].split(',')[0][6:].strip()


def get_issue(soup):
    if not PUBLICATION_INFO:
        load_publication_info(soup)
    return PUBLICATION_INFO[0].split(',')[1].strip()[5:].strip()


def get_pages(soup):
    if not PUBLICATION_INFO:
        load_publication_info(soup)
    pages = PUBLICATION_INFO[2][5:].strip().split('–')
    return {
        'first': pages[0],
        'last': pages[1]
    }


def get_citation(soup):
    cite = soup.body.find(id='citethis-text')
    if cite:
        cite = cite.text.strip()
    return cite


def get_identifiers(soup):
    # <li class="article-header__meta-info-item">
    return {
        'doi': get_doi(soup),
        'pmid': get_pubmedID(soup)
    }


def get_doi(soup):
    doi = soup.body.find('span', 'article-info__section-doi-data')
    if doi:
        doi = doi.text.strip()  # c[1][1:]
    return doi


def get_pubmedID(soup):
    return None


def get_authors(soup):
    #<div class="article-header__authors-container">
    return [ a.text.strip() for a in soup.body.find_all('span', 'authors__name') ]


def get_abstract(soup):
    abstract = soup.body.find('section', id='abstract')
    if abstract:
        sections = abstract.find_all('section')
        if sections:    # Dividido en secciones (Background, Method, ...)
            abstract = {}
            for s in sections[1:]:
                if s.h3:
                    abstract[s.h3.text.strip()] = s.p.text.strip()     # { 'Background': 'bla', ... }
        else:
            abstract = abstract.p.text.strip()
    return abstract


def get_keywords(soup):
    return [ (lambda k: k[:-1] if k[-1:] == ';' else k)(k.text.strip())
             for k in soup.body.find_all('li', 'article-info__keywords-item') ]


def get_references(soup):
    return [ get_reference_info(r)
             for r in soup.body.find('ul', 'article-section__references-list').children
             if r != '\n']


def get_reference_info(ref):
    return {
        'authors': get_ref_authors(ref),
        'year': get_ref_year(ref),
        'title': get_ref_title(ref),
        'journal': get_ref_journal(ref),
        'volume': get_ref_volume(ref),
        'pages': get_ref_pages(ref),
        'reference': get_ref_text(ref),
        'ids': get_ref_identifiers(ref)
    }


def get_ref_authors(ref):
    return [ a.text.strip() for a in ref.find_all('span', 'author')]


def get_ref_year(ref):
    year = ref.find('span', 'pubYear')
    if year:
        year = year.text.strip()
    return year


def get_ref_title(ref):
    title = ref.find('span', 'articleTitle')
    if title:
        title = title.text.strip()
    return title


def get_ref_journal(ref):
    journal = ref.find('span', 'journalTitle')
    if journal:
        journal = journal.text.strip()
    return journal


def get_ref_volume(ref):
    volume = ref.find('span', 'vol')
    if volume:
        volume = volume.text.strip()
    return volume


def get_ref_pages(ref):
    first = ref.find('span', 'pageFirst')
    last = ref.find('span', 'pageLast')
    return {
        'first': first.text.strip() if first else None,
        'last': last.text.strip() if last else None
    }


def get_ref_text(ref):
    return None


def get_ref_identifiers(ref):
    return {
        'doi': get_ref_doi(ref),
        'pmid': get_ref_pubmedID(ref)
    }


def get_ref_doi(ref):
    ref_info = ref.find('ul', 'article-section__references-list-additional u-horizontal-list')
    doi = None
    if ref_info:
        doi = ref_info.get('data-doi')
        for link in ref_info.find_all('a'):
            if 'doi.org' in link['href']:
                doi = link['href'][link['href'].rfind('doi.org') + 8:]
                break
    return doi


def get_ref_pubmedID(ref):
    ref_info = ref.find('ul', 'article-section__references-list-additional u-horizontal-list')
    pmid = None
    if ref_info:
        for link in ref_info.find_all('a'):
            if 'pubmed' in link['href']:
                pmid = link['href'][link['href'].rfind('/') + 1:]
                break
    return pmid
