#Course : CST-205
#Title : Crypto Bot
#Abstract : Get the live crypto data of any coin listed on Kucoin using their official API with some insights.
#Authors : Sanchit Kumar, Rishabh Shetty, Chinmay Nayak, Pranav Warrier and Rohit Kannaujiya.
#Date : 05/21/2022



import streamlit as st
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
from kucoin.client import Market
client = Market(url='https://api.kucoin.com')

tv = TvDatafeed()
tickers = client.get_all_tickers() #importing data from API
tickers = pd.DataFrame(tickers['ticker'])
tickers['symbol'].replace('-','', regex=True, inplace=True)



st.set_page_config(layout="wide")


st.title("Crypto Data")
st.markdown(
    "Browse and Download through the data of any crypto currency listed on Kucoin"
)

col1 = st.sidebar
col2 = st.columns(1)



def crypto_display():

    with st.sidebar:
        st.write("Crypto Inputs")
       
        segment = st.selectbox("Select Symbol",tickers['symbol'] )
        exch = st.selectbox('Select Exchange',['KUCOIN'])
        interval = st.selectbox('Select Interval',['1 Min','3 Mins','5Mins','15 Mins','1 Hour','4 Hours'])

        if interval == "1 Min":
            crypto = tv.get_hist(segment,exch,Interval.in_1_minute,n_bars=5000)
        elif interval == '5 Mins':
            crypto = tv.get_hist(segment,exch,Interval.in_5_minute,n_bars=5000)
        elif interval == '15 Mins':
            crypto = tv.get_hist(segment,exch,Interval.in_15_minute,n_bars=5000)
        elif interval == '3 Mins':
            crypto = tv.get_hist(segment,exch,Interval.in_3_minute,n_bars=5000)
        elif interval == '1 Hour':
            crypto = tv.get_hist(segment,exch,Interval.in_1_hour,n_bars=5000)
        else:
            crypto = tv.get_hist(segment,exch,Interval.in_4_hour,n_bars=5000)
        
        DSR =  crypto['close'].pct_change(1)
        volatility = DSR.std()
        DCSR = (DSR+1).cumprod()
        
    st.write(f'{segment}')
    st.download_button(
    "Download", crypto.to_csv(), file_name=f"{segment}.csv"
    ) #Download button to download all the data in csv format.
    st.write(crypto)

   
    Combine = [crypto['close'],crypto['volume']]
    df = pd.concat(Combine,axis=1)

    st.line_chart(df['close'])
    st.line_chart(df['volume']) #plottting zoom-able graphs
   
    st.markdown("""VOLATILITY IS :""")
    st.write(volatility)
    #Average daily return
    





analysis_dict = {
        "Live Data": crypto_display ,
     
    }

with st.sidebar:
    selected_analysis = st.radio("Select Analysis", list(analysis_dict.keys()))
    st.write("---")

st.header(selected_analysis)

analysis_dict[selected_analysis]()
