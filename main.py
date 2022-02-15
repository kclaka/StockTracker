import streamlit as st
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

st.subheader("Current Stock Price")
st.write("Call Group member microservice here {Stock Price}")
st.subheader('Raw data')
st.write(data.tail())



def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()


df_train = data['Date', 'Close']
print(df_train)
# df_train = df_train.rename(columns={"Date":"ds", "Close":"y"})
#
# m = Prophet()
# m.fit(df_train)
# future = m.make_future_dataframe(periods=period)
# forecast = m.predict(future)