import os
import requests
import string
from bs4 import BeautifulSoup

host = "https://www.nature.com"
pages_link_base = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page="
articles_link = "https://www.nature.com/nature/articles"


def get_news_links(url, type_):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    article_types = soup.find_all("span", class_="c-meta__type")
    links = {}

    for item in article_types:
        if item.text == type_:
            article_name = item.find_previous("a").text
            transtable = str.maketrans(dict.fromkeys(string.punctuation))  # OR {key: None for key in string.punctuation}
            article_name = article_name.translate(transtable).replace(" ", "_")
            links[article_name] = host+item.find_previous("a")["href"]
    return links


def get_article_body(link):
    html_doc = requests.get(link)
    link_content = BeautifulSoup(html_doc.content, "html.parser")
    if type_articles == "Research Highlight":
        article = link_content.find("div", class_="article-item__body")
    else:
        article = link_content.find("div", class_="article__body")
    return bytes(article.text.strip(), encoding='utf-8')


def save_articles(links_list):
    saved_articles_list = []
    for article_name, article_link in links_list.items():
        response = requests.get(article_link)
        article_body = get_article_body(article_link)
        if response:
            filename = os.path.join(dirname, article_name+'.txt')
            file = open(filename, 'wb')
            file.write(article_body)
            file.close()
            saved_articles_list.append(article_name)
            print(f'Content of "{article_name}.txt" saved.')
        else:
            print(f"The URL returned {response.status_code}")
    print(f"Saved {len(saved_articles_list)} articles:", saved_articles_list)


qty_pages = int(input('Number of pages: '))
type_articles = input('Type of articles: ')
pages_links = [articles_link]
for i in range(2, qty_pages+1):
    pages_links.append(pages_link_base + str(i))
# print(pages_links)
for page_link in pages_links:
    page_n = 'Page_' + str(pages_links.index(page_link)+1)
    scrape_links = get_news_links(page_link, type_articles)
    dirname = os.path.join(os.getcwd(), page_n)
    if page_n not in os.listdir() or not os.path.isdir(dirname):
        os.mkdir(dirname)
    save_articles(scrape_links)
