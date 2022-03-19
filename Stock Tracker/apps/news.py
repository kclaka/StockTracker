import streamlit as st
import requests
from bs4 import BeautifulSoup


def app():
    st.header("News")
    try:
        r = requests.get('https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069')
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            if len(link) < 10 or len(title) < 10:
                continue
            else:
                published = a.find('pubDate').text
                st.subheader(f"[{title}](%s)" % link)
                st.write(f"Published on {published}")
    except ValueError:
        pass
