import requests

result = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols=^GSPC")

quote_response = result.json()['quoteResponse']['result'][0]

if quote_response['regularMarketChange'] > 0:
    print("#[fg=#66ff00]{} ({})".format(quote_response['regularMarketPrice'], round(quote_response['regularMarketChange'], 2)))
else:
    print("#[fg=#ff0000]{} ({})".format(quote_response['regularMarketPrice'], round(quote_response['regularMarketChange'], 2)))

