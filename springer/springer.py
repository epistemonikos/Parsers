import json
from bs4 import BeautifulSoup

def springer_parser(file):
    soup = BeautifulSoup(open(file, encoding='utf-8'), 'html.parser')
    resp = {}

    # Extraer nombre
    name = soup.body.find('h1', 'ArticleTitle')
    if name:
        resp["name"] = name.contents[0].strip()

    # Extraer Journal
    journal = soup.body.find('span', 'JournalTitle')
    if journal:
        resp["journal"] = journal.contents[0].strip()

    # Extraer Año
    year = soup.body.find('span', 'ArticleCitation_Year')
    if year:
        resp["year"] = year.time.contents[0].strip()

    # Extraer Volume
    volume = soup.body.find('span', 'ArticleCitation_Volume')
    if volume:
        resp["volume"] = volume.contents[0].strip()

    # Extraer Issue
    issue = soup.body.find('span', 'ArticleCitation_Issue')
    if issue:
        resp["issue"] = issue.contents[0].strip()

    # Extraer Paginas
    pages = soup.body.find('span', 'ArticleCitation_Pages')
    if pages:
        resp["pages"] = pages.contents[0].strip()

    # Extraer cita
    cite = soup.body.find(id='citethis-text')
    if cite:
        resp["citation"] = cite.contents[0].strip()

    # Extraer DOI
    article_doi = soup.body.find('p', 'article-doi')
    if article_doi:
        resp["doi"] = article_doi.contents[1][1:].strip()

    # Extraer Autores
    resp["authors"] = []
    for a in soup.body.find_all('span', 'authors__name'):
        resp["authors"].append(a.contents[0].strip())

    # Extraer Abstract
    abstract = soup.body.find('section', 'Abstract')
    sections = abstract.find_all('div', 'AbstractSection')
    if sections:
        a = {}
        for s in sections:
            a[s.h3.contents[0].strip()] = s.p.contents[0].strip()
        resp["abstract"] = a
    else:
        resp["abstract"] = abstract.p.contents[0].strip()

    # Extraer keywords
    resp["keywords"] = []
    for k in soup.body.find_all('span', 'Keyword'):
        resp["keywords"].append(k.contents[0].strip())

    # Extraer referencias
    resp["references"] = []
    for r in soup.body.find_all('div', 'CitationContent'):
        c = {}
        c["citation"] = r.contents[0].strip()
        doi = r.find('span', 'OccurrenceDOI')
        if doi:
            c["doi"] = doi.a['href'][18:]
        pubmed = r.find('span', 'OccurrencePID')
        if pubmed:
            c["pubmed"] = pubmed.a['href']
        resp["references"].append(c)

    return json.dump(resp)
