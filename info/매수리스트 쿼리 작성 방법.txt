
# 관리종목 code_name !='' : code_name 이 비어있는 종목은 상장폐지 종목
select * from stock_managing where code_name !='';
# 불성실공시법인종목
select * from stock_insincerity where code_name !='';



# 아래 쿼리에서 날짜를 금일 날짜로 변경 후 조회 후 영웅문에서 해당 종목 리스트를 조회 해보면
# 위험종목 -> "위"  / 경고종목 -> "경" / 주의종목 -> "주" 라고 기재 되어 있다
# (주의 종목 리스트 중 "경"이라고 명시 된 것도 있고, 경고 종목 리스트 중 "주" 이라고 명시 된 것도 있다.)


# 투자 주의 종목
# > 최근 3달 이내의 투자 주의 종목 조회 ('투자경고 지정해제' 제외)
# DATE_SUB(20200626, INTERVAL 3 MONTH ) -> 2020-03-26 (3개월 전)
# 확인 방법 :
# select DATE_SUB(20200626, INTERVAL 3 MONTH )
# 3 대신 다른 숫자 가능 , MONTH 대신 YEAR(년), DAY(일) 가능
# Date() -> 스트링을 date type으로 변환
select * from stock_invest_caution
where DATE_SUB(20200203, INTERVAL 3 MONTH ) < post_date and post_date < Date(20200203) and type != '투자경고 지정해제' group by code;

# 투자 경고 종목
# cleared_date is null : 날짜를 오늘로 지정 했을 때 아직 해지일(cleard_date)가 없는 경우가 있기 때문에 설정
# test를 방법 : ctrl+shift+r-> scope -> current file -> 20200203을 오늘날짜로 모두 변경 후 테스트
select * from stock_invest_warning
where post_date <= DATE(20200203)
  and (cleared_date > DATE(20200203) or cleared_date is null)
group by code;

# 투자 위험 종목
select * from stock_invest_danger
where post_date <= DATE(20200203)
  and (cleared_date > DATE(20200203) or cleared_date is null)
group by code;


# 매수 알고리즘 쿼리문 만들기
# 1단계. daily_buy_list db에서 특정 날짜를 선택 한다.
select * from `20200203`;

# 2단계. 조건을 하나씩 넣는다.
# 2-1단계: 매수 조건 넣기 (5 / 20 골든크로스 buy)
select * from `20200203`
where yes_clo20 > yes_clo5 and clo5 > clo20;



# 2-2단계: konex는 사지 않겠다.
# (두가지 쿼리 결과는 동일하지만, NOT exists 방식이 성능이 더 좋아서 선택


# not in
select * from `20200203` a
where yes_clo20 > yes_clo5 and clo5 > clo20
and a.code not in (select code from stock_konex b);

# NOT exists
select * from `20200203` a
where yes_clo20 > yes_clo5 and clo5 > clo20
and NOT exists (select null from stock_konex b where a.code=b.code);



# 2-3단계) 관리, 불성실, 주의, 경고, 위험 제외
select * from `20200203` a
where yes_clo20 > yes_clo5 and clo5 > clo20
and NOT exists (select null from stock_konex b where a.code=b.code)
and NOT exists (select null from stock_managing c where a.code=c.code and c.code_name != '' group by c.code)
and NOT exists (select null from stock_insincerity d where a.code=d.code and d.code_name !='' group by d.code)
and NOT exists (select null from stock_invest_caution e where a.code=e.code and DATE_SUB(20200203, INTERVAL 3 MONTH ) < e.post_date and e.post_date < Date(20200203) and e.type != '투자경고 지정해제' group by e.code)
and NOT exists (select null from stock_invest_warning f where a.code=f.code and f.post_date <= DATE(20200203) and (f.cleared_date > DATE(20200203) or f.cleared_date is null) group by f.code)
and NOT exists (select null from stock_invest_danger g where a.code=g.code and g.post_date <= DATE(20200203) and (g.cleared_date > DATE(20200203) or g.cleared_date is null) group by g.code);

