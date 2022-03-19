import streamlit
import streamlit as st
import requests
from datetime import date


import yfinance as yf

from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go




START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Tracker and Predictor")

stocks = ("TSLA", "MSFT", "F", "AAPL")
selected = st.selectbox("Select Stock you want to predict", stocks)

n_years = st.slider("Years of prediction:", 1, 5)
period = n_years * 365




@st.cache
def load_stock(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text("Loading data...")
data = load_stock(selected)
data_load_state = st.text("Done!")
r =requests.get(f'https://cs361-stock-price-conversion.herokuapp.com/search?stock={selected}')
print(r.json())
st.subheader(f"Current Stock Price: ${r.json()['stock_price']}" )
st.write("Call Group member microservice here {$895}")
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

df_train = df_train.rename(columns={"Date":"ds", "Close":"y"})

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