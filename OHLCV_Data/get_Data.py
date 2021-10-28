"""
get_Data.py
"""
from pykrx import stock
import json
import pandas as pd
import time
from datetime import datetime
import os

def _get_codes():
    stock_list = []
    for ticker in stock.get_market_ticker_list(market='KOSPI'):
        stock_list.append((ticker, stock.get_market_ticker_name(ticker)))
    for ticker in stock.get_market_ticker_list(market='KOSDAQ'):
        stock_list.append((ticker, stock.get_market_ticker_name(ticker)))
    with open('Stock_codes_with_names.json', 'w') as f:
        json.dump(stock_list, f)

    ETF_list = []
    for ticker in stock.get_etf_ticker_list():
        ETF_list.append((ticker, stock.get_etf_ticker_name(ticker)))
    with open('ETF_codes_with_names.json', 'w') as f:
        json.dump(ETF_list, f)

    index_list = []
    for ticker in stock.get_index_ticker_list():
        index_list.append((ticker, stock.get_index_ticker_name(ticker)))
    for ticker in stock.get_index_ticker_list(market="KOSDAQ"):
        index_list.append((ticker, stock.get_index_ticker_name(ticker)))
    with open('Index_codes_with_names.json', 'w') as f:
        json.dump(index_list, f)

def _get_Data(type, from_Date, to_Date=datetime.now().date().strftime("%Y%m%d"), begin_idx=0, save_dir='C:/Git/Data/수정/OHLCV/'):
    """
    :param type: 'ALL', 'Stock', 'ETF', 'Index'
    :param from_Date: '20170101'
    :param to_Date: '20210730'
    :param begin_idx: 0
    :param save_dir: 'C:/Git/Data/수정/'
    :return:
    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    if type == 'ALL':
        stock_dir = save_dir + 'Stock/'
        if not os.path.isdir(stock_dir):
            os.mkdir(stock_dir)
        with open('Stock_codes_with_names.json', 'r') as f:
            stock_list = json.load(f)
        print('Downloading Stock Data...')
        for i in range(begin_idx, len(stock_list)):
            _stock = stock_list[i]
            start_time = time.time()
            while True:
                try:
                    temp_df = stock.get_market_ohlcv_by_date(from_Date, to_Date, _stock[0])
                    new_index_list = []
                    for j in range(len(temp_df)):
                        new_index_list.append(temp_df.index[j].strftime("%Y%m%d"))
                    temp_df.index = new_index_list
                    break
                except json.decoder.JSONDecodeError:
                    pass
            fname = stock_dir + _stock[0] + '.xlsx'
            writer = pd.ExcelWriter(fname, engine='xlsxwriter')
            temp_df.to_excel(writer)
            writer.close()
            print(str(i) + 'th Data Download Complete. (' + str(round(i / (len(stock_list) - 1) * 100, 2)) + '%)')
            # print("* 소요 시간: " + str(round(time.time() - start_time, 2)) + "초")

        ETF_dir = save_dir + 'ETF/'
        if not os.path.isdir(ETF_dir):
            os.mkdir(ETF_dir)
        with open('ETF_codes_with_names.json', 'r') as f:
            ETF_list = json.load(f)
        print('Downloading ETF Data...')
        for i in range(begin_idx, len(ETF_list)):
            ETF = ETF_list[i]
            start_time = time.time()
            valueError_flag = False
            while True:
                try:
                    temp_df = stock.get_etf_ohlcv_by_date(from_Date, to_Date, ETF[0])
                    new_index_list = []
                    for j in range(len(temp_df)):
                        new_index_list.append(temp_df.index[j].strftime("%Y%m%d"))
                    temp_df.index = new_index_list
                    break
                except json.decoder.JSONDecodeError:
                    pass
                except ValueError:
                    valueError_flag = True
                    break
            if valueError_flag:
                continue
            fname = ETF_dir + ETF[0] + '.xlsx'
            writer = pd.ExcelWriter(fname, engine='xlsxwriter')
            temp_df.to_excel(writer)
            writer.close()
            print(str(i) + 'th Data Download Complete. (' + str(round(i / (len(ETF_list) - 1) * 100, 2)) + '%)')
            # print("* 소요 시간: " + str(round(time.time() - start_time, 2)) + "초")

        index_dir = save_dir + 'Index/'
        if not os.path.isdir(index_dir):
            os.mkdir(index_dir)
        with open('Index_codes_with_names.json', 'r') as f:
            index_list = json.load(f)
        print('Downloading Index Data...')
        for i in range(begin_idx, len(index_list)):
            index = index_list[i]
            start_time = time.time()
            while True:
                try:
                    temp_df = stock.get_index_ohlcv_by_date(from_Date, to_Date, index[0])
                    new_index_list = []
                    for j in range(len(temp_df)):
                        new_index_list.append(temp_df.index[j].strftime("%Y%m%d"))
                    temp_df.index = new_index_list
                    break
                except json.decoder.JSONDecodeError:
                    pass
            fname = index_dir + index[0] + '.xlsx'
            writer = pd.ExcelWriter(fname, engine='xlsxwriter')
            temp_df.to_excel(writer)
            writer.close()
            print(str(i) + 'th Data Download Complete. (' + str(round(i/(len(index_list)-1)*100, 2)) + '%)')
            # print("* 소요 시간: " + str(round(time.time() - start_time, 2)) + "초")

    elif type == 'Stock':
        stock_dir = save_dir + 'Stock/'
        if not os.path.isdir(stock_dir):
            os.mkdir(stock_dir)
        with open('Stock_codes_with_names.json', 'r') as f:
            stock_list = json.load(f)
        print('Downloading Stock Data...')
        for i in range(begin_idx, len(stock_list)):
            _stock = stock_list[i]
            start_time = time.time()
            while True:
                try:
                    temp_df = stock.get_market_ohlcv_by_date(from_Date, to_Date, _stock[0])
                    new_index_list = []
                    for j in range(len(temp_df)):
                        new_index_list.append(temp_df.index[j].strftime("%Y%m%d"))
                    temp_df.index = new_index_list
                    break
                except json.decoder.JSONDecodeError:
                    pass
            fname = stock_dir + _stock[0] + '.xlsx'
            writer = pd.ExcelWriter(fname, engine='xlsxwriter')
            temp_df.to_excel(writer)
            writer.close()
            print(str(i) + 'th Data Download Complete. (' + str(round(i / (len(stock_list) - 1) * 100, 2)) + '%)')
            # print("* 소요 시간: " + str(round(time.time() - start_time, 2)) + "초")

    elif type == 'ETF':
        ETF_dir = save_dir + 'ETF/'
        if not os.path.isdir(ETF_dir):
            os.mkdir(ETF_dir)
        with open('ETF_codes_with_names.json', 'r') as f:
            ETF_list = json.load(f)
        print('Downloading ETF Data...')
        for i in range(begin_idx, len(ETF_list)):
            ETF = ETF_list[i]
            start_time = time.time()
            valueError_flag = False
            while True:
                try:
                    temp_df = stock.get_etf_ohlcv_by_date(from_Date, to_Date, ETF[0])
                    new_index_list = []
                    for j in range(len(temp_df)):
                        new_index_list.append(temp_df.index[j].strftime("%Y%m%d"))
                    temp_df.index = new_index_list
                    break
                except json.decoder.JSONDecodeError:
                    pass
                except ValueError:
                    valueError_flag = True
                    break
            if valueError_flag:
                continue
            fname = ETF_dir + ETF[0] + '.xlsx'
            writer = pd.ExcelWriter(fname, engine='xlsxwriter')
            temp_df.to_excel(writer)
            writer.close()
            print(str(i) + 'th Data Download Complete. (' + str(round(i / (len(ETF_list) - 1) * 100, 2)) + '%)')
            # print("* 소요 시간: " + str(round(time.time() - start_time, 2)) + "초")

    elif type == 'Index':
        index_dir = save_dir + 'Index/'
        if not os.path.isdir(index_dir):
            os.mkdir(index_dir)
        with open('Index_codes_with_names.json', 'r') as f:
            index_list = json.load(f)
        print('Downloading Index Data...')
        for i in range(begin_idx, len(index_list)):
            index = index_list[i]
            start_time = time.time()
            while True:
                try:
                    temp_df = stock.get_index_ohlcv_by_date(from_Date, to_Date, index[0])
                    new_index_list = []
                    for j in range(len(temp_df)):
                        new_index_list.append(temp_df.index[j].strftime("%Y%m%d"))
                    temp_df.index = new_index_list
                    break
                except json.decoder.JSONDecodeError:
                    pass
            fname = index_dir + index[0] + '.xlsx'
            writer = pd.ExcelWriter(fname, engine='xlsxwriter')
            temp_df.to_excel(writer)
            writer.close()
            print(str(i) + 'th Data Download Complete. (' + str(round(i/(len(index_list)-1)*100, 2)) + '%)')
            print("* 소요 시간: " + str(round(time.time() - start_time, 2)) + "초")

    else:
        print('Type Error: Type should be \'Stock\' or \'ETF\' or \'Index\'. ')
        return

_get_Data(type='Index', from_Date='20160101', begin_idx=0)


