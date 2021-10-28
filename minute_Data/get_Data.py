"""
get_Data.py
종목 리스트의 분 데이터를 수집하여 저장 <최대 2년>
"""
import win32com.client
import pandas as pd
import os
from datetime import datetime, timedelta
from time import sleep
from pykrx import stock
import json

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')

class CpStockDataRequest:
    def __init__(self):
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    def RequestMinuteData(self, code, date, caller):
        # 연결 여부 체크
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False
        self.objStockChart.SetInputValue(0, code)                   # 종목코드
        self.objStockChart.SetInputValue(1, ord('1'))               # 기간으로 받기
        self.objStockChart.SetInputValue(2, date)                   # To 날짜
        self.objStockChart.SetInputValue(3, date)                   # From 날짜
        self.objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, ord('m'))               # '차트 주기 - 분
        self.objStockChart.SetInputValue(7, 1)                      # 분틱차트 주기
        self.objStockChart.SetInputValue(9, ord('1'))               # 수정주가 사용 여부
        self.objStockChart.BlockRequest()

        rqStatus = self.objStockChart.GetDibStatus()
        rqRet = self.objStockChart.GetDibMsg1()
        if rqStatus != 0:
            exit()
        length = self.objStockChart.GetHeaderValue(3)
        caller.dates = []
        caller.times = []
        caller.opens = []
        caller.highs = []
        caller.lows = []
        caller.closes = []
        caller.vols = []
        for i in range(length):
            caller.dates.append(self.objStockChart.GetDataValue(0, i))
            caller.times.append(self.objStockChart.GetDataValue(1, i))
            caller.opens.append(self.objStockChart.GetDataValue(2, i))
            caller.highs.append(self.objStockChart.GetDataValue(3, i))
            caller.lows.append(self.objStockChart.GetDataValue(4, i))
            caller.closes.append(self.objStockChart.GetDataValue(5, i))
            caller.vols.append(self.objStockChart.GetDataValue(6, i))
        caller.dates.reverse()
        caller.times.reverse()
        caller.opens.reverse()
        caller.highs.reverse()
        caller.lows.reverse()
        caller.closes.reverse()
        caller.vols.reverse()
        caller.times = list(map('{:04d}'.format, caller.times))
        return

class StockDataController():
    def __init__(self):
        # Stock Info
        self.code = ''
        self.date = 0

        # Request Module
        self.CSDR = CpStockDataRequest()

        # OHLC Container
        self.dates = []
        self.times = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.vols = []

    # code 와 date 설정
    def set_code(self, code):
        self.code = code

    def set_date(self, date):
        self.date = date

    # code 주식 date 일자의 minute data를 self container에 저장
    def request_minute_data(self):
        if not self.code:
            print('code or date input error')
            return
        self.CSDR.RequestMinuteData(self.code, self.date, self)

    # 현재 self container의 data를 txt 파일로 저장
    def save_minute_data(self):
        # Incomplete File 배제
        # if len(self.dates) < 381:
        #     return
        # Dir 생성
        base_dir = 'C:/Git/Data/수정/minute_Data/'
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        code_dir = base_dir + '/' + self.code
        if not os.path.isdir(code_dir):
            os.mkdir(code_dir)
        file_name = code_dir + '/' + str(self.date) + '.json'
        data = {'time': self.times, 'price': self.closes, 'volumes': self.vols}
        df = pd.DataFrame(data=data)
        df.to_json(file_name, orient='table')

    # 해당 종목의 2년치 minute data를 json 파일로 저장
    def save_all_minute_data(self):
        ref_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
        past_date = datetime.strftime(datetime.now().date() - timedelta(days=731), "%Y%m%d")
        while True:
            try:
                dates_df = stock.get_index_ohlcv_by_date(past_date, ref_date, "1001")
                break
            except json.decoder.JSONDecodeError:
                pass
        dates_list = dates_df.index.to_list()
        for i, date in enumerate(dates_list):
            dates_list[i] = datetime.strftime(date, "%Y%m%d")
        for date in dates_list:
            self.set_date(date)
            self.request_minute_data()
            self.save_minute_data()
            # Creon Data 통신 제한
            if i % 50 == 0:
                sleep(20)

    # 해당 종목의 minute data update
    def update_all_minute_data(self):
        ref_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
        with open('last_update_date.txt', 'r') as f:
            last_update_date = f.readline()
        while True:
            try:
                dates_df = stock.get_index_ohlcv_by_date(last_update_date, ref_date, "1001")
                break
            except json.decoder.JSONDecodeError:
                pass
        dates_list = dates_df.index.to_list()
        for i, date in enumerate(dates_list):
            dates_list[i] = datetime.strftime(date, "%Y%m%d")
        for date in dates_list:
            self.set_date(date)
            self.request_minute_data()
            self.save_minute_data()
            # Creon Data 통신 제한
            if i % 50 == 0:
                sleep(20)

