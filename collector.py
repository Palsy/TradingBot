# 아래는 코드에서 주석으로 한글을 쓰기 위해서 달아주는 약속. 암기 X 그냥 복사 -> 붙여넣기.
# 필기 내용

# 파이썬은 들여쓰기가 되지 않은 Level0의 코드를 가장 먼저 실행시킨다.

# openapi.py 라는 소스파일에 있는 모든 함수, 라이브러리, 클래스 등을 가져오고 싶을 경우 아래처럼!
from openapi import *

# -> openapi.py 라는 소스파일에 있는 Openapi 클래스만 가져와서 사용하고 싶은 경우. -> openapi에 import 된 라이브러리를 사용하고 싶지 않다!
# from openapi import Openapi

# 아래 세줄 -> mysql이라는 데이터베이스를 사용하기 위해 필요한 라이브러리들 -> 암기X! 그냥 다음에 mysql을 사용하고 싶으면 아래 세 줄을 복사, 붙여넣기
# 라이브러리 다운로드 -> ctrl + alt + s (file -> setting ->project:bot -> python interpreter)
# 위와 같은 방식으로 설치가 안되는 경우는 아래 terminal 탭 클릭 후 -> pip install pymysql
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()


class Collector:
    def __init__(self):
        print("def __init__(self):")
        # self.api라는 인스턴스 변수를 만든다. Openapi클래스의 인스턴스를 self.api라는 인스턴스 변수에 담는다.
        # Openapi() 클래스를 호출하게 되면 openapi프로그램이 실행 되면서 증권사 계정과 연동이 된다.
        self.api = Openapi()

    def db_setting(self):
        # db_name 이라는 변수에 우리가 조회 하고자 하는 데이터베이스의 이름을 넣는다.
        db_name = 'bot_test1'

        # mysql 데이터베이스랑 연동하는 방식.
        # bot: 계정명
        # 1234!@#$ : 본인 데이터베이스의 비밀번호를 입력
        # localhost : 자신의 PC에 데이터베이스를 구축한 경우 (만약 다른 PC에 데이터베이스를 구축한 경우는 해당 PC의 IP를 기재)
        # 3306 : mysql 접속 기본 포트 번호 (만약 포트 번호를 변경 하신 분은 그에 맞게 설정 해주셔야 합니다.)
        self.engine_bot = create_engine("mysql+mysqldb://bot:" + "1234!@#$" + "@localhost:3306/" + db_name,
                                        encoding='utf-8')

        # 데이터베이스에 실행 할 쿼리
        sql = "select * from bot_test1.class1;"

        # 위의 sql 문을 데이터베이스에 실행한 결과를 rows라는 변수에 담는다.
        rows = self.engine_bot.execute(sql).fetchall()
        print(rows)


#  __name__ ? => 현재 모듈의 이름을 담고 있는 내장 변수, 우리는 colector라는 파일을 실행한다! -> 이 파일의 이름은 __main__ 이 된다.
# import openapi를 통해서 openapi소스코드를 참고를 하는 경우 openapi파일의 __name__은 "openapi"로 찍힌다.
# openapi 파일을 실행하면 그때는 참고 한 것이 아니기 때문에 __name__은 __main__ 이 된다.
print("collector.py __name__: ", __name__)
if __name__ == "__main__":
    print("if __name__ == __main__")
    # 아래는 키움증권 openapi를 사용하기 위해 사용하는 한 줄! 이해 할 필요 X
    app = QApplication(sys.argv)
    # c = collector() 이렇게 c라는 collector라는 클래스의 인스턴스를 만든다.
    # 아래 클래스를 호출하자마다 __init__ 함수가 실행이 된다.
    c = Collector()
    c.db_setting()
