from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def biomed_parser(file):
    """
        this function parse and get relevant information from biomedcentral html pages.
        :params file: html file
    """
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
    """
        this function get publication information from html.
        :params soup: instance of BeautifulSoup class
    """
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
        year = year.text.strip()
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
    if pages:  # "pp X-Y"
        pages = pages.text.strip()
        if '–' in pages:
            pages = pages[3:].split('–')  # [ X, Y ]
            return {
                'first': pages[0],
                'last': pages[1]
            }
    return pages


def get_citation(soup):
    return None


def get_identifiers(soup):
    """
        this function get identifiers from html.
        :params soup: instance of BeautifulSoup class
    """
    return {
        'doi': get_doi(soup),
        'pmid': get_pubmedID(soup)
    }


def get_doi(soup):
    article_doi = soup.body.find('p', 'ArticleDOI')
    if article_doi:
        article_doi = article_doi.text[4:].strip()
    return article_doi


def get_pubmedID(soup):
    return None


def get_authors(soup):
    """
        this function get authors from html.
        :params soup: instance of BeautifulSoup class
    """
    return [ a.text.strip() for a in soup.body.find_all('span', 'AuthorName') ]


def get_abstract(soup):
    """
        this function get abstract from html.
        :params soup: instance of BeautifulSoup class
    """
    abstract = soup.body.find('section', 'Abstract')
    if abstract:
        sections = abstract.find_all('div', 'AbstractSection')
        if sections:
            abstract = {}
            for s in sections:
                if s.h3:
                    abstract[s.h3.text.strip()] = s.p.text.strip()
        else:
            abstract = abstract.p.text.strip()
    return abstract


def get_keywords(soup):
    """
        this function get keywords from html.
        :params soup: instance of BeautifulSoup class
    """
    return [ k.text.strip() for k in soup.body.find_all('span', 'Keyword') ]


def get_references(soup):
    """
    this function get all references from html.
    :params soup: instance of BeautifulSoup class
    """
    return [ get_reference_info(r) for r in soup.body.find_all('cite', 'CitationContent') ]


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
    return []


def get_ref_year(ref):
    return None


def get_ref_title(ref):
    return None


def get_ref_journal(ref):
    return None


def get_ref_volume(ref):
    return None


def get_ref_pages(ref):
    return None


def get_ref_text(ref):
    if ref.contents:
        return ref.contents[0].strip()
    return None


def get_ref_identifiers(ref):
    return {
        'doi': get_ref_doi(ref),
        'pmid': get_ref_pubmedID(ref),
        'scholar': get_ref_scholar(ref)
    }


def get_ref_doi(ref):
    doi = ref.find('span', 'OccurrenceDOI')
    if doi:
        doi = doi.a['href'][18:]
    return doi


def get_ref_pubmedID(ref):
    pubmed = ref.find('span', 'OccurrencePID')
    if pubmed:
        pmid = parse_qs(urlparse(pubmed.a['href']).query)['list_uids'][0]
    return pubmed


def get_ref_scholar(ref):
    scholar = ref.find('span', 'OccurrenceGS')
    if scholar:
        scholar = scholar.a["href"]
    return scholar