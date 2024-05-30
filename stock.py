import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def stockpredict(stock_code):
    try:
        # Example: If the stock code is "2330.TW", it represents TSMC stock.
        stock = yf.Ticker(stock_code + ".TW")
        
        # Retrieve historical data
        history = stock.history(period='1mo')  #  must be one of ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        
        if not history.empty:
            # Prepare data
            X = np.array(range(len(history))).reshape(-1, 1)
            y = history['Close'].values
            
            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=666)
            
            # Train linear regression model
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Make prediction for tomorrow
            tomorrow_index = len(history)
            predicted_price = model.predict([[tomorrow_index]])[0]
            
            return predicted_price
        else:
            return "No historical data available for the specified stock code."
    except Exception as e:
        return f"Error: {str(e)}"
