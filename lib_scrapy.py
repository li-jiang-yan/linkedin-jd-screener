from collections import Counter
import itertools
from urllib.parse import quote

from bs4 import BeautifulSoup
import crochet
import numpy as np
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from sklearn.feature_extraction.text import CountVectorizer

from scraper.spiders.post_spider import PostSpider

crochet.setup()
runner = CrawlerRunner(get_project_settings())

def extract_text(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    lines = list(line.strip() for line in soup.get_text().split("\n") if line.strip())
    return "\n".join(lines)


def count_tokens(texts):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    tokens = vectorizer.get_feature_names_out()
    counts = map(int, np.sum(np.where(X.toarray() > 0, 1, 0), axis=0))
    return Counter(dict(zip(tokens, counts)))


@crochet.wait_for(timeout=180.0)
def crawl_post(url):
    crawler = runner.create_crawler(PostSpider)
    d = crawler.crawl(start_url=url)

    def done(_):
        return crawler.spider.items

    d.addCallback(done)
    return d


def scrape_post_urls(keyword, location, number):
    urls = list(f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={quote(keyword)}&location={quote(location)}&start={start}" for start in range(0, int(number), 25))
    responses = itertools.chain.from_iterable(crawl_post(url) for url in urls)
    soups = list(BeautifulSoup(response["body"], "html.parser") for response in responses)
    posts = itertools.chain.from_iterable(soup.find_all("li") for soup in soups)
    return list(post.select_one("a.base-card__full-link").get("href") for post in posts)


def scrape_description_texts(urls):
    responses = itertools.chain.from_iterable(crawl_post(url) for url in urls)
    soups = list(BeautifulSoup(response["body"], "html.parser") for response in responses)
    description_texts = list(soup.select_one("div.description__text").prettify() for soup in soups if soup.select_one("div.description__text"))
    return description_texts


if __name__ == "__main__":
    scrape_description_texts(scrape_post_urls("Computer Science", "Singapore", 50))
