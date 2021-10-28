"""
load_Data.py
"""
from pykrx import stock
import json
import pandas as pd
import time
from datetime import datetime
import os

def _load_OHLCV_Data(code, from_Date, to_Date, ohlcv_dir='C:/Git/Data/수정/OHLCV/'):
    """
    :param code: '005930'
    :param from_Date: '20160101'
    :param to_Date: '20210727'
    :param ohlcv_dir: 'C:/Git/Data/수정/'
    :return:
    dataframe
    """
    from_Date = datetime.strptime(from_Date, "%Y%m%d")
    to_Date = datetime.strptime(to_Date, "%Y%m%d")

    with open('Stock_codes_with_names.json', 'r') as f:
        stock_list = json.load(f)
    with open('ETF_codes_with_names.json', 'r') as f:
        ETF_list = json.load(f)
    with open('Index_codes_with_names.json', 'r') as f:
        index_list = json.load(f)
    stock_list = [x[0] for x in stock_list]
    ETF_list = [x[0] for x in ETF_list]
    index_list = [x[0] for x in index_list]
    if code in stock_list:
        data_dir = ohlcv_dir + 'Stock/'
    elif code in ETF_list:
        data_dir = ohlcv_dir + 'ETF/'
    elif code in index_list:
        data_dir = ohlcv_dir + 'Index/'
    else:
        return pd.DataFrame()

    file_name = data_dir + code + '.xlsx'
    if not os.path.isfile(file_name):
        return pd.DataFrame()

    df = pd.read_excel(file_name, index_col=0, engine='openpyxl')
    new_index_list = []
    for index in df.index:
        new_index_list.append(datetime.strptime(str(index), "%Y%m%d"))
    df.index = new_index_list
    return df[(df.index >= from_Date) & (df.index <= to_Date)]



