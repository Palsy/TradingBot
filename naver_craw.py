# version 1.3.1
# *단위: 억원, %, 배, 주 * 분기: 순액기준
# 총 크롤링한 종목의 수 : select count(*) from (select * from naver group by code) a

import re
import datetime

import pandas as pd
import pymysql
import requests
from sqlalchemy.exc import ProgrammingError

pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from library import cf


class NoEncDataException(Exception):
    pass


class NAVERCrawl:
    def __init__(self):
        db_url = URL(
            drivername="mysql+mysqldb",
            username=cf.db_id,
            password=cf.db_passwd,
            host=cf.db_ip,
            port=cf.db_port,
            database='daily_buy_list'
        )
        self.db_engine = create_engine(db_url)

        # 모든 종목 코드 가져오기
        self.get_stock_item_all()

    def get_stock_item_all(self):
        sql = """
        SELECT code, code_name
        FROM stock_item_all
        WHERE code not in (
            SELECT code FROM stock_konex
        )
        ORDER BY code
        """  # Konex 제외 (기업현황 데이터 미제공)
        self.stock_item_all = self.db_engine.execute(sql).fetchall()

    def get_encparam(self, cmp_code):
        """
        Naver에서 만든 보안 절차를 뚫기 위해 키를 받아옴

        :param cmp_code: 종목 코드
        :return: encparam, id, enc_data_url
        """
        # 브라우저에 아래와같이 검색 시 크롤링 대상 사이트로 접속 가능(삼성전자)
        # http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=005930
        enc_data_url = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}'.format(cmp_code)
        enc_res = requests.get(enc_data_url)
        retry = 0
        while '접속장애' in enc_res.text and retry != 3:
            enc_res = requests.get(enc_data_url)
            retry += 1

        if retry == 3:
            print('접속장애가 발견되었습니다. 잠시 후 다시 시도하여 주시기 바랍니다.')
            return

        encparam_exp = "encparam: \\'(.*?)\\'"  # 정규식 패턴 encparam을 찾음
        id_exp = "id: \\'([a-zA-Z0-9]*)\\' \?"  # 정규식 패턴 id를 찾음

        try:
            encparam = re.search(encparam_exp, enc_res.text).groups(1)
            id = re.search(id_exp, enc_res.text).groups(1)
        except (IndexError, AttributeError) as e:
            raise NoEncDataException(f"Cannot find encparam or id! - {e}")

        return encparam, id, enc_data_url

    # 크롤링 함수
    def get_fin_info(self, cmp_code):

        try:
            encparam, id, enc_data_url = self.get_encparam(cmp_code)
        except NoEncDataException:
            print("해당 종목의 정보가 없습니다")
            return []
        fin_url = 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx'

        # dictionary 자료형 -> ex) year_fin_params = { .. }
        # 사전이라는 뜻.
        # '사과' : 'apple'
        # '주식' : 'stock'
        # 와 같이 딕셔너리는 Key(사과)와 Value(apple)를 한 쌍으로 갖는 자료형
        # header 의 query string parameter
        year_fin_params = {
            'cmp_cd': cmp_code,
            'fin_typ': 0,
            'freq_typ': 'Y',
            'encparam': encparam,
            'id': id
        }
        # dictionary 데이터 활용 방법
        # print(year_fin_params['cmp_cd'])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Referer': enc_data_url
        }

        res = requests.get(fin_url, year_fin_params, headers=headers)  # request
        try:
            return pd.read_html(res.text)[1]
        except Exception as e:
            return []


    def get_latest_index(self):
        """
         naver 테이블에서 가장 최근에 받은 종목의 index를 반환

         :return: latest_index
         """
        latest_year = datetime.datetime.now().year - 1

        try:
            latest_code = self.db_engine.execute("""
                        SELECT code FROM naver 
                        WHERE year = {}
                        ORDER BY code DESC LIMIT 1
                    """.format(latest_year)).first()[0]

            for i, (scode, _) in enumerate(self.stock_item_all):
                if scode == latest_code:
                    latest_index = i
        except ProgrammingError:  # 아직 한번도 데이터를 넣지 않아 테이블이 존재하지 않을 시
            latest_index = 0
        return latest_index

    def crawl(self):
        ##### 촬영 후 추가 코드 ##############################
        # 네이버 크롤링 최대 조회 장애(Max retries exceeded)
        # 등의 이유로 인해 프로그램이 꺼지게 되면 다시 돌릴 때 이미 받은 종목들은 skip 하기 위해 로직 추가
        num = len(self.stock_item_all)  # print 용 변수
        latest_index = self.get_latest_index()
        count = latest_index # print 용 변수
        ####################################################

        # self.stock_item_all[latest_index + 1:] : 가장 최근 받은 종목 이후로 시작
        for stock_code in self.stock_item_all[latest_index + 1:]:
            count += 1
            code = stock_code[0]
            code_name = stock_code[1]
            print("++++++++++++++ {} ++++++++++++++ {} / {}".format(code_name, count, num))


            df = self.get_fin_info(code)

            # 추가 내용 (비어있는지 체크, len(df)가 0이면 False-> not len(df) 는 True -> continue
            if not len(df):
                continue

            # 데이터 프레임에 code, code_name 컬럼을 추가하고 각각의 값을 넣어준다
            df['code'] = code
            df['code_name'] = code_name
            # year_df 에서 사용할 컬럼만을 짜른다.
            year_df = df[df.columns[1:-5]]

            # List comprehension
            years = [int(y.split('/')[0]) for _, y in year_df.columns if not y.startswith('Unnamed:')]

            # years = []
            # for _, y in year_df.columns:
            #     if not y.startswith('Unamed:'):
            #         years.append(int(y.split('/')[0]))

            new_df = pd.DataFrame(columns=['code', 'code_name', 'year', 'label', 'value'])
            for data in df.itertuples():
                for y, v in zip(years, data[2:7]):
                    try:
                        existing_rows = self.db_engine.execute("""
                            SELECT count(*) FROM naver
                            WHERE code = "{}" AND year = "{}" AND label = "{}"
                        """.format(data._10, y, data._1.replace("%", "%%"))).first()  # str.replace(from, to)
                        if existing_rows[0] != 0:
                            continue
                    except ProgrammingError:  # 아직 한번도 데이터를 넣지 않아 테이블이 존재하지 않을 시
                        pass

                    new_df.loc[len(new_df)] = (data._10, data._11, y, data._1, v)  # loc
                    print("입력 중.. {}".format(new_df.iloc[-1:].values))

            new_df.to_sql('naver', self.db_engine, if_exists='append', index=False)  # index False


if __name__ == "__main__":
    navercraw = NAVERCrawl()
    navercraw.crawl()
    print("naver 크롤링을 성공적으로 마쳤습니다.")
