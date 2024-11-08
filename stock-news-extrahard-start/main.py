import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import os

account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')

today = datetime.today()
yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
two_days_ago = (today - timedelta(days=2)).strftime("%Y-%m-%d")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stocks_endpoint = "https://www.alphavantage.co/query"
news_endpoint = "https://newsapi.org/v2/everything"

api_key_stocks = os.getenv('api_key_stocks')
api_key_news = os.getenv('api_key_news')

stocks_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key_stocks
}

news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "language": "en",
    "pageSize": 3,
    "apikey": api_key_news
}

news_response = requests.get(news_endpoint, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()

stocks_response = requests.get(stocks_endpoint, params=stocks_parameters)
stocks_response.raise_for_status()
stocks_data = stocks_response.json()
yesterday_data = stocks_data["Time Series (Daily)"][yesterday]["4. close"]
two_days_ago_data = stocks_data["Time Series (Daily)"][two_days_ago]["4. close"]
difference = abs(float(yesterday_data) - float(two_days_ago_data))
percentage = difference * 100 / float(two_days_ago_data)
if percentage >= 5:
    client = Client(account_sid, auth_token)
    percentage_message = client.messages.create(
        body=f"There's been a {percentage} change in your Tesla shares",
        from_='+12172671228',
        to='+34628850650'
    )
    first_new = client.messages.create(
        body=f"Title: {news_data['articles'][0]['title']}\n\n{news_data['articles'][0]['description']}",
        from_='+12172671228',
        to='+34628850650'
    )
    print(first_new.status)
