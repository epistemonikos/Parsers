import json
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def springer_parser(file):
    soup = BeautifulSoup(open(file, encoding='utf-8'), 'html.parser')
    resp = {}

    # Extraer nombre
    name = soup.body.find('h1', 'ArticleTitle')
    if name:
        resp["name"] = name.text.strip()

    # Extraer Journal
    journal = soup.body.find('span', 'JournalTitle')
    if journal:
        resp["journal"] = journal.text.strip()

    # Extraer Año
    year = soup.body.find('span', 'ArticleCitation_Year')
    if year:
        resp["date"] = year.time.text.strip()

    # Extraer Volume
    volume = soup.body.find('span', 'ArticleCitation_Volume')
    if volume:
        resp["volume"] = volume.text.strip()

    # Extraer Issue
    issue = soup.body.find('span', 'ArticleCitation_Issue')
    if issue:
        resp["issue"] = issue.text.strip()

    # Extraer Paginas
    pages = soup.body.find('span', 'ArticleCitation_Pages')
    if pages:
        resp["pages"] = pages.text.strip()

    # Extraer cita
    cite = soup.body.find(id='citethis-text')
    if cite:
        resp["citation"] = cite.text.strip()

    # Extraer DOI
    article_doi = soup.body.find('p', 'article-doi')
    if article_doi:
        resp["doi"] = article_doi.text[4:].strip() #c[1][1:]

    # Extraer Autores
    resp["authors"] = []
    for a in soup.body.find_all('span', 'authors__name'):
        resp["authors"].append(a.text.strip())

    # Extraer Abstract
    abstract = soup.body.find('section', 'Abstract')
    sections = abstract.find_all('div', 'AbstractSection')
    if sections:
        a = {}
        for s in sections:
            a[s.h3.text.strip()] = s.p.text.strip()
        resp["abstract"] = a
    else:
        resp["abstract"] = abstract.p.text.strip()

    # Extraer keywords
    resp["keywords"] = []
    for k in soup.body.find_all('span', 'Keyword'):
        resp["keywords"].append(k.text.strip())

    # Extraer referencias
    resp["references"] = []
    for r in soup.body.find_all('div', 'CitationContent'):
        c = {}
        c["citation"] = r.contents[0].strip()       # text entrega la cita + ocurrences :/
        doi = r.find('span', 'OccurrenceDOI')
        if doi:
            c["doi"] = doi.a['href'][18:]           # DOI sin url
        pubmed = r.find('span', 'OccurrencePID')
        if pubmed:
            #c["pubmed"] = pubmed.a['href']
            c["pubmedID"] = parse_qs(urlparse(pubmed.a['href']).query)['list_uids'][0]
        resp["references"].append(c)

    return json.dumps(resp)
