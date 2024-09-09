import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time

st.title("Real-time IBOVESPA Prices")

# Define the ticker symbol for IBOVESPA
ticker_symbol = '^BVSP'

# Get the data of the stock
bvsp = yf.Ticker(ticker_symbol)

# Create a matplotlib figure
fig, ax = plt.subplots()

# Use st.pyplot to display the plot
plot = st.pyplot(fig)

# Loop to fetch and update stock values
while True:
    # Get the historical prices for IBOVESPA
    historical_prices = bvsp.history(period='1d', interval='1m')
    
    # Get the latest price and time
    latest_price = historical_prices['Close'].iloc[-1]
    latest_time = historical_prices.index[-1].strftime('%H:%M:%S')
    
    # Clear the plot and plot the new data
    ax.clear()
    ax.plot(historical_prices.index, historical_prices['Close'], label='Stock Value')
    ax.set_xlabel('Time')
    ax.set_ylabel('Stock Value')
    ax.set_title('IBOVESPA Value')
    ax.legend(loc='upper left')
    ax.tick_params(axis='x', rotation=45)
    
    # Update the plot in the Streamlit app
    plot.pyplot(fig)
    
    # Show the latest stock value in the app
    st.write(f"Latest Price ({latest_time}): {latest_price}")
    
    # Sleep for 1 minute before fetching new data
    time.sleep(60)