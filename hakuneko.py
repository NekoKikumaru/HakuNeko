import cloudscraper, json
from bs4 import BeautifulSoup

class HakuNeko:

    def url2soup(self, url):
        scraper = cloudscraper.CloudScraper()
        html = scraper.get(url).text
        soup = BeautifulSoup(html, features='html.parser')
        return soup

    def hakuneko(self, comics, extension):
        f = open('hakuneko.mangas.'+extension, 'w+', encoding='utf8')
        f.write(json.dumps(comics))

class MangaGo:

    def __init__(self):
        super().__init__()
        self.run()
    
    def generate(self):
        pages = []
        base = 'https://www.mangago.me/list/directory/all/'
        result = None
        while result is None:
            soup = HakuNeko().url2soup(base+'1/')
            div = soup.find('div', {'class': 'pagination'})
            result = div
        count = int(div['total'])
        for i in range(count):
            pages.append(base+str(i+1)+'/')
        return pages

    def scrape(self, pages):
        comics = []
        for page in pages:
            print('Currently scraping: '+page)
            result = 0
            while result == 0:
                soup = HakuNeko().url2soup(page)
                aList = soup.findAll('a', {'class': 'lazy'})
                for a in aList:
                    comics.append({'id': a['href'], 'title': a['title']})
                result = len(aList)
        comics = sorted(comics, key=lambda c: c['title'])
        return comics

    def run(self):
        pages = self.generate()
        comics = self.scrape(pages)
        HakuNeko().hakuneko(comics, 'mangago')

if __name__ == '__main__':
    source = 'mangago'
    if source == 'mangago':
        MangaGo()
