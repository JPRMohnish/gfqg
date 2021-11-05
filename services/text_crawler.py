import wikipedia


class Crawler:
    def __init__(self, keyword):
        self.keyword = keyword

    def crawl_wikepedia(self):
        self.data = wikipedia.page(
            title=self.keyword,
            pageid=1,
            auto_suggest=True,
            redirect=True,
            preload=True).content

    def print_data(self):
        print(self.data)
