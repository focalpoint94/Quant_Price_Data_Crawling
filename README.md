# Quant_Price_Data_Crawling
주식/ETF OHLCV 및 분 단위 데이터 수집

## ETF_minute_Data
### get_Data.py
'ETF_codes.json' ETF 리스트의 최근 2년치 분 단위 데이터를 수집하여 저장합니다.
아래 두 함수를 사용하여 신규로 데이터를 저장하거나, 데이터를 추가할 수 있습니다.
- save_all_data(begin_idx=0, renew_code_list=False)
```
'ETF_codes.json' ETF 리스트의 최근 2년치 분 단위 데이터를 수집하여 저장합니다.
begin_idx: ETF_codes.json 리스트의 idx를 의미합니다.
다운로드 중 인터넷 연결 불량 등의 이유로 비정상적으로 종료되었을 때, 다시 다운로드를 시작할 idx를 지정할 수 있습니다.
renew_code_list: ETF_codes.json을 현재 상장 ETF 리스트로 갱신 여부를 지정합니다. (True: 갱신)
```
- update_all_data(begin_idx, renew_code_list=False)
```
마지막 실행일로부터 최근까지의 데이터를 추가로 수집하여 저장합니다.
예컨대 2019년 01월 01일 ~ 2021년 01월 01일이 저장되어 있는 상태에서 2021년 10월 28일 위 함수를 실행하면,
2021년 01월 02일 ~ 2021년 10월 28일까지의 데이터가 추가로 저장됩니다.
```

## minute_Data
### get_Data.py
'krx_codes.json' 주식 종목 리스트의 최근 2년치 분 단위 데이터를 수집하여 저장합니다.
아래 두 함수를 사용하여 신규로 데이터를 저장하거나, 데이터를 추가할 수 있습니다.
- save_all_data(begin_idx=0, renew_code_list=False)
```
'krx_codes.json' 주식 종목 리스트의 최근 2년치 분 단위 데이터를 수집하여 저장합니다.
begin_idx: krx_codes.json 리스트의 idx를 의미합니다.
다운로드 중 인터넷 연결 불량 등의 이유로 비정상적으로 종료되었을 때, 다시 다운로드를 시작할 idx를 지정할 수 있습니다.
renew_code_list: krx_codes.json을 현재 상장 주식 종목 리스트로 갱신 여부를 지정합니다. (True: 갱신)
```
- update_all_data(begin_idx, renew_code_list=False)
```
마지막 실행일로부터 최근까지의 데이터를 추가로 수집하여 저장합니다.
예컨대 2019년 01월 01일 ~ 2021년 01월 01일이 저장되어 있는 상태에서 2021년 10월 28일 위 함수를 실행하면,
2021년 01월 02일 ~ 2021년 10월 28일까지의 데이터가 추가로 저장됩니다.
```

## OHLCV_Data
### get_data.py
주식/ETF/Index 혹은 전부의 OHLCV Data를 다운로드 받습니다.
- _get_Data(type, from_Date, to_Date=datetime.now().date().strftime("%Y%m%d"), begin_idx=0, save_dir)
```
type: 다운로드할 데이터를 'ALL', 'Stock', 'ETF', 'Index' 중 선택
from_Date: 시작 기준일
to_Date: 종료 기준일
begin_idx: 리스트의 idx
save_dir: 저장 경로
```

### load_data.py
OHLCV 데이터를 load하여 dataframe으로 반환합니다.
- _load_OHLCV_Data(code, from_Date, to_Date, ohlcv_dir)
```
code: 종목 코드
from_Date: 시작 기준일
to_Date: 종료 기준일
ohlcv_dir: 저장 경로
```

## AutoConnect.py
ETF 및 주식 분 데이터를 수집하기 위해 크레온 프로그램에 로그인하는 코드입니다.

## Data_Example.7z
ETF 및 주식 분 데이터, OHLCV 데이터 다운로드 예시 파일입니다.
