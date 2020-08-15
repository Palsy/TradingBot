import datetime
import math
import multiprocessing
import time
from functools import partial

import pandas as pd
import pymysql.cursors
from sqlalchemy import Integer, event, create_engine

from library import cf
from library.open_api import escape_percentage

pymysql.install_as_MySQLdb()

# cpu 수
max_core_count = multiprocessing.cpu_count()

engine_daily_buy_list = create_engine(
    "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/daily_buy_list",
    encoding='utf8')
event.listen(engine_daily_buy_list, 'before_execute', escape_percentage, retval=True)

sql = "SELECT code_name,code FROM stock_item_all STOCK_ALL " \
      "WHERE (exists (SELECT null FROM stock_kospi KOSPI WHERE STOCK_ALL.code=KOSPI.code) "\
        "OR exists (SELECT null FROM stock_kosdaq KOSDAQ WHERE STOCK_ALL.code=KOSDAQ.code)) "

code_df_all = engine_daily_buy_list.execute(sql).fetchall()

# crawl_set 만드는 함수.
def crawl_node_setting():
    add_value = math.ceil(len(code_df_all) / max_core_count)
    print("add_value: " + str(add_value))
    crawl_set = []
    start = 0
    for i in range(max_core_count):
        node_num = i + 1
        if i == max_core_count - 1:
            # (index 시작점, index 끝, 프로세스 번호)
            crawl_set.append((start, len(code_df_all), node_num))
        else:
            crawl_set.append((start, start + add_value, node_num))
        start += add_value
    return crawl_set


def crawling_data(node_range, today_min_date):
    data_list = []
    node_start, node_end, node_num = node_range[0], node_range[1], node_range[2]

    print("node number: " + str(node_num))
    print("node_start, node_end ! ", node_start, node_end)

    for i in range(node_start, node_end):
        code = code_df_all[i][1]
        code_name = code_df_all[i][0]
        # 아래 print를 없애면 크롤링 속도가 좀 더 빨라집니다.
        print(f"{i} 번 종목 크롤링: {code_name}")

        url = f'http://finance.naver.com/item/sise_day.nhn?code={code}&page=1'
        df = pd.read_html(url, header=0)[0]

        # df.dropna()를 이용해 결측값(nan) 있는 행 제거
        df = df.dropna()
        # 제일 위에 행 하나만 추출(최근 일자)
        df = df.head(1)
        # 한글로 된 컬럼명을 영어로 바꿔줌
        df = df.rename(columns={
            '날짜': 'date',
            '종가': 'close',
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '거래량': 'volume'
        })

        df['date'] = today_min_date
        df = df.drop(columns="전일비")
        df['code'] = code
        df['code_name'] = code_name
        # 거래 정지 종목들을 삭제
        df = df[df.open != 0]

        if not df.empty:
            data_list.append(df)

    multi_list = pd.concat(data_list, ignore_index=True)
    print(f"{node_num} 노드의 multi_list 길이 : {len(multi_list)}")

    multi_list.to_sql(
        name='naver_min_crawl',
        con=engine_daily_buy_list,
        if_exists='append',
        index=False,
        dtype={
            'close': Integer(),
            'open': Integer(),
            'high': Integer(),
            'low': Integer(),
            'volume': Integer()
        }
    )


def run_crawl(today_min_date):
    start_time = time.time()
    # 프로세스 하나로 테스트 하는 경우
    # 176초
    # crawling_data((0, len(code_df_all), 1), today_min_date)


    # # 멀티 프로세싱 Pool 사용
    print("max_core_count : ", max_core_count)
    crawl_set = crawl_node_setting()
    print("crawl_set : ", crawl_set)

    with multiprocessing.Pool(processes=max_core_count) as pool:
        pool.map(partial(crawling_data, today_min_date=today_min_date), crawl_set)



    print(f"--- {time.time() - start_time} seconds ---")


if __name__ == '__main__':
    print("__name__", __name__)
    today_min_date = datetime.datetime.today().strftime("%Y%m%d%H%M")
    print(f"today_min_date : {today_min_date}")
    run_crawl(today_min_date)
