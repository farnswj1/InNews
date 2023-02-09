import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
from newspaper import Article
import io
import nltk

nltk.download('punkt')

st.set_page_config(page_title='InNews 🇮🇳: A Summarised News 📰 Portal', page_icon='./Meta/newspaper.ico')


def extract_news_from_url(url):
    with urlopen(url) as page:  # Open that site and close when finished
        return page.read()  # read data from site


def fetch_news_list(url):
    news = extract_news_from_url(url)
    sp_page = bs4(news, 'xml')  # scrapping data from site
    return sp_page.find_all('item')  # finding news


def fetch_news_poster(url):
    try:
        raw_data = extract_news_from_url(url)
        filepath = io.BytesIO(raw_data)
    except:
        filepath = './Meta/no_image.jpg'

    image = Image.open(filepath)
    st.image(image, use_column_width=True)


def display_news(list_of_news, news_quantity):
    for news, index in zip(list_of_news, range(1, news_quantity + 1)):
        st.write(f'**({index}) {news.title.text}**')
        news_data = Article(news.link.text)

        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(e)

        fetch_news_poster(news_data.top_image)

        with st.expander(news.title.text):
            st.markdown(
                f'''<h6 style='text-align: justify;'>{news_data.summary}"</h6>''',
                unsafe_allow_html=True
            )
            st.markdown(f"[Read more at {news.source.text}...]({news.link.text})")

        st.success(f"Published Date: {news.pubDate.text}")


def main():
    st.title("InNews 🇮🇳: A Summarized News 📰")
    image = Image.open('./Meta/newspaper.png')

    col1, col2, col3 = st.columns([3, 5, 3])

    with col1:
        st.write("")

    with col2:
        st.image(image, use_column_width=False)

    with col3:
        st.write("")

    category = ('--Select--', 'Trending🔥 News', 'Favourite💙 Topics', 'Search🔍 Topic')
    cat_op = st.selectbox('Select your Category', category)
    
    if cat_op == category[0]:
        st.warning('Please select Type!!')
    elif cat_op == category[1]:
        st.subheader("✅ Here is the Trending🔥 news for you")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
        url = 'https://news.google.com/news/rss'  # top news
        news_list = fetch_news_list(url)
        display_news(news_list, no_of_news)
    elif cat_op == category[2]:
        av_topics = (
            'Choose Topic', 'WORLD', 'NATION',
            'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT',
            'SPORTS', 'SCIENCE', 'HEALTH'
        )
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
        
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            url = f'https://news.google.com/news/rss/headlines/section/topic/{chosen_topic}'  # category news
            news_list = fetch_news_list(url)

            if news_list:
                st.subheader(f"✅ Here are the some {chosen_topic} News for you")
                display_news(news_list, no_of_news)
            else:
                st.error(f"No News found for {chosen_topic}")
    elif cat_op == category[3]:
        user_topic = st.text_input("Enter your Topic 🔍")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=15, step=1)

        if st.button("Search") and user_topic:
            user_topic_pr = user_topic.replace(' ', '')
            url = f'https://news.google.com/rss/search?q={user_topic_pr}'  # search topics
            news_list = fetch_news_list(url)

            if news_list:
                st.subheader(f"✅ Here are the some {user_topic.capitalize()} News for you")
                display_news(news_list, no_of_news)
            else:
                st.error(f"No news found for {user_topic}")
        else:
            st.warning("Please write Topic Name to Search 🔍")


if __name__ == '__main__':
    main()
