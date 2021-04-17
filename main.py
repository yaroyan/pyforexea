import logging
import sys
from threading import Thread

from app.controllers.streamdata import stream
from app.controllers.webserver import start
import app.models

from app.models.candle import factory_candle_class
from app.models.candle import create_candle_with_duration
from oanda.oanda import Ticker

import settings

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    # api_client = APIClient(settings.access_token, settings.account_id)
    # balance = api_client.get_balance()
    # ticker = api_client.get_ticker(settings.product_code)
    # print(balance.currency)
    # print(ticker.product_code)
    # print(ticker.truncate_date_time('5s'))
    # print(ticker.truncate_date_time(settings.trade_duration))
    # print(ticker.truncate_date_time('1h'))
    # print(ticker.mid_price)
    # print(ticker.volume)
    # api_client.get_realtime_ticker(None)
    # from functools import partial

    # def trade(ticker):
    #     print(ticker.mid_price)
    #     print(ticker.ask)
    #     print(ticker.bid)
    # callback = partial(trade)
    # api_client.get_realtime_ticker(callback)

    # order = Order(
    #     product_code=settings.product_code,
    #     side='BUY',
    #     units=1,
    # )

    # trade = api_client.send_order(order)
    # print(trade.trade_id)
    # print(trade.side)
    # print(trade.units)
    # print(trade.price)

    # trades = api_client.get_open_trade()
    # for t in trades:
    #     api_client.trade_close(t.trade_id)

    # streamThread = Thread(target=stream.stream_ingestion_data)
    serverThread = Thread(target=start)
    # streamThread.start()
    serverThread.start()
    # streamThread.join()
    serverThread.join()

    # import talib
    # import numpy as np
    # from app.models.dfcandle import DataFrameCandle
    # df = DataFrameCandle(settings.product_code,
    #                      settings.trade_duration)
    # df.set_all_candles(settings.past_period)
    # df.add_sma(7)
    # print(df.value)
    # values = talib.SMA(np.asarray(df.closes), 7)
    # print(values)
