import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


account_sid = 'ACcf5b9ee7e3c0d76bcd8477bd41efc644'
auth_token = '7ea01d8e3868fe7f2df26f13a22d9e45'

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "GKO60DXL5GAFIP4H"
NEWS_API_KEY = "240697c18cb04af99b276367d909771e"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}



response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
print(data)
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing = yesterday_data["4. close"]
print(yesterday_closing)

# Get the day before yesterday's closing stock price

day_before_yesterday = data_list[1]
day_before_yesterday_closing = day_before_yesterday["4. close"]
print(day_before_yesterday_closing)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing) - float(day_before_yesterday_closing)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
positive_difference = abs(difference)

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percentage_diff = round((positive_difference / float(yesterday_closing)) * 100)

#If percentage is greater than 5 then print("Get News").
if percentage_diff > 1:
    # Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    # Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_article = [f"Headline: {article['title']}\nBrief: {article['description']}" for article in three_articles]
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    client = Client(account_sid, auth_token)

    # to send a separate message with each article's title and description to your phone number.

    # Send each article as a separate message via Twilio.
    for article_message in formatted_article:
        message = client.messages \
            .create(
            body=f'"{COMPANY_NAME}": {up_down}{percentage_diff}%\n{article_message}',
            from_='+17632251469',
            to='+919995957505'
        )
        print(message.status)


