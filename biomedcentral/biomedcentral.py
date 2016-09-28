import json
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def biomed_parser(file):
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
        resp["date"] = year.text.strip()

    # Extraer Volume
    volume = soup.body.find('span', 'ArticleCitation_Volume')
    if volume:
        resp["volume"] = volume.text.strip()     # tiene <strong> entremedio :C

    # Extraer Issue
    issue = soup.body.find('span', 'ArticleCitation_Issue')
    if issue:
        resp["issue"] = issue.text.strip()

    # Extraer Paginas
    pages = soup.body.find('span', 'ArticleCitation_Pages')     # Parece que no existe en BioMed
    if pages:
        resp["pages"] = pages.text.strip()

    # Extraer cita
    cite = soup.body.find(id='citethis-text')                   # Parece que no existe en BioMed
    if cite:
        resp["citation"] = cite.contents[0].strip()

    # Extraer DOI
    article_doi = soup.body.find('p', 'ArticleDOI')
    if article_doi:
        resp["doi"] = article_doi.text[4:].strip()              # Viene como "DOI:xxx/xxx..."

    # Extraer Autores
    resp["authors"] = []
    for a in soup.body.find_all('span', 'AuthorName'):
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
    for r in soup.body.find_all('cite', 'CitationContent'):
        c = {}
        c["citation"] = r.contents[0].strip()
        doi = r.find('span', 'OccurrenceDOI')
        if doi:
            c["doi"] = doi.a['href'][18:]                       # Viene como URL
        pubmed = r.find('span', 'OccurrencePID')
        if pubmed:
            #c["pubmed"] = pubmed.a["href"]
            c["pubmedID"] = parse_qs(urlparse(pubmed.a['href']).query)['list_uids'][0]
        scholar = r.find('span', 'OccurrenceGS')
        if scholar:
            c["scholar"] = scholar.a["href"]
        resp["references"].append(c)
        
    return json.dumps(resp)
