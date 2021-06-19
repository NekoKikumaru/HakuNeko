import cloudscraper, inquirer, json, os
from bs4 import BeautifulSoup

class HakuNeko:

    def progress(self, url):
        print('Currently scraping: '+url)

    def url2soup(self, url):
        scraper = cloudscraper.CloudScraper()
        html = scraper.get(url).text
        soup = BeautifulSoup(html, features='html.parser')
        return soup

    def hakuneko(self, comics, extension):
        comics = sorted(comics, key=lambda c: c['title'])
        f = open('Include\\hakuneko.mangas.'+extension, 'w+', encoding='iso-8859-8')
        f.write(json.dumps(comics))
        f.close()
        print('hakuneko.mangas.'+extension+' is in '+os.getcwd()+'\\Include')

class MangaGo:

    def __init__(self):
        super().__init__()
        self.run()
    
    def generate(self):
        base = 'https://www.mangago.me/list/directory/all/'
        result = None
        while result is None:
            soup = HakuNeko().url2soup(base+'1/')
            div = soup.find('div', {'class': 'pagination'})
            result = div
        pages = int(div['total'])
        pages = [base+str(p+1)+'/' for p in list(range(pages))]
        return pages

    def scrape(self, pages):
        comics = []
        for page in pages:
            HakuNeko().progress(page)
            result = 0
            while result == 0:
                soup = HakuNeko().url2soup(page)
                aList = soup.findAll('a', {'class': 'lazy'})
                for a in aList:
                    comics.append({'id': a['href'], 'title': a['title']})
                result = len(aList)
        return comics

    def run(self):
        pages = self.generate()
        comics = self.scrape(pages)
        HakuNeko().hakuneko(comics, 'mangago')

if __name__ == '__main__':
    sources = ['Mangago']
    question = [inquirer.List('source', message="Select the source to generate hakuneko data", choices=list(sources))]
    answer = inquirer.prompt(question)
    if answer['source'] == sources[0]:
        MangaGo()
