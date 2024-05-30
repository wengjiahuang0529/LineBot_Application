import yfinance as yf

def CurrentStock(stock_code):
    # Example: If the stock code is "2330.TW", it represents TSMC stock.
    stock = yf.Ticker(stock_code)
    current_price = stock.history(period='1d')['Close'].iloc[-1]
    return current_price

import stock

# Call the stockpredict function with the stock code as argument
price = stock.CurrentStock("2330.TW")  # Example for TSMC stock

print("Current price of the stock:", price)
