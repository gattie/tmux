import requests
import sys

stock_symbol = sys.argv[1]

result = requests.get(
    ("https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&"
    "corsDomain=finance.yahoo.com&symbols={}").format(stock_symbol)
    )

quote_response = result.json()['quoteResponse']['result'][0]

if quote_response['regularMarketChange'] > 0:
    print("#[fg=black]{}: #[fg=#66ff00]{} ({})".format(
        stock_symbol,
        quote_response['regularMarketPrice'],
        round(quote_response['regularMarketChange'], 2)
        ))
else:
    print("#[fg=black]{}: #[fg=#ff0000]{} ({})".format(
        stock_symbol,
        quote_response['regularMarketPrice'],
        round(quote_response['regularMarketChange'], 2)
        ))

