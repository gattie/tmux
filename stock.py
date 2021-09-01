#!/usr/bin/env python3

import requests
import argparse

def color_coding(color_codes):
    if color_codes == 'tmux':
        red = '#[fg=#ff0000]'
        green = '#[fg=#66ff00]'
        black = '#[fg=black]'
    else:
        red = '\033[1;31;40m'
        green = '\033[1;32;40m'
        black = '\033[1;30;40m'

    return red, green, black

def get_quote(stock_symbol):
    headers = {
            'User-Agent': 'curl/7.54.0'
            }
    result = requests.get(
        ("https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&"
        "region=US&corsDomain=finance.yahoo.com&symbols={}").format(
            stock_symbol), headers=headers)

    return result.json()['quoteResponse']['result'][0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', required=True)
    parser.add_argument(
        '--color-format',
        '-c',
        dest='color',
        default='terminal',
        choices=['tmux', 'terminal']
    )
    parser.add_argument(
        '--percent-change', '-p', dest='percent', action='store_true')
    parser.add_argument(
        '--market-change', '-m', dest='market', action='store_true')
    parser.add_argument('--name', '-n', action='store_true')
    args = parser.parse_args()

    quote_response = get_quote(args.symbol)

    color_red, color_green, color_black = color_coding(args.color)

    if quote_response['regularMarketChange'] > 0:
        color_value_change = color_green
    else:
        color_value_change = color_red

    if args.percent:
        percent_change = " [{}%]".format(
            round(quote_response['regularMarketChangePercent'], 2))
    else:
        percent_change = ''

    if args.market:
        market_change = " ({})".format(
            round(quote_response['regularMarketChange'], 2))
    else:
        market_change = ''

    if args.name:
        name = quote_response['shortName']
    else:
        name = quote_response['symbol']

    print("{}{}: {}{}{}{}".format(
        color_black,
        name,
        color_value_change,
        round(quote_response['regularMarketPrice'], 2),
        market_change,
        percent_change
        ))

if __name__ == "__main__":
    main()
