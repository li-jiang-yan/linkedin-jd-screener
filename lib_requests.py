from collections import Counter
import itertools
from urllib.parse import quote

from bs4 import BeautifulSoup
import numpy as np
import requests
from sklearn.feature_extraction.text import CountVectorizer

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


def scrape_post_urls(keyword, location, number):
    urls = list(f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={quote(keyword)}&location={quote(location)}&start={start}" for start in range(0, int(number), 10))
    responses = list(requests.get(url) for url in urls)
    soups = list(BeautifulSoup(response.content, "html.parser") for response in responses)
    posts = itertools.chain.from_iterable(soup.find_all("li") for soup in soups)
    return list(post.select_one("a.base-card__full-link").get("href") for post in posts)


def scrape_description_texts(urls):
    responses = list(requests.get(url) for url in urls)
    soups = list(BeautifulSoup(response.content, "html.parser") for response in responses)
    description_texts = list(soup.select_one("div.description__text").prettify() for soup in soups if soup.select_one("div.description__text"))
    return description_texts


if __name__ == "__main__":
    scrape_description_texts(scrape_post_urls("Computer Science", "Singapore", 50))
