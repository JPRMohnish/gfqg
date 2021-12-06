import wikipedia


class Crawler:
    def __init__(self, keyword):
        self.keyword = keyword
    def wiki_summary(self):
        self.data = wikipedia.summary(self.keyword)
        return self.data.split('==')
    def crawl_wikepedia(self):
        self.data = wikipedia.page(
            title=self.keyword,
            pageid=1,
            auto_suggest=True,
            redirect=True,
            preload=True).content
        paras = self.data.split('==')
        print(len(paras))
        print(paras[-1])
        return paras;
    def print_data(self):
        print(self.data)
