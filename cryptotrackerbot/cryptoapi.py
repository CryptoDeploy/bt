
import requests


def get_price(coins):
    result = dict()
    quote_symbols = ['WETH', 'USDT', 'quote_volume']
    upper_coins = [coin.upper() for coin in coins]
    for coin in upper_coins:
        result[coin] = dict()

    response = requests.get('https://next.api.uniswap.info/v2/tickers', headers={'x-api-key': '1tme3bEk2f50bUdDEbTE04P53XsQHbWb9qrz5bhl'}).json()
    while item := response.popitem() if response else None:
        if item[1]['base_symbol'] in upper_coins and item[1]['quote_symbol'] in quote_symbols:
            result[item[1]['base_symbol']][item[1]['quote_symbol']] = item[1]['last_price']

    return result

def get_rank(limit=10):
    base = "https://api.coinmarketcap.com/v1/ticker/?limit={}"
    response = requests.get(base.format(limit)).json()
    return response


def get_history(coin, interval=None, limit=None, aggregate=3):
    interval_string = 'histominute' if interval == 'minute' else 'histohour' if interval == 'hour' else 'histoday'
    base = "https://min-api.cryptocompare.com/data/{}?fsym={}&tsym=USD&limit={}&aggregate={}&e=CCCAGG"
    string = base.format(interval_string, coin.upper(), limit, aggregate)
    response = requests.get(string).json()
    return response

