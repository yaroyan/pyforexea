import logging

from sqlalchemy import Column
from sqlalchemy import desc
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy.exc import IntegrityError

from app.models.base import Base
from app.models.base import session_scope

import constants

logger = logging.getLogger(__name__)


class BaseCandleMixin(object):
    """
    ローソク足の基底クラスです。
    """
    time = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)

    @classmethod
    def create(cls, time, open, close, high, low, volume):
        """
        DBへローソク足を保存します。
        """
        candle = cls(time=time,
                     open=open,
                     close=close,
                     high=high,
                     low=low,
                     volume=volume)
        try:
            with session_scope() as session:
                session.add(candle)
            return candle
        except IntegrityError:
            return False

    @classmethod
    def get(cls, time):
        """
        DBからローソク足を取得します。
        """
        with session_scope() as session:
            candle = session.query(cls).filter(
                cls.time == time
            ).first()
        if candle is None:
            return None
        return candle

    def save(self):
        """
        DBのローソク足を更新します。
        """
        with session_scope() as session:
            session.add(self)

    @classmethod
    def get_all_candles(cls, limit=100):
        """
        DBから全てのローソク足を取得します。
        """
        with session_scope() as session:
            candles = session.query(cls).order_by(
                desc(cls.time)).limit(limit).all()

        if candles is None:
            return None

        candles.reverse()
        return candles

    @property
    def value(self):
        return {
            'time': self.time,
            'open': self.open,
            'close': self.close,
            'high': self.high,
            'low': self.low,
            'volume': self.volume,
        }


class UsdJpyCandle1H(BaseCandleMixin, Base):
    __tablename__ = 'USD_JPY_1H'


class UsdJpyCandle1M(BaseCandleMixin, Base):
    __tablename__ = 'USD_JPY_1M'


class UsdJpyCandle5S(BaseCandleMixin, Base):
    __tablename__ = 'USD_JPY_5S'


def factory_candle_class(product_code, duration):
    if product_code == constants.PRODUCT_CODE_USD_JPY:
        if duration == constants.DURATION_5S:
            return UsdJpyCandle5S
        if duration == constants.DURATION_1M:
            return UsdJpyCandle1M
        if duration == constants.DURATION_1H:
            return UsdJpyCandle1H


def create_candle_with_duration(product_code, duration, ticker):
    cls = factory_candle_class(product_code, duration)
    ticker_time = ticker.truncate_date_time(duration)
    current_candle = cls.get(ticker_time)
    price = ticker.mid_price
    # 1M 1:00:00 100
    #    1:00:00 110 => 1:00:00
    if current_candle is None:
        cls.create(ticker_time, price, price, price, price, ticker.volume)
        return True

    if current_candle.high <= price:
        current_candle.high = price
    elif current_candle.low >= price:
        current_candle.low = price
    current_candle.volume += ticker.volume
    current_candle.close = price
    current_candle.save()
    return False