def get_code_list():
    """
    :return:
    오늘 기준 상장 기업 리스트
    """
    ref_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
    code_set = set([])
    tickers1 = stock.get_market_ticker_list(ref_date, market="KOSPI")
    code_set.update(tickers1)
    tickers2 = stock.get_market_ticker_list(ref_date, market="KOSDAQ")
    code_set.update(tickers2)
    return list(code_set)

def data_validation():
    report = []
    base_dir = 'C:/Git/Data/수정/minute_Data/'
    code_list = os.listdir(base_dir)
    for i in range(0, len(code_list)):
        code = code_list[i]
        code_dir = base_dir + code + '/'
        file_list = os.listdir(code_dir)
        file_list.reverse()
        start_date = file_list[-1].split('.')[0]
        end_date = file_list[0].split('.')[0]
        while True:
            try:
                temp = stock.get_market_ohlcv_by_date(start_date, end_date, code[1:])
                break
            except:
                pass
        dates_list = temp.index.to_list()
        dates_list.reverse()
        for j in range(len(dates_list)):
            dates_list[j] = datetime.strftime(dates_list[j], "%Y%m%d")
        discrepancy_flag = False
        for j in range(len(dates_list)):
            file_name = code_dir + dates_list[j] + '.json'
            df = pd.read_json(file_name, orient='table')
            if df.empty:
                continue
            if temp.loc[datetime.strptime(dates_list[j], "%Y%m%d")]['종가'] != df.iloc[-1]['price']:
                report.append((code[1:], dates_list[j-1]))
                discrepancy_flag = True
                break
        if not discrepancy_flag:
            report.append((code[1:], dates_list[-1]))
        print(code[1:] + ', 유효시작날짜: ' + report[-1][1])
        print('진행률: ' + str(round(i/(len(code_list)-1)*100, 2)) + '%')
    with open(base_dir + 'dates.json', 'w') as f:
        json.dump(report, f)

def delete_faulty_files():
    """
    :param date:
    :return:
    date (당일 미포함) 이전 data 모두 삭제
    """
    base_dir = 'C:/Git/Data/수정/minute_Data/'
    with open(base_dir + 'dates.json', 'r') as f:
        report = json.load(f)

    for i, item in enumerate(report):
        code = item[0]
        date = item[1]
        A_code = 'A' + code
        code_dir = base_dir + A_code + '/'
        file_list = os.listdir(code_dir)
        for j in range(len(file_list)):
            if file_list[j].split('.')[0] < date:
                file_name = code_dir + file_list[j]
                os.remove(file_name)
            else:
                break

"""
Execution Functions
"""
def save_all_data(begin_idx=0, renew_code_list=False):
    """
    :param begin_idx: 시작 idx
    :param renew_code_list: code list update 여부
    :return: 최근 2년치 분 데이터 저장
    """
    if renew_code_list:
        code_list = get_code_list()
        with open('krx_codes.json', 'w') as f:
            json.dump(code_list, f)

    sdc = StockDataController()
    with open('krx_codes.json', 'r') as f:
        code_list = json.load(f)

    for i in range(begin_idx, len(code_list)):
        code = code_list[i]
        A_code = 'A' + code
        sdc.set_code(A_code)
        sdc.save_all_minute_data()
        print('{}th code: {}'.format(i, code), '저장 완료', '(', str(round(i/(len(code_list)-1)*100, 2)), '%)')

    ref_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
    last_update_date = datetime.strftime(datetime.strptime(ref_date, "%Y%m%d") - timedelta(days=1), "%Y%m%d")
    with open('last_update_date.txt', 'w') as f:
        f.write(last_update_date)

    data_validation()
    delete_faulty_files()

def update_all_data(begin_idx, renew_code_list=False):
    """
    :param begin_idx: 시작 idx
    :param renew_code_list: code list update 여부
    :return: 모든 분 데이터 업데이트
    """
    if renew_code_list:
        code_list = get_code_list()
        with open('krx_codes.json', 'w') as f:
            json.dump(code_list, f)

    sdc = StockDataController()
    with open('krx_codes.json', 'r') as f:
        code_list = json.load(f)

    for i in range(begin_idx, len(code_list)):
        code = code_list[i]
        A_code = 'A' + code
        sdc.set_code(A_code)
        sdc.update_all_minute_data()
        print('{}th code: {}'.format(i, code), '저장 완료', '(', str(round(i/(len(code_list)-1)*100, 2)), '%)')

    ref_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
    last_update_date = datetime.strftime(datetime.strptime(ref_date, "%Y%m%d") - timedelta(days=1), "%Y%m%d")
    with open('last_update_date.txt', 'w') as f:
        f.write(last_update_date)

    data_validation()
    delete_faulty_files()


update_all_data(begin_idx=0, renew_code_list=True)