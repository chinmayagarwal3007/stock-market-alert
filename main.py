import requests
import sys
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()


# Change the encoding to 'utf-8' for the console output
sys.stdout.reconfigure(encoding='utf-8')

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")


alpha_vantage_key =  os.getenv("alpha_vantage_key")

stock_url = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey":alpha_vantage_key
}

response = requests.get(stock_url, params=stock_params)
data = response.json()

data_list = [(key, value) for (key, value) in data["Time Series (Daily)"].items()]


yesterday = data_list[0][1]["4. close"]
day_before_yesterday_closing = data_list[1][1]["4. close"]

change = (float(yesterday) - float(day_before_yesterday_closing))/float(yesterday) * 100

if change > 0:
    logo = "📈"
else:
    logo = "📉"

if abs(change) >= 2:
    news_key = os.getenv("news_key")


    news_url = "https://newsapi.org/v2/everything"

    news_params = {
        "q":"tesla stock",
        "from":data_list[0][0],
        "to":data_list[0][0],
        "language":"en",
        "sortBy":"relevancy",
        "apiKey":news_key
    }


    response = requests.get(news_url, params=news_params)

    data = response.json()

    title = data["articles"][0]["title"]
    description = data["articles"][0]["description"]

    #print(f"Tesla {round(change, 2)}%\nHeadline: {title}\nBrief: {description}")

    client = Client(account_sid, auth_token)

    from_number = os.getenv("from_number")
    to_number = os.getenv("to_number")


    message = client.messages.create(
    from_=from_number,
    body=f"Tesla {logo} {round(change, 2)}%\nHeadline: {title}\nBrief: {description}",
    to=to_number
    )

    print(message.sid)