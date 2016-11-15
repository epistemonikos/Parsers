
import re
from functools import reduce
from parsers.default_parser import Parser


def getCorrectDoi(url):
        stringSplit = url.split('/')
        if ((stringSplit[0] == 'http:' or stringSplit[0] == 'https:') and stringSplit[2] == "dx.doi.org"):
             doi = stringSplit[3:]
             return reduce( lambda x, y: x + y, doi, "")
        else:
            return  url

class ScienceDirectParser(Parser):

    def get_title(self):
        title = self.soup.body.find('h1','svTitle')
        if title:
            title = title.text.strip()
        return title

    def get_authors(self):
      resp = []
      for author in self.soup.body.find('ul', 'authorGroup noCollab svAuthor').find_all('li'):
         resp.append(author.a['data-fn']+" "+author.a['data-ln'])
      return resp

    def get_abstract(self):
        abstract = self.soup.body.find('div','abstract svAbstract ')
        c={}
        if abstract:
            for titles, texts in zip(abstract.find_all('h4'), abstract.find_all('p')):
                c[titles.get_text()] = texts.get_text()
        return c

    def get_keywords(self):
      k =[]
      for keywords in self.soup.body.find('ul','keyword').find_all('li'):
          k.append(keywords.find('span').get_text())
      return k


    def get_journal(self):
        journal = self.soup.body.find('div','publicationHead')
        if journal:
            journal = journal.find('span').get_text()
        return journal

    def get_year(self):
        volume = self.soup.body.find('p','volIssue')
        year = None
        if volume:
            year=re.search(r', (.*),', volume.contents[1]).group(1)
        return year

    def get_volume(self):
        volume = self.soup.body.find('p','volIssue')
        v = None
        if volume:
            v=volume.a.get_text().split(',')[0]
        return v

    def get_issue(self):
        volume = self.soup.body.find('p','volIssue')
        i = None
        if volume:
            i=volume.a.get_text().split(',')[1]
        return i

    def get_pages(self):
        volume = self.soup.body.find('p','volIssue')
        pages = {'first': None, 'last': None}
        if volume:
           pgs = volume.contents[1].split(',')[2]
           pages['first']= pgs.strip().split(' ')[1].split('–')[0]
           pages['last']= pgs.strip().split(' ')[1].split('–')[1]
        return pages


    def get_doi(self):
        return getCorrectDoi(self.soup.body.find('dd','doi').get_text())



    def get_references(self):
            r = []
            for groupofreferences in self.soup.body.find_all('ol','references'):
                for references in groupofreferences.find_all('ul', 'reference'):
                    r.append(self.get_reference_info(references))

            return r

    def get_ref_doi(self, ref):
        doi = ref.find('li','source')
        if doi and doi.find('a'):
            doi = getCorrectDoi(doi.find('a').get_text())
        return doi

    def get_ref_authors(self, ref):
        return ref.find('li','author').get_text()

    def get_ref_title(self, ref):
        return ref.find('li','title').p.get_text()

    def get_ref_journal(self, ref):
        source = ref.find('li','source').p.contents[0]
        return source.split(',')[0]


