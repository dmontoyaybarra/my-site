import streamlit as st 
import pandas as pd
import yahoo_fin.stock_info as yff 
import datetime as dt
import yfinance as yf
import plotly.express as px

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #144664;">
  <a class="navbar-brand" href="https://www.linkedin.com/in/domingo-montoya-a47324179" target="_blank">Domingo Montoya</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.linkedin.com/in/domingo-montoya-a47324179" target="_blank">LinkedIn</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://twitter.com/Dmontoyaybarra" target="_blank">Twitter</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

options = st.sidebar.selectbox("Select project", ("Earnings and Dividends", "Drowdown"))
st.header(options)

if options == "Earnings and Dividends":
    st.write("Only stocks are available for this option")
    st.subheader("Next date will be:")
    symbol = st.sidebar.text_input("Symbol:", value="")
    if symbol != "":
        earnings = yff.get_next_earnings_date(symbol).strftime("%d-%b-%Y")
        st.write(earnings)
    
        start = dt.datetime(2021,1,1)
        end = dt.datetime.now()
    
        st.subheader("Last dividends:")
        dividends = yff.get_dividends(symbol,start_date=start,end_date=end,index_as_date=True)
        df_dividends = pd.DataFrame(dividends)
        df_dividends.reset_index(inplace=True)
        df_dividends.rename(columns={"index":"Dates"}, inplace=True)
        df_dividends.rename(columns={"dividend":"Dividends"}, inplace=True)
        st.dataframe(df_dividends)
    else:
        st.write("Please enter the symbol")

if options == "Drowdown":
    stock = st.sidebar.text_input("Stock/ETF:", value="")
    if stock != "":
        stock_data = yf.Ticker(stock).history("5y")
        moving_windows_size = 252
        roll_max = stock_data['Close'].rolling(moving_windows_size,min_periods=1).max()
        daily_drowdown = stock_data['Close']/roll_max - 1
    
        chart = px.line(stock_data['Close'],title="Historical data of " + stock.upper() + " last 5Y")
        drowdown_chart = px.line(daily_drowdown,title="Drowdown")
        st.write(chart)
        st.write(drowdown_chart)
    else:
       st.write("Enter the symbol")
        

    