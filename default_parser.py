from bs4 import BeautifulSoup

class Parser():

    def parse(self, file):
        self.soup = BeautifulSoup(open(file, encoding='utf-8'), 'html.parser')
        return {
            'title': self.get_title(),
            'publication_info': self.get_publication_info(),
            'citation': self.get_citation(),
            'ids': self.get_identifiers(),
            'authors': self.get_authors(),
            'abstract': self.get_abstract(),
            'keywords': self.get_keywords(),
            'references': self.get_references()
        }

    def get_title(self):
        return None

    def get_publication_info(self):
        """
            this function get publication information from html.
            :params soup: instance of BeautifulSoup class
        """
        return {
            'journal': self.get_journal(),
            'year': self.get_year(),
            'volume': self.get_volume(),
            'issue': self.get_issue(),
            'pages': self.get_pages()
        }

    def get_journal(self):
        return None

    def get_year(self):
        return None

    def get_volume(self):
        return None

    def get_issue(self):
        return None

    def get_pages(self):
        return {
            'first': None,
            'last': None
        }

    def get_citation(self):
        return None

    def get_identifiers(self):
        """
            this function get identifiers from html.
            :params soup: instance of BeautifulSoup class
        """
        return {
            'doi': self.get_doi(),
            'pmid': self.get_pubmedID()
        }

    def get_doi(self):
        return None

    def get_pubmedID(self):
        return None

    def get_authors(self):
        """
            this function get authors from html.
            :params soup: instance of BeautifulSoup class
        """
        return []

    def get_abstract(self):
        """
            this function get abstract from html.
            :params soup: instance of BeautifulSoup class
        """
        return None

    def get_keywords(self):
        """
            this function get keywords from html.
            :params soup: instance of BeautifulSoup class
        """
        return []

    def get_references(self):
        """
        this function get all references from html.
        :params soup: instance of BeautifulSoup class
        """
        return []

    def get_reference_info(self, ref):
        return {
            'authors': self.get_ref_authors(ref),
            'year': self.get_ref_year(ref),
            'title': self.get_ref_title(ref),
            'journal': self.get_ref_journal(ref),
            'volume': self.get_ref_volume(ref),
            'pages': self.get_ref_pages(ref),
            'reference': self.get_ref_text(ref),
            'ids': self.get_ref_identifiers(ref)
        }

    def get_ref_authors(self, ref):
        return []

    def get_ref_year(self, ref):
        return None

    def get_ref_title(self, ref):
        return None

    def get_ref_journal(self, ref):
        return None

    def get_ref_volume(self, ref):
        return None

    def get_ref_pages(self, ref):
        return None

    def get_ref_text(self, ref):
        return None

    def get_ref_identifiers(self, ref):
        return {
            'doi': self.get_ref_doi(ref),
            'pmid': self.get_ref_pubmedID(ref),
            'scholar': self.get_ref_scholar(ref)
        }

    def get_ref_doi(self, ref):
        return None

    def get_ref_pubmedID(self, ref):
        return None

    def get_ref_scholar(self, ref):
        return None