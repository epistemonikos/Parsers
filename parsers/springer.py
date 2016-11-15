from urllib.parse import urlparse, parse_qs
from parsers.default_parser import Parser


class SpringerParser(Parser):

    def get_title(self):
        title = self.soup.body.find('h1', 'ArticleTitle')
        if title:
            title = title.text.strip()
        return title

    def get_journal(self):
        journal = self.soup.body.find('span', 'JournalTitle')
        if journal:
            journal = journal.text.strip()
        return journal

    def get_year(self):
        year = self.soup.body.find('span', 'ArticleCitation_Year')
        if year:
            year = year.time.text.strip()
        return year

    def get_volume(self):
        volume = self.soup.body.find('span', 'ArticleCitation_Volume')
        if volume:
            volume = volume.text.strip()
        return volume

    def get_issue(self):
        issue = self.soup.body.find('span', 'ArticleCitation_Issue')
        if issue:
            issue = issue.text.strip()
        return issue

    def get_pages(self):
        pages = self.soup.body.find('span', 'ArticleCitation_Pages')
        if pages:  # "pp X-Y"
            pages = pages.text.strip()
            if '–' in pages:
                pages = pages[3:].split('–')  # [ X, Y ]
                return {
                    'first': pages[0],
                    'last': pages[1]
                }
        return pages

    def get_citation(self):
        cite = self.soup.body.find(id='citethis-text')
        if cite:
            cite = cite.text.strip()
        return cite

    def get_doi(self):
        article_doi = self.soup.body.find('p', 'article-doi')
        if article_doi:
            article_doi = article_doi.text[4:].strip()  # c[1][1:]
        return article_doi

    def get_authors(self):
        return [a.text.strip() for a in self.soup.body.find_all('span', 'authors__name')]

    def get_abstract(self):
        abstract = self.soup.body.find('section', 'Abstract')
        if abstract:
            sections = abstract.find_all('div', 'AbstractSection')
            if sections:  # Dividido en secciones (Background, Method, ...)
                abstract = {}
                for s in sections:
                    if s.h3:
                        abstract[s.h3.text.strip()] = s.p.text.strip()  # { 'Background': 'bla', ... }
            else:
                abstract = abstract.p.text.strip()
        return abstract

    def get_keywords(self):
        return [k.text.strip() for k in self.soup.body.find_all('span', 'Keyword')]

    def get_references(self):
        return [self.get_reference_info(r) for r in self.soup.body.find_all('div', 'CitationContent')]

    def get_ref_text(self, ref):
        return ref.contents[0].strip()

    def get_ref_doi(self, ref):
        doi = ref.find('span', 'OccurrenceDOI')
        if doi:
            doi = doi.a['href'][18:]  # DOI sin url
        return doi

    def get_ref_pubmedID(self, ref):
        pmid = ref.find('span', 'OccurrencePID')
        if pmid:
            pmid = parse_qs(urlparse(pmid.a['href']).query)['list_uids'][0]
        return pmid
