from cmath import inf
from binance.client import Client
from binance.enums import *
from math import ceil, floor, log
from binance import AsyncClient, BinanceSocketManager
from telebot import TeleBot, types
import asyncio
import os
from decimal import Decimal
import sys

channel = '' # telegram 
api_key = "" # binance
api_secret = "" # binance
telegrambottoken=''
symbols = []
stepSize = {}

proc = 1

client = None#Client(api_key, api_secret)
bot = TeleBot(telegrambottoken)
ioloop = asyncio.get_event_loop()

async def sendmsg(msg):
    bot.send_message(channel, msg)

async def float_round(num, places = 0, direction = floor):
    return direction(num * (10**places)) / float(10**places)

async def get_tickers():
    global stepSize
    exchange = await client.get_exchange_info()
    # print(exchange)
    rows = []
    for e in exchange['symbols']:
        if 'USDT' in e['symbol']:
            print(e['symbol'], e['filters'][2]['stepSize'])
            stepSize[e['symbol']] = e['filters'][2]['stepSize']
    return stepSize

async def convertor(s):
    try :
        int(s.rstrip('0').rstrip('.'))
        return 0
    except: 
        return len(str(float(s)).split('.')[-1])


async def logarifm():
    adx = await get_tickers()
    print(adx)
    loggg = {}
    
    for key, value in adx.items():
        logg = log(float(value), 10)
        loggg[key] = value
    return loggg



async def create_stop(symbol, price, quantity):
    print(price)
    global client
    if not client:
        client = await AsyncClient.create(api_key, api_secret)
    try:
        print(symbol, price, quantity)
        await client.create_order(
            symbol = symbol, 
            side = SIDE_SELL,
            type = ORDER_TYPE_STOP_LOSS_LIMIT,
            timeInForce = TIME_IN_FORCE_GTC, 
            quantity = quantity,
            price = '{}'.format(price), 
            stopPrice = price)
        print("CREATED!")
        await sendmsg(msg="Stop loss created for: {}    with price: {}                                     in quantity: {} coins!".format(symbol, price, quantity))
            # print("no bal")
    except Exception as e:
        print(e)

async def status():
    global client

    if not client:
        aclient = await AsyncClient.create(api_key, api_secret)
    while True:
        try:
            status = await aclient.get_system_status()
            # print(dir(status))
            if not status:
                print('kjsdf')
                ioloop.close()
        except Exception as e:
            print('BREAK')
            os.system('killall python3')
            sys.exit()

        await asyncio.sleep(10)
async def main():
    global client
    if not client:
        client = await AsyncClient.create(api_key, api_secret)
    bm = BinanceSocketManager(client)
    ts = bm.user_socket()
    async with ts as tscm:
        print("OK!")
        await logarifm()
        while True:
            res = await tscm.recv() 
            print(res)
            if res['e'] == 'executionReport':
                if res['S'] == 'BUY':
                    if res['X'] == 'FILLED':
                        procent = float(res['L']) / 100
                        stopprice = float(float(res['L']) - procent*proc)   
                        # print(symbol=res['s'], price='{0:.8f}'.format(stopprice), quantity=float(res['q']))
                        try:
                            commission = float(res['q'])*0.997
                            await create_stop(symbol=res['s'], price='{0:.8f}'.format(stopprice), quantity='{:.{}f}'.format(commission, await logarifm()))
                        except Exception as e:
                            print(e)


    await client.close_connection()

tasks = [
    ioloop.create_task(main()),
    ioloop.create_task(status())
]
ioloop.run_until_complete(asyncio.wait(tasks))
asyncio.set_event_loop(ioloop)