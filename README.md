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
