import sys
import logging

logger = logging.getLogger(__name__)
is_64bits = sys.maxsize > 2**32
if not is_64bits:
    logger.critical('64bit 환경으로 실행해 주시기 바랍니다.')
    exit(1)

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Normalization
# 딥러닝 모델이 학습을 잘하기 위해서는 정규화 해주는 작업이 필요. sklearn 패키지에 있는 MinMaxScaler를 활용하여 전체 학습 데이터를 Normalize
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# keras는 텐서플로우를 돌리기 쉽게 도와주는 라이브러리

from keras.models import Sequential
# layers는 모델을 구성하는 층, 신경망
from keras.layers import Dense, LSTM, BatchNormalization
from library import cf

# daily_craw, min_craw 모두 선택 가능
conn = pymysql.connect(host=cf.db_ip,
                       port=int(cf.db_port),
                       user=cf.db_id,
                       password=cf.db_passwd,
                       db='daily_craw',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

FEATURE_COLUMNS = ["date","close", "volume", "open", "high", "low"]
code_name = '삼성전자'
until = '20200712'
sql = """
    SELECT {} FROM `{}`
    WHERE STR_TO_DATE(date, '%Y%m%d%H%i') <= '{}'
""".format(','.join(FEATURE_COLUMNS), code_name, until)

df = pd.read_sql(sql, conn)
if not len(df):
    print(f'{code_name}의 {until}까지 데이터가 존재하지 않습니다.')
    exit(1)


print(df)

plt.plot(df['volume'])
plt.show()

plt.plot(df['close'])
plt.show()

df_temp = df[['volume', 'close']].values

# 정규화 (0과 1사이 값으로 변환)
# 0,1 범위?
# MinMaxScaler를 해주면 전체 데이터는 0, 1사이의 값을 갖도록 해줍니다.
scaler = MinMaxScaler()
sc_df = scaler.fit_transform(df_temp)

N_STEPS = 5 # 시퀀스 데이터를 몇개씩 담을지 설정.
            # 5개씩 데이터를 넣겠다(lstm은 시퀀스 데이터를 다루는 모델이라 여러개의 값을 넣는것 )

X=[]
y=[]
# X에는 0~4까지 담고, 1~5까지 담고 ... => 시퀀스
# y에는 5 번째 close, 6번째 close ....
# 시퀀스(Sequence) : 시퀀스란 데이터를 순서대로 하나씩 나열하여 나타낸 데이터 구조
for i in range(len(sc_df) - N_STEPS):
    # 시퀀스 데이터(문제지)
    X.append(sc_df[i:i+N_STEPS])
    # 결과값(정답지)
    y.append(sc_df[i+N_STEPS,[1]])


X= np.array(X)
y= np.array(y)


# test_size=0.2: 일부분만 train 데이터로 사용하고 나머지를 test데이터로 사용하겠다는 뜻
# train_size:80% / test_size를 20%
# shuffle = False : 시퀀스 데이터의 순서를 섞지 않겠다.

# len(X)*0.2  /  len(X_test) 비교
X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=0.2, shuffle=False)

# X_train.shape => [9092, 5, 2]
# 9092: row(9092일치 데이터), 5: N_STEPS, 2: 속성(volume, close)
# y_train.shape => [9092, 1]
# 9092: row(9092일치 데이터), 1: 속성(close)


# #시퀀스를 섞고 train_size:80% / test_size를 20%
# X_train_temp2, X_test_temp2, y_train_temp2, y_test_temp2 = \
#         train_test_split(X, y, test_size=0.2, shuffle=True)




# 층층이 차례대로 쌓겠다/ # Sequential 순서대로 layer을 쌓는 모델
model = Sequential()
# sequential이니까 순차적으로 쌓인다


# LSTM 활용하기 위해서는 3차원 데이터가 필요
# [data_size, time_steps, features] 3차원 array로 구성
# data_size : 데이터가 몇 개 인지
# time_steps : 한 묶음에 몇 개의 데이터가 있는지
# features : 속성(컬럼)의 수 (차원)
# data_size 는 생략해도 input_shape에서 자동으로 계산해줌
model.add(LSTM(units=32 ,input_shape=X_train.shape[1:]))
# Dense : 출력층 값이 1개가 나온다. 우리가 예측한 주가, 이것을 통해서 오차를 구하고 학습을 해서 모델을 만드는 것
model.add(Dense(units=1))



model.compile(loss='mae', optimizer='adam')
# X_train, y_train은 train할 데이터, X_test, y_test는 실제로 테스트 할 데이터
# epochs : 몇번 테스트를 할 것인지
# batch_size: 각 학습 반복에 사용할 데이터 샘플 수
#             ex) 1000개 데이터를 batch_size =10로 설정하면, 100개의 step을 통해 1epoch를 도는 것
#                 즉, 1epoch(학습1번) = 10(batch_size) * 100(step)
#               batch_size가 커지면 한번에 많은 양을 학습하기 때문에 train 과정이 빨라진다. 그러나 컴퓨터 메모리 문제로 나눠서 학습하는 것
h=model.fit(X_train, y_train, batch_size=32, epochs = 10, validation_data= (X_test, y_test), verbose=1)

# 위에서 만든 모델로 예측 (3차원 데이터를 넣어줘야함)
pred_y = model.predict(X_test)


plt.figure(figsize=[15,6])
# ravel() 1차원으로 변경
# pred_y는 예측한 값
plt.plot(pred_y.ravel(), 'r-', label = 'pred_y')
# y_test는 실제 값
plt.plot(y_test.ravel(), 'b-', label = 'y_test')
# plt.plot((pred_y-y_test).ravel(), 'g-', label = 'diff*10')

plt.legend() # 범례 표시
plt.title("samsung")
plt.show()

# history : 학습한 history를 저장하고 있음
plt.plot(h.history['loss'], label = 'loss')
plt.legend()
plt.title('Loss')
# x축이 epochs / y축이 loss
plt.show()
