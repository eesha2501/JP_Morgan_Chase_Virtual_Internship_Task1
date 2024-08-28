import urllib.request
import json
import random

# Server API URLs
QUERY = "http://localhost:8085/query?id={}"

def getDataPoint(quote):
    """ Produce all of the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price']) if quote['top_bid'] else 0
    ask_price = float(quote['top_ask']['price']) if quote['top_ask'] else 0
    price = (bid_price + ask_price) / 2 if bid_price and ask_price else 0
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None
    return price_a / price_b

def query_server(query_id):
    """ Query the server and return the response as a JSON object """
    url = QUERY.format(query_id)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data

if __name__ == "__main__":
    quotes = query_server(random.random())
    for quote in quotes:
        stock, bid_price, ask_price, price = getDataPoint(quote)
        print(f"Quoted {stock} at (bid: {bid_price}, ask: {ask_price}, price: {price})")
    
    # Calculate ratio if both stocks are available
    prices = {quote['stock']: getDataPoint(quote)[3] for quote in quotes}
    if 'ABC' in prices and 'DEF' in prices:
        ratio = getRatio(prices['ABC'], prices['DEF'])
        print(f"Ratio ABC/DEF: {ratio}")
    else:
        print("One or both stocks are missing, cannot calculate ratio.")
