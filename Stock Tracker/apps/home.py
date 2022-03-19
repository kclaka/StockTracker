import streamlit
import streamlit as st
import requests
from datetime import date

import yfinance as yf

from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import sqlite3


def add_stock():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    new_stock = st.text_input("Enter stock", max_chars=10)
    query = f"INSERT INTO stocks (stock_name) VALUES (new_stock)"
    c.execute(query)



    conn.commit()
    conn.close()


def app():
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title("Stock Tracker and Predictor")

    stocks = c.execute("SELECT * FROM stocks")
    stock_select = set([x[0] for x in stocks])
    selected = st.selectbox("Select Stock you want to predict", stock_select)

    conn.commit()
    conn.close()

    @st.cache
    def load_stock(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

    st.button("Add Stock to your list", on_click=add_stock())


    data = load_stock(selected)

    r = requests.get(f'https://cs361-stock-price-conversion.herokuapp.com/search?stock={selected}')
    print(r.json())
    st.write(f"Current Stock Price of {selected}: ${r.json()['stock_price']}")

    st.subheader('Raw data')
    st.write(data.tail())

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

    df_train = data[['Date', 'Close']]

    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    n_years = st.slider("Years of prediction:", 1, 5)
    period = n_years * 365
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.subheader("Forecastt Data")
    st.write(forecast.tail())
    st.write('forecast data')
    fig1 = plot_plotly(m, forecast)
    streamlit.plotly_chart(fig1)

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
