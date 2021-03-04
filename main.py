import datetime
import logging
import sys

from oanda.oanda import APIClient
from oanda.oanda import Order

from app.models.candle import UsdJpyCandle1M
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

    import app.models
    now1 = datetime.datetime(2020, 1, 2, 3, 4, 5)
    UsdJpyCandle1M.create(now1, 1.0, 2.0, 3.0, 4.0, 5)
    candle = UsdJpyCandle1M.get(now1)
    print(candle.open)
    candle.open = 100.0
    candle.save()
    updated_candle = UsdJpyCandle1M.get(now1)
    print(updated_candle.open)
