# -*- coding: utf-8 -*-
"""
Brandeis International Business School
NLP Analysis - Summer 2022

PART THREE
Quality Minus Junk strategy and final analysis

@author: Skye Li
"""
#%%
"""
Import libraries needed
"""
import pandas as pd
import yfinance as yf
#from pandas.tseries.offsets import BDay
from scipy import stats
import pandas_market_calendars as mcal
from datetime import timedelta
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

#%%
"""
Download price data
"""
# due to missing reports in EDGAR database, we have only 435 for analysis
# date from 2015 - 2021
df_company = pd.read_csv('available_company.csv')

company_list = df_company['Company'].to_list()
data_price = yf.download(company_list, start='2014-12-01', end='2022-08-05') # The latest report published on 20220701

# save to csv file
data_price.to_csv('available_prices.csv')

#%%
"""
Join price & sentiment tables
"""
## price
# read raw csv file
df_sp500_prices = pd.read_csv('available_prices.csv', skiprows=[0,2])
df_sp500_prices = df_sp500_prices.rename(columns = {'Unnamed: 0':'Date'})

# change dataframe structure
df_price = pd.melt(df_sp500_prices, 
            id_vars='Date', 
            value_vars=list(df_sp500_prices.columns[1:]), 
            var_name='Company', 
            value_name='Price')
# change Date to datetime format
df_price['Date']=pd.to_datetime(df_price['Date'],format='%Y/%m/%d')

# Save dataframe to csv file as a backup
df_price.to_csv('tbl_available_price.csv')


## ts sentiment
# import csv file
ts_sentiment = pd.read_csv('ts_sentiment.csv')
ts_sentiment = ts_sentiment[['Company', 'Date', 'Sentiment_Score']].copy()

# change data to datetime format
ts_sentiment['Date'] = pd.to_datetime(ts_sentiment['Date'],format='%Y%m%d')

## join to get strategy table
# Find the next business day
ts_sentiment['Next_Date'] = ts_sentiment['Date'] + timedelta(30)

# check if next_date is a trading date
def helper_trading_date(date):
    # create a calendar
    nyse = mcal.get_calendar('NYSE')
    # get all trading days
    days = nyse.valid_days(start_date='2014-12-31', end_date='2022-12-31')
    if date not in days:
        date = date + timedelta(days=1)
    return date

# Repeat this process until you get all trading dates as next date
# This is stupid, but it works. Still trying to figure out why {while} would blow up the loop...
ts_sentiment['Next_Date'] = ts_sentiment['Next_Date'].map(helper_trading_date) # run this

# Join Company price on the next business day with 10K report published
strategy = ts_sentiment.merge(df_price, left_on=['Company','Next_Date'], right_on = ['Company','Date'], how='left') 
df_strategy = strategy[['Company', 'Date_x', 'Next_Date', 'Sentiment_Score', 'Price']].copy()
df_strategy.to_csv('strategy.csv')

# Missing prices
df_strategy = pd.read_csv('strategy.csv')
df_strategy = df_strategy.dropna()
df_complete = df_strategy.groupby('Company').count()
df_complete = df_complete[df_complete['Price']==8].reset_index() # 339 companies

#%%
"""
Regression Analysis
"""
df = df_strategy.copy()
# helper column for return
df['lag_Price'] = df['Price'].shift(1)
# helper column to identify rows to discard
df['company_shift'] = df['Company'].shift(1)

# calculate annual return
df = df[df['Company'] == df['company_shift']]
df['ret'] = df['Price']/df['lag_Price'] - 1
df = df.sort_values(['Company', 'Date_x'])

# standardize sentiment scores
ts_std = df['Sentiment_Score'].std()
ts_mean = df['Sentiment_Score'].mean()
df['sentiment_new'] = (df['Sentiment_Score'] - ts_mean)/ts_std

# save standardized sentiment scores and annual returns
df_sentiment_ret = df[['Company','sentiment_new', 'ret']].copy()
df_sentiment_ret.to_csv('sentiment_ret.csv')

# rank correlation between sentiment score and return
df_sentiment_ret = pd.read_csv('sentiment_ret.csv')
stats.spearmanr(df_sentiment_ret['sentiment_new'], df_sentiment_ret['ret'])
# SpearmanrResult(correlation=0.12766271776651647, pvalue=2.8517073421156885e-11)


df_capm = pd.read_csv('CAPM_rets.csv')
df['Year'] = pd.DatetimeIndex(df['Date_x']).year
df_final = df.merge(df_capm, left_on=['Year'], right_on=['Date'], how='inner')[['Company', 'Year', 'ret', 'Sentiment_Score', 'Mkt-RF', 'RF']].copy()

df_final.to_csv('final.csv')

# Use linear regression to quantify the impact of sentiment score
y = df_final['ret'] - df_final['RF']
X = df_final[['Mkt-RF', 'Sentiment_Score']]
lr = sm.OLS(y, X)
results = lr.fit()
print(results.summary())


