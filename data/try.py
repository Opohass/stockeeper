import yfinance as yf
import pandas as pd
import numpy as np
import glob
import os


glob_names = glob.glob(os.getcwd() + "/data/*.csv")
stock_names = []
for i in glob_names:
    stock_names.append(i.split('/')[-1][:-4].lower())

stock_data = {}
for stock in stock_names:
    data = yf.Ticker(stock)
    data = data.history(period="5y",interval="1d")
    data = pd.DataFrame({"Date":data.index, "Close":data["Close"].values}, index=np.arange(len(data)))
    stock_data[stock] = data
    
for key in stock_data.keys():
    print(key)
    print(stock_data[key])
