import yfinance as yf
import pandas as pd
import numpy as np
#thanks chatgpt

def fetch_stock_data(symbol, start_date, end_date):
    """
    Fetch stock data from Yahoo Finance.

    Parameters:
    - symbol: Ticker symbol of the stock.
    - start_date: Start date in the format 'YYYY-MM-DD'.
    - end_date: End date in the format 'YYYY-MM-DD'.

    Returns:
    - data: pandas DataFrame with 'High', 'Low', 'Close', and 'Volume' columns.
    """
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def calculate_obv(data):
    """
    Calculate On-balance volume (OBV).

    Parameters:
    - data: pandas DataFrame with 'Close' and 'Volume' columns.

    Returns:
    - obv: list containing OBV values.
    """
    obv = []
    prev_obv = 0

    for i in range(1, len(data)):
        if data['Close'][i] > data['Close'][i - 1]:
            obv.append(prev_obv + data['Volume'][i])
        elif data['Close'][i] < data['Close'][i - 1]:
            obv.append(prev_obv - data['Volume'][i])
        else:
            obv.append(prev_obv)
        prev_obv = obv[-1]

    return obv

def calculate_adl(data):
    """
    Calculate Accumulation/distribution (A/D) line.

    Parameters:
    - data: pandas DataFrame with 'High', 'Low', 'Close', and 'Volume' columns.

    Returns:
    - adl: list containing A/D line values.
    """
    adl = [0]

    for i in range(1, len(data)):
        mf_multiplier = ((data['Close'][i] - data['Low'][i]) - (data['High'][i] - data['Close'][i])) / (data['High'][i] - data['Low'][i])
        adl.append(adl[-1] + mf_multiplier * data['Volume'][i])

    return adl

def calculate_adx(data, period=14):
    """
    Calculate Average directional index (ADX).

    Parameters:
    - data: pandas DataFrame with 'High', 'Low', 'Close' columns.
    - period: window size for calculating ADX (default is 14).

    Returns:
    - adx: list containing ADX values.
    """
    tr = pd.DataFrame(index=data.index, columns=['TR'])
    tr['TR'] = np.maximum.reduce([data['High'] - data['Low'], abs(data['High'] - data['Close'].shift(1)), abs(data['Low'] - data['Close'].shift(1))])

    atr = tr['TR'].rolling(window=period, min_periods=1).mean()
    dx = 100 * (atr.diff() / atr).ewm(span=period, adjust=False).mean().abs()

    adx = dx.rolling(window=period, min_periods=1).mean()

    return adx

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Calculate Moving average convergence divergence (MACD).

    Parameters:
    - data: pandas DataFrame with 'Close' column.
    - short_window: short-term moving average window size (default is 12).
    - long_window: long-term moving average window size (default is 26).
    - signal_window: signal line window size (default is 9).

    Returns:
    - macd: list containing MACD values.
    """
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    
    macd = macd_line - signal_line
    
    return macd

def calculate_rsi(data, window=14):
    """
    Calculate Relative strength index (RSI).

    Parameters:
    - data: pandas DataFrame with 'Close' column.
    - window: window size for calculating RSI (default is 14).

    Returns:
    - rsi: list containing RSI values.
    """
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi