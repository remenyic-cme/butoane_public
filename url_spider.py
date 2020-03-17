# author: Claudiu Remenyi

"""
REQUIREMENTS:
Python 3+
requests-html: https://pypi.org/project/requests-html/
pip install requests-html
"""
from urllib.parse import urlparse
from requests_html import HTMLSession

'''
Spider class takes 1 argumet, which is the website uri
'''
class Spider():
    session = HTMLSession()
    website = None
    to_crawl = []
    crawled = []

    # initializes the spider
    def __init__(self, site_url):
        self.website = site_url

    # self calling method which crawls website uri, collects and validates links
    # to have same base uri as the main website and adds them to to_crawl list
    # after job is done, method calls itself in an attempt to empty the to_crawl list
    # by moving links from to_crawl to crawled list and crawls them
    def get_links(self, **kwargs):
        if 'link' in kwargs.keys():
            link = kwargs['link']
            print('Crawling: ', link)
        else: link = self.website

        #initializer for current request session
        web_session = self.session.get(link)
        links = web_session.html.absolute_links

        if link in self.to_crawl:
            idx = self.to_crawl.index(link)
            self.crawled.append(self.to_crawl.pop(idx))
        for l in links:
            if l in self.crawled:
                continue
            else:
                parsed_link = urlparse(l)
                if parsed_link.netloc == urlparse(self.website).netloc:
                    self.to_crawl.append(l)
                    # writing each link to a .txt file so they can be used later
                    with open("links.txt", "a") as savefile:
                        savefile.write(l + '\n')
        print('Links to crawl: ', len(self.to_crawl))
        print('Crawled links: ', len(self.crawled))
        print('----------------------')
        self.to_crawl = list(set(self.to_crawl))
        # as long 'to_crawl' is not empty, it will keep crawling first link it finds in
        if len(self.to_crawl) > 0:
            self.get_links(link=self.to_crawl[0])


r = Spider('https://www.example.com/')
r.get_links()
