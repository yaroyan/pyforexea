import dateutil.parser
import pandas as pd
import pathlib
from datetime import datetime


def import_csv():
    src = pathlib.Path(__file__).resolve().parent / 'resources/axiory/USDJPY'
    paths = pathlib.Path(src).glob('*.csv')
    header = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
    df = pd.read_csv(list(paths)[0], header=None, names=header)
    df['time'] = df['date'] + ' ' + df['time']
    def formatter(x): return datetime.timestamp(dateutil.parser.parse(x))
    df['time'] = df['time'].apply(formatter)
    df.drop(columns=['date'], inplace=True)
    # paths = pathlib.Path()
    # df = pd.read_csv('./resources/axiory/USDJPY_2020_01.csv')
    # print(df)
    # hiduke = '2020.01.02 00:00'
    # hiduke = '2020.01.02 00:01'
    # print(dateutil.parser.parse(hiduke))


import_csv()
