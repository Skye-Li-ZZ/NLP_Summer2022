# NLP_Summer2022

## PART ONE - Download 10K annual reports for SP500 companies
Using SEC-EDGAR-text downloader to get financial reports from the EDGAR database. 
First, clone the repo, and install the packages in requirements.txt.

```
git clone https://github.com/alions7000/SEC-EDGAR-text
pip install -r SEC-EDGAR-text/requirements.txt
```

Second, choose the type of filling to download, specify start and end year as well as the path to the folder for saving the documents.

For example, 10K reports for SP500 companies (in “companies_list.txt”) from 2015 to 2021.
```
python SEC-EDGAR-text --storage=path/to/folder/EDGAR_downloader --start=20150101 --end=20220101 --filings=10-K
```

After downloading every file asked, you should see them in a folder named “batch_000X” with reports saved in several folders inside. The full folder of 10K files from 2015 to 2021 can be found in “EDGAR_files.zip” in our google drive here.

## PART TWO - Time series of sentiment scores
Use “ts_sentiment.py” to generate sentiment-score for  “Item 7, Management’s Discussion and Analysis of Financial Condition and Results of Operations” in each 10K report. 
The output of each text contains 2 components: “label” (Positive, Neutral, Negative), “score” (the probability of text classified as that label). Details of the pre-trained FinBert model can be found here.

In our analysis, we map “label” to {Positive: 1, Neutral: 0, Negative: -1}, then time it with probability. The output would be a score between -1 and 1, with 1 being a positive sentiment whereas -1 being a negative sentiment.

## PART THREE - Quality Minus Junk strategy and final analysis
Use “strategy.py” to apply Quality Minus Junk strategy, and get final analysis results.
First, download daily pricing data using “yfinance (feel free to use other data sources if you find them more reliable). Due to missing reports in PART TWO, we got only 435 companies available for following analysis. The list of these companies could be found in “available_company.csv”. Pricing data is saved in “available_prices.csv”.

Second, join price and sentiment data together. To leave enough time for the market reacting to reports, we use daily adjusted close price one month later than the issuing date of 10K for each stock. 

SP500 is a weighted index to track performance of the US stock market, based on the market cap of each company. To reflect different weightings for companies in our portfolio, we download weights of these companies in SP500 (“company_weight.csv”) to calculate relative weighting of each stock in our portfolio. After clearing up all missing values, we end up with 295 companies and 7 years of trading data for final analysis.

Finally, after all the above preparation, now we can try to quantify the impact of our sentiment scores on the return of stocks. Using the last part of code in this script, we standardize time series sentiment scores to make sure they are normally distributed. Here’s what I’m seeing: 
The Spearman's rank correlation between sentiment score and annual return is as small as 0.13. Data used for correlation is saved in “sentiment_ret.csv”.
Building a linear regression model based on CAMP model, result is shown below. Risk free returns and average market risk premiums during the past years in the US could be found in “CAPM_rets.csv”.

## Part Four - Potential research in the future
1. Average returns in different quantile bucks for sentiment scores (10th, 20th, …)
2. Correlation between number of words used in annual report and the sentiment of that text.
3. Include more factors to improve the regression model (Adj R-squared here is just 0.124, a lot room for improvements!)
4. Other data sources (e.g. 10Q reports, other parts in 10K reports, etc.) that may generate more trustworthy sentiment. 


### Appendix - files in the folder
1. available_company.csv - list of companies available for further analysis due to missing reports in EDGAR database
2. available_prices.csv - raw price data downloaded from Yahoo Finance API yfinance using Python
3. CAPM_rets.csv - risk free returns and average market risk premiums needed for CAPM model
4. EDGAR_files.zip - 10K reports downloaded from EDGAR database
5. final20221001 - final table ready for regression analysis 
6. FinBERT-demo.ipynb - demo for FinBERT classification model
7. sentiment_ret.csv - standardized sentiment scores and annual returns, used to calculate Spearman's rank correlation
8. strategy20221001.csv - companies with report issued dates, business date after a month and stock price on that trading date
9. strategy20221001.py - 2nd script to combine sentiment scores data with pricing data, as well as all analysis performed in this project
10. tbl_available_price20220913.csv -  transformed table with pricing data for each company, needed to merge with ts_sentiment table
11. ts_sentiment.csv - panel data with sentiment score for each company each year
12. ts_sentiment20220913.py - script to input 10K text files and generate sentiment scores
