# version 1.3.2
# 이 코드가 완벽히 이해가 된다면 봇 개발 절반은 성공.


#아래는 코드에서 주석으로 한글을 쓰기 위해서 달아주는 약속. 암기 X 그냥 복사 -> 붙여넣기.

# crtl + alt + 좌우방향키 : 이전 커서 위치로

print("collector 프로그램이 시작 되었습니다!")
# 파이썬은 들여쓰기가 되지 않은 Level0의 코드를 가장 먼저 실행시킨다.

# openapi.py 라는 소스파일에 있는 모든 함수, 라이브러리, 클래스 등을 가져오고 싶을 경우 아래처럼!

# 아래 openapi는 더이상 사용하지 않습니다. =>
# openapi파일은 예제용이며 실제 사용하는 파일은 library 폴더 안의 open_api 입니다.
# from openapi import *
from library.collector_api import *
# -> openapi.py 라는 소스파일에 있는 Openapi 클래스만 가져와서 사용하고 싶은 경우. -> openapi에 import 된 라이브러리를 사용하고 싶지 않다!
# from openapi import Openapi

# 아래 세줄 -> mysql이라는 데이터베이스를 사용하기 위해 필요한 라이브러리들 -> 암기X! 그냥 다음에 mysql을 사용하고 싶으면 아래 세 줄을 복사, 붙여넣기
# 라이브러리 다운로드 -> ctrl + alt + s (file -> setting ->project:bot -> python interpreter)
# 위와 같은 방식으로 설치가 안되는 경우는 아래 terminal 탭 클릭 후 -> pip install pymysql
import pymysql
pymysql.install_as_MySQLdb()


class Collector:
    print("collector 클래스에 들어왔습니다.")

    def __init__(self):
        print("__init__ 함수에 들어왔습니다.")
        # self.api라는 인스턴스 변수를 만든다. Openapi클래스의 인스턴스를 self.api라는 인스턴스 변수에 담는다.
        # Openapi() 클래스를 호출하게 되면 openapi프로그램이 실행 되면서 증권사 계정과 연동이 된다.

        # self.collector_api: 데이터를 수집하는 API 클래스에 대한 인스턴스
        self.collector_api = collector_api()
        #코스피, 코스닥 종목 출력 테스트

    def collecting(self):
        self.collector_api.code_update_check()

#  __name__ ? => 현재 모듈의 이름을 담고 있는 내장 변수, 우리는 colector라는 파일을 실행한다! -> 이 파일의 이름은 __main__ 이 된다.
# import openapi를 통해서 openapi소스코드를 참고를 하는 경우 openapi파일의 __name__은 "openapi"로 찍힌다.
# openapi 파일을 실행하면 그때는 참고 한 것이 아니기 때문에 __name__은 __main__ 이 된다.
print("collector.py 의 __name__ 은?: ", __name__)
if __name__ == "__main__":
    print("__main__에 들어왔습니다.")
    # 아래는 키움증권 openapi를 사용하기 위해 사용하는 한 줄! 이해 할 필요 X
    app = QApplication(sys.argv)
    # c = collector() 이렇게 c라는 collector라는 클래스의 인스턴스를 만든다.
    # 아래 클래스를 호출하자마다 __init__ 함수가 실행이 된다.
    c = Collector()

    # 데이터 수집 시작 -> 주식 종목, 종목별 금융 데이터 모두 데이터베이스에 저장.
    c.collecting()
