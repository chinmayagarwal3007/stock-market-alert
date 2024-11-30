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

url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey={alpha_vantage_key}"


response = requests.get(url)
data = response.json()
yesterday = data["Time Series (Daily)"]['2024-11-29']["4. close"]
day_before_yesterday_closing = data["Time Series (Daily)"]['2024-11-27']["4. close"]

change = (float(yesterday) - float(day_before_yesterday_closing))/float(yesterday) * 100

if change > 0:
    logo = "📈"
else:
    logo = "📉"

if abs(change) >= 2:
    news_key = os.getenv("news_key")


    url = (f"https://newsapi.org/v2/everything?q='tesla stock'&from=2024-11-29&to=2024-11-29&language=en&sortBy=relevancy&apiKey={news_key}")

    response = requests.get(url)

    data = response.json()

    title = data["articles"][0]["title"]
    description = data["articles"][0]["description"]

    print(f"Tesla {round(change, 2)}%\nHeadline: {title}\nBrief: {description}")

    client = Client(account_sid, auth_token)

    from_number = os.getenv("from_number")
    to_number = os.getenv("to_number")


    message = client.messages.create(
    from_=from_number,
    body=f"Tesla {logo} {round(change, 2)}%\nHeadline: {title}\nBrief: {description}",
    to=to_number
    )

    print(message.sid)