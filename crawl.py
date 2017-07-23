import subprocess
from urllib2 import urlopen, Request
import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor


class MangaSpider(scrapy.Spider):
    name = "manga"
    start_urls = ["http://uptruyen.com/manga/147313/comedy/touch-tam-voi.html"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def shouldDownload(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html)
        sum_img = sum([1 for i in soup.find_all(
            'img')])
        return sum_img > 50

    def download(self, url):
        bashCommand = "wget -k -p {url}".format(url=url)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    def parse(self, response):
        links = LinkExtractor(
            canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            url_to = link.url
            if self.shouldDownload(url_to):
                # Download
                self.download(url_to)
