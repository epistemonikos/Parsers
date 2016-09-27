import json
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
        resp["year"] = year.text.strip()

    # Extraer Volume
    volume = soup.body.find('span', 'ArticleCitation_Volume')
    if volume:
        resp["volume"] = volume.text.strip()     # tiene <strong> entremedio :C

    # Extraer Issue
    issue = soup.body.find('span', 'ArticleCitation_Issue')
    if issue:
        resp["issue"] = issue.text.strip()

    # Extraer Paginas
    pages = soup.body.find('span', 'ArticleCitation_Pages')
    if pages:
        resp["pages"] = pages.contents[0].strip()

    # Extraer cita
    cite = soup.body.find(id='citethis-text')
    if cite:
        resp["citation"] = cite.contents[0].strip()

    # Extraer DOI
    article_doi = soup.body.find('p', 'ArticleDOI')
    if article_doi:
        resp["doi"] = article_doi.text[4:].strip()

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
            c["doi"] = doi.a['href'][18:]
        pubmed = r.find('span', 'OccurrencePID')
        if pubmed:
            c["pubmed"] = pubmed.a['href']
        scholar = r.find('span', 'OccurrenceGS')
        if scholar:
            c["scholar"] = scholar.a["href"]
        resp["references"].append(c)

    return json.dump(resp)