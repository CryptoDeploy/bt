
import datetime
import time
from matplotlib.dates import date2num
from cryptotrackerbot import cryptoapi
from cryptotrackerbot import utils
from cryptotrackerbot import emoji

from telegram.ext.dispatcher import run_async



@run_async
def price_command(bot, update, args, job_queue):
    if len(args) == 0:  # return if no args added
        text = "Please use the /uprice command with the coin you wanna fetch the price \n\nExample: <code>/uprice dai weth pnk</code>"
        utils.send_autodestruction_message(bot, update, job_queue, text)
        return

    response = cryptoapi.get_price(args)
    #print(response)
    if 'Response' in response and response['Response'] == 'Error':  # return if response from api is error
        text = "<b>Error!</b>"
        text += "\n{}".format(response['Message']) if 'Message' in response else ''
        utils.send_autodestruction_message(bot, update, job_queue, text)
        return

    text = ""
    for coin in response:
        text += "<b>— {}:</b>".format(coin)
        prices = response[coin]
        for fiat in prices:
            emoji_coin = emoji.WETH if fiat.upper() == 'WETH' else emoji.USDT if fiat.upper() == 'USDT' else emoji.EUR if fiat.upper() == 'EUR' else ""
            text += "\n  - {}{}: {}".format(emoji_coin, fiat, utils.sep(prices[fiat]))
        text += "\n\n"
    utils.send_autodestruction_message(bot, update, job_queue, text)


@run_async
def help(bot, update, job_queue):
    text = (
        "<b>👋👋Welcome to BestSwap Bot👋👋</b>\n"
        "\n"
        "<b>BestSwapBot is a telegram bot that returns price of tokens listed on uniswap exchange, feel free to join our telegram group @yourgroup . Stay Safe💥💥</b>\n"
        "\n"
        "<b>🔧Bot Commands:</b>\n"
        "\n"
        "/uprice or /p  - <i>return price of Uniswap assets</i>\n"
        "/help - <i>return help message</i>\n"
        "/rank - <i>return coins rank</i>\n"
        "/graph - <i>return coins graph</i>\n"
        "\n"
        "⚠️: Bot automatically cleans up its messages if given admin rights in supergroups "
        "\n""\n"
        "For more info please stay tuned to <a href=\"https://t.me/bestswap\">BestSwap</a>."
    )
    utils.send_autodestruction_message(bot, update, job_queue, text, destruct_in=120, disable_web_page_preview=True)


@run_async
def rank_command(bot, update, job_queue):
    text = ""
    response = cryptoapi.get_rank()
    for coin in response:
        text += "<b>{}){}:</b>".format(coin['rank'], coin['symbol'])
        text += " {}".format("+" if utils.string_to_number(coin["percent_change_24h"]) > 0 else "")
        text += "{}%{}".format(coin["percent_change_24h"], utils.arrow_up_or_down(utils.string_to_number(coin["percent_change_24h"])))
        text += " {}{}".format(utils.sep(round(utils.string_to_number(coin['price_usd']), 2)), emoji.USD)
        text += "\n"
    utils.send_autodestruction_message(bot, update, job_queue, text, destruct_in=120)



@run_async
def graph_command(bot, update, job_queue, args):
    if len(args) != 1:
        text = "Error: You have to append to the command as parameters the code of only one crypto you want\n\nExample:<code>/graph btc</code>"
        utils.send_autodestruction_message(bot, update, job_queue, text)
        return
    coin = args[0]
    intervals = ['1d', '1w']#, 'day']
    for interval in intervals:
        send_graph(bot, update, job_queue, coin, interval)



def send_graph(bot, update, job_queue, coin, interval):
    if interval == '1d':
        limit = 600
        interval_string = 'minute'
        aggregate = 10
    elif interval == '1w':
        limit = 600
        interval_string = 'hour'
        aggregate = 1
    response = cryptoapi.get_history(coin, aggregate=aggregate, limit=limit, interval=interval_string)
    if 'Response' in response and response['Response'] == 'Error':  # return if response from api is error
        text = "<b>Error!</b>"
        text += "\n{}".format(response['Message']) if 'Message' in response else ''
        utils.send_autodestruction_message(bot, update, job_queue, text)
        return
    utils.send_sending_photo_alert(bot, update) # so user knows the bot is running
    data = response['Data']
    cut_data = []
    for i in data:
        if interval == '1d' and i['time'] < (time.time() - 60*60*24):  # stats blocked 1 day
            continue
        if interval == '1w' and i['time'] < (time.time() - 60*60*24*7):  # stats blocked 1w
            continue
        cut_data.append(i)
    caption = "{} - USD. INTERVAL: {}".format(
        coin.upper(), 
        "1 day" if interval == '1d' else "1 week" if interval == '1w' else ''
    )
    pic = utils.build_graph(cut_data, title=caption)
    utils.send_autodestruction_photo(bot, update, pic, caption, job_queue, destruct_in=60, quote=False)
