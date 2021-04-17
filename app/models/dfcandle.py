import numpy as np
import talib
from utils.utils import Serializer

from app.models.candle import factory_candle_class

import settings


def nan_to_zero(values: np.asarray):
    values[np.isnan(values)] = 0
    return values


def empty_to_none(input_list):
    if not input_list:
        return None
    return input_list


class Sma(Serializer):
    def __init__(self, period: int, values: list):
        self.period = period
        self.values = values


class DataFrameCandle(object):

    def __init__(self, product_code=settings.product_code, duration=settings.trade_duration):
        self.product_code = product_code
        self.duration = duration
        self.candle_cls = factory_candle_class(
            self.product_code, self.duration)
        self.candles = []
        self.smas = []

    def set_all_candles(self, limit=1000):
        self.candles = self.candle_cls.get_all_candles(limit)
        return self.candles

    @property
    def value(self):
        return {
            'product_code': self.product_code,
            'duration': self.duration,
            'candles': [c.value for c in self.candles],
            'smas': empty_to_none([s.value for s in self.smas]),
        }

    @property
    def opens(self):
        values = [candle.open for candle in self.candles]
        return values

    @property
    def closes(self):
        values = [candle.close for candle in self.candles]
        return values

    @property
    def highs(self):
        values = [candle.high for candle in self.candles]
        return values

    @property
    def lows(self):
        values = [candle.low for candle in self.candles]
        return values

    @property
    def volums(self):
        values = [candle.volume for candle in self.candles]
        return values

    def add_sma(self, period: int):

        if len(self.closes) > period:
            values = talib.SMA(np.asarray(self.closes), period)
            sma = Sma(period,
                      nan_to_zero(values).tolist())
            self.smas.append(sma)
            return True
        return False
