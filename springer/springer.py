import json
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def springer_parser(file):
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
    title = soup.body.find('h1', 'ArticleTitle')
    if title:
        title = title.text.strip()
    return title


def get_publication_info(soup):
    return {
        'journal': get_journal(soup),
        'year': get_year(soup),
        'volume': get_volume(soup),
        'issue': get_issue(soup),
        'pages': get_pages(soup)
    }


def get_journal(soup):
    journal = soup.body.find('span', 'JournalTitle')
    if journal:
        journal = journal.text.strip()
    return journal


def get_year(soup):
    year = soup.body.find('span', 'ArticleCitation_Year')
    if year:
        year = year.time.text.strip()
    return year


def get_volume(soup):
    volume = soup.body.find('span', 'ArticleCitation_Volume')
    if volume:
        volume = volume.text.strip()
    return volume


def get_issue(soup):
    issue = soup.body.find('span', 'ArticleCitation_Issue')
    if issue:
        issue = issue.text.strip()
    return issue


def get_pages(soup):
    pages = soup.body.find('span', 'ArticleCitation_Pages')
    if pages:   # "pp X-Y"
        pages = pages.text.strip()
        if '–' in pages:
            pages = pages[3:].split('–')       # [ X, Y ]
            return {
                'first': pages[0],
                'last': pages[1]
            }
    return pages


def get_citation(soup):
    cite = soup.body.find(id='citethis-text')
    if cite:
        cite = cite.text.strip()
    return cite


def get_identifiers(soup):
    return {
        'doi': get_doi(soup),
        'pmid': get_pubmedID(soup)
    }


def get_doi(soup):
    article_doi = soup.body.find('p', 'article-doi')
    if article_doi:
        article_doi = article_doi.text[4:].strip()  # c[1][1:]
    return article_doi


def get_pubmedID(soup):
    return None


def get_authors(soup):
    return [ a.text.strip() for a in soup.body.find_all('span', 'authors__name') ]


def get_abstract(soup):
    abstract = soup.body.find('section', 'Abstract')
    if abstract:
        sections = abstract.find_all('div', 'AbstractSection')
        if sections:    # Dividido en secciones (Background, Method, ...)
            abstract = {}
            for s in sections:
                abstract[s.h3.text.strip()] = s.p.text.strip()     # { 'Background': 'bla', ... }
        else:
            abstract = abstract.p.text.strip()
    return abstract


def get_keywords(soup):
    return [ k.text.strip() for k in soup.body.find_all('span', 'Keyword') ]


def get_references(soup):
    return [ get_reference_info(r) for r in soup.body.find_all('div', 'CitationContent') ]


def get_reference_info(ref):
    return {
        'reference': get_ref_text(ref),
        'ids': get_ref_identifiers(ref)
    }


def get_ref_text(ref):
    return ref.contents[0].strip()  # text entrega la cita + ocurrences :/


def get_ref_identifiers(ref):
    return {
        'doi': get_ref_doi(ref),
        'pmid': get_ref_pubmedID(ref)
    }


def get_ref_doi(ref):
    doi = ref.find('span', 'OccurrenceDOI')
    if doi:
        doi = doi.a['href'][18:]  # DOI sin url
    return doi


def get_ref_pubmedID(ref):
    pmid = ref.find('span', 'OccurrencePID')
    if pmid:
        # c["pubmed"] = pubmed.a['href']
        pmid = parse_qs(urlparse(pmid.a['href']).query)['list_uids'][0]
    return pmid
