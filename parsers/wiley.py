from parsers.default_parser import Parser


class WileyParser(Parser):

    def __init__(self):
        self.publication_info = None

    def get_title(self):
        title = self.soup.body.find('h1', 'article-header__title')
        if title:
            title = title.text.strip()
        return title

    def get_journal(self):
        journal = self.soup.body.find('strong', 'journal-header__name-title')
        if journal:
            journal = journal.text.strip()
        return journal

    def load_publication_info(self):
        self.publication_info = [x.strip() for x in
                                self.soup.body.find('p', 'issue-header__description').text.strip().split('\n')[1:]]

    def get_year(self):
        if not self.publication_info:
            self.load_publication_info()
        return self.publication_info[1][-4:]

    def get_volume(self):
        if not self.publication_info:
            self.load_publication_info()
        return self.publication_info[0].split(',')[0][6:].strip()

    def get_issue(self):
        if not self.publication_info:
            self.load_publication_info()
        return self.publication_info[0].split(',')[1].strip()[5:].strip()

    def get_pages(self):
        if not self.publication_info:
            self.load_publication_info()
        pages = self.publication_info[2][5:].strip().split('–')
        return {
            'first': pages[0],
            'last': pages[1]
        }

    def get_doi(self):
        doi = self.soup.body.find('span', 'article-info__section-doi-data')
        if doi:
            doi = doi.text.strip()  # c[1][1:]
        return doi

    def get_authors(self):
        return [a.text.strip() for a in self.soup.body.find_all('span', 'authors__name')]

    def get_abstract(self):
        abstract = self.soup.body.find('section', id='abstract')
        if abstract:
            sections = abstract.find_all('section')
            if sections:  # Dividido en secciones (Background, Method, ...)
                abstract = {}
                for s in sections[1:]:
                    if s.h3:
                        abstract[s.h3.text.strip()] = s.p.text.strip()  # { 'Background': 'bla', ... }
            else:
                abstract = abstract.p.text.strip()
        return abstract

    def get_keywords(self):
        return [(lambda k: k[:-1] if k[-1:] == ';' else k)(k.text.strip())
                for k in self.soup.body.find_all('li', 'article-info__keywords-item')]

    def get_references(self):
        refs = self.soup.body.find('ul', 'article-section__references-list')
        if refs:
            return [self.get_reference_info(r)
                    for r in refs.children
                    if r != '\n']
        return []

    def get_ref_authors(self, ref):
        return [a.text.strip() for a in ref.find_all('span', 'author')]

    def get_ref_year(self, ref):
        year = ref.find('span', 'pubYear')
        if year:
            year = year.text.strip()
        return year

    def get_ref_title(self, ref):
        title = ref.find('span', 'articleTitle')
        if title:
            title = title.text.strip()
        return title

    def get_ref_journal(self, ref):
        journal = ref.find('span', 'journalTitle')
        if journal:
            journal = journal.text.strip()
        return journal

    def get_ref_volume(self, ref):
        volume = ref.find('span', 'vol')
        if volume:
            volume = volume.text.strip()
        return volume

    def get_ref_pages(self, ref):
        first = ref.find('span', 'pageFirst')
        last = ref.find('span', 'pageLast')
        return {
            'first': first.text.strip() if first else None,
            'last': last.text.strip() if last else None
        }


    def get_ref_doi(self, ref):
        ref_info = ref.find('ul', 'article-section__references-list-additional u-horizontal-list')
        doi = None
        if ref_info:
            doi = ref_info.get('data-doi')
            for link in ref_info.find_all('a'):
                if 'doi.org' in link['href']:
                    doi = link['href'][link['href'].rfind('doi.org') + 8:]
                    break
        return doi

    def get_ref_pubmedID(self, ref):
        ref_info = ref.find('ul', 'article-section__references-list-additional u-horizontal-list')
        pmid = None
        if ref_info:
            for link in ref_info.find_all('a'):
                if 'pubmed' in link['href']:
                    pmid = link['href'][link['href'].rfind('/') + 1:]
                    break
        return pmid
