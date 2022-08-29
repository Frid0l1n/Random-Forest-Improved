import yfinance as yf
import pandas as pd
import numpy as np

class data():
    def __init__(self, stock, start_date, end_date):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        
        price_data = yf.download(stock, start=start_date, end=end_date, interval="1d")

        #calculating change in price
        price_data["Change In Price"] = price_data["Close"].diff()

        #calculating low 14 / high 14
        n = 14
        low = price_data[["Low"]].copy()
        high = price_data[["High"]].copy()
        low_14 = low["Low"].transform(lambda x: x.rolling(window = n).min())
        high_14 = high["High"].transform(lambda x: x.rolling(window = n).max())

        #calculating RSI
        up_df, down_df = price_data[['Change In Price']].copy(), price_data[['Change In Price']].copy()
        #for updays if the change is smaller than 0 set it to 0
        #for downdays if the change is greater than 0 set it to 0
        up_df.loc['Change in Price'] = up_df.loc[(up_df['Change In Price'] < 0), 'Change In Price'] = 0
        down_df.loc['Change In Price'] = down_df.loc[(down_df['Change In Price'] > 0), 'Change In Price'] = 0
        #change the variable to an absolute variable
        down_df['Change In Price'] = down_df['Change In Price'].abs()
        #calculate the EWMA (Exponential Wheigtet Moving Average), older values are given less weight than never values
        ewma_up = up_df['Change In Price'].transform(lambda x: x.ewm(span = n).mean())
        ewma_down = down_df['Change In Price'].transform(lambda x: x.ewm(span = n).mean())
        #calculate the relative strength "RS"
        relative_strength = ewma_up/ewma_down
        #calculate the relative strength index
        relative_strength_index = 100.0 -(100.0 / (1.0+(relative_strength)))

        price_data["Low 14"] = low_14
        price_data["High 14"] = high_14
        price_data['RSI'] = relative_strength_index

        print(price_data)
        
        pass