# 2-4단계) 종가가 invest_unit 보다 작은 것들만 가져온다, (한 주의 종가가 invest_unit(종목당 투자금액) 보다 크면 매수 자체가 불가하기 떄문
# 아래 예제는 invest_unit이 5만원 일경우
select * from `20200203` a
where yes_clo20 > yes_clo5 and clo5 > clo20
and NOT exists (select null from stock_konex b where a.code=b.code)
and NOT exists (select null from stock_managing c where a.code=c.code and c.code_name != '' group by c.code)
and NOT exists (select null from stock_insincerity d where a.code=d.code and d.code_name !='' group by d.code)
and NOT exists (select null from stock_invest_caution e where a.code=e.code and DATE_SUB(20200203, INTERVAL 3 MONTH ) < e.post_date and e.post_date < Date(20200203) and e.type != '투자경고 지정해제' group by e.code)
and NOT exists (select null from stock_invest_warning f where a.code=f.code and f.post_date <= DATE(20200203) and (f.cleared_date > DATE(20200203) or f.cleared_date is null) group by f.code)
and NOT exists (select null from stock_invest_danger g where a.code=g.code and g.post_date <= DATE(20200203) and (g.cleared_date > DATE(20200203) or g.cleared_date is null) group by g.code)
and a.close < 50000;


# 3단계
# db_to_realtime_daily_buy_list 함수에 적용한다.
# 위 예제의 숫자, 날짜 중 가변적인 것들을 %s로 지정 하면 된다. / format, {} 이용가능












# 매수 알고리즘
#         elif self.db_to_realtime_daily_buy_list_num == 4:
#             sql = "select * from `" + date_rows_yesterday + "` a " \
#                     "where yes_clo20 > yes_clo5 and clo5 > clo20 " \
#                     "and NOT exists (select null from stock_konex b where a.code=b.code)" \
#                     "and NOT exists (select null from stock_managing c where a.code=c.code and c.code_name != '' group by c.code) " \
#                     "and NOT exists (select null from stock_insincerity d where a.code=d.code and d.code_name !='' group by d.code) " \
#                     "and NOT exists (select null from stock_invest_caution e where a.code=e.code and DATE_SUB('%s', INTERVAL '%s' MONTH ) < e.post_date and e.post_date < Date('%s') and e.type != '투자경고 지정해제' group by e.code)"\
#                     "and NOT exists (select null from stock_invest_warning f where a.code=f.code and f.post_date <= DATE('%s') and (f.cleared_date > DATE('%s') or f.cleared_date is null) group by f.code)"\
#                     "and NOT exists (select null from stock_invest_danger g where a.code=g.code and g.post_date <= DATE('%s') and (g.cleared_date > DATE('%s') or g.cleared_date is null) group by g.code)"\
#                     "and a.close < '%s'"
#
#             realtime_daily_buy_list = self.engine_daily_buy_list.execute(sql % (date_rows_yesterday, self.interval_month, date_rows_yesterday,date_rows_yesterday ,date_rows_yesterday,date_rows_yesterday,date_rows_yesterday, self.invest_unit)).fetchall()
#
#
#
#
#
# # 변수 설정 함수
#         if self.simul_num == 1 or self.simul_num == 4:
#             # 시뮬레이팅 시작 일자
#             self.simul_start_date = "20190101"
#
#             ######### 알고리즘 선택 #############
#             # 매수 리스트 설정 알고리즘 번호
#             self.db_to_realtime_daily_buy_list_num = 1
#
#             # 매도 리스트 설정 알고리즘 번호
#             self.sell_list_num = 1
#             ###################################
#
#             # 초기 투자자금
#             self.start_invest_price = 10000000
#
#             # 매수 금액
#             self.invest_unit = 1000000
#
#             # 자산 중 최소로 남겨 둘 금액
#             self.limit_money = 3000000
#
#             # 익절 수익률 기준치
#             self.sell_point = 10
#
#             # 손절 수익률 기준치
#             self.losscut_point = -2
#
#             # 실전/모의 봇 돌릴 때 매수하는 순간 종목의 최신 종가 보다 1% 이상 오른 경우 사지 않도록 하는 설정(변경 가능)
#             self.invest_limit_rate = 1.01
#             # 실전/모의 봇 돌릴 때 매수하는 순간 종목의 최신 종가 보다 -2% 이하로 떨어진 경우 사지 않도록 하는 설정(변경 가능)
#             self.invest_min_limit_rate = 0.98
#
#             if self.simul_num == 4:
#                 self.db_to_realtime_daily_buy_list_num = 4
#                 self.interval_month = 3
#                 self.invest_unit = 50000
