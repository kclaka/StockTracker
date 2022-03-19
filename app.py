import streamlit as st
from navigation import MultiApp
from apps import home, about, news # import your app modules here


import sqlite3

conn = sqlite3.connect('stocks.db')
c = conn.cursor()
#c.execute("""CREATE TABLE stocks (
#            stock_name text
 #         )""")


# c.execute("""CREATE TABLE stock_names (
           # stock_name text)"""

#)

#c.execute("INSERT INTO stocks (stock_name) VALUES ('F')")
#c.execute("INSERT INTO stocks (stock_name) VALUES ('TSLA')")
#c.execute("INSERT INTO stocks (stock_name) VALUES ('TSLA')")
#c.execute("INSERT INTO stocks VALUES ('F')")
#c.execute("INSERT INTO stocks VALUES ('META')")
#c.execute("INSERT INTO stocks VALUES 'IOT'")

conn.commit()
conn.close()

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("News", news.app)
app.add_app("About", about.app)


# The main app
app.run()