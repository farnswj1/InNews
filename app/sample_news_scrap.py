from bs4 import BeautifulSoup
from urllib.request import urlopen
from newspaper import Article
import nltk

nltk.download('punkt')

# By major topics
# https://news.google.com/news/rss/headlines/section/TOPIC/SPORTS

# Top news
# https://news.google.com/news/rss

# By Search query
# https://news.google.com/rss/search?q={query}

url = 'https://news.google.com/rss/search?q=politics'

with urlopen(url) as site:  # Open that site, then close after
    data = site.read()  # read data from site

sp_page = BeautifulSoup(data, 'xml')  # scrapping data from site
news_list = sp_page.find_all('item')  # finding news
print(news_list)

for news in news_list:  # printing news
    news_data = Article(news.link.text)
    news_data.download()
    news_data.parse()
    news_data.nlp()

    print('Title:', news.title.text)
    print('News Link', news.link.text)
    print("News Summary:", news_data.summary)
    print("News Poster Link:", news_data.top_image)
    print("Pub date: ", news.pubDate.text)
    print('-' * 60)
