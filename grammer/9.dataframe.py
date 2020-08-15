print("\n*************************************ex1*************************************")
# dataframe ? => 행렬을 저장
from get_item import get_item
# get_item 클래스에 대한 인스턴스인 item 객체를 만든다
item=get_item()
print(item.code_df_kospi)



print("\n*************************************ex2*************************************")
print("type: ", type(item.code_df_kospi))

print("\n*************************************ex3*************************************")
print("len: ", len(item.code_df_kospi))

print("\n*************************************ex4*************************************")
# iloc : 행, 열 단위로 dafaframe 안에 있는 데이터에 접근

# 아래는 0행 0열과 0행 1열을 출력
print(item.code_df_kospi.iloc[0,0], item.code_df_kospi.iloc[0,1])

# 아래는 123행 0열과 123행 1열을 출력
print(item.code_df_kospi.iloc[123,0], item.code_df_kospi.iloc[123,1])

print("\n*************************************ex5*************************************")
# iloc와 동일하게 dataframe에 행, 열로 접근하는데 열의 경우 라벨명으로 접근.

# 아래는 0행 'code_name' 열과 0행 'code'열을 출력
print(item.code_df_kospi.loc[0,'code_name'], item.code_df_kospi.loc[0,'code'])

# 아래는 123행 'code_name' 열과 123행 'code'열을 출력
print(item.code_df_kospi.loc[123,'code_name'], item.code_df_kospi.loc[123,'code'])