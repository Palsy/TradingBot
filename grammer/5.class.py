print("\n*************************************ex1*************************************")
# class : 붕어빵 틀
class human():
    # 메서드(method) : 클래스 내부에 정의 된 함수(그냥 함수랑 같다고 생각!)
    def dancing(self):
        # self : - 파이썬 메서드의 첫 번째 매개변수 이름은 관례적으로 self를 사용
        #        - 객체를 호출할 때 호출한 객체 자신이 전달되기 때문에 self를 사용한 것
        print("self: ", self)
        print("type(self): ", type(self))

    def singing(self, param):
        # param : 지역변수 (함수 내에서만 사용 가능)
        # self.param : instance 변수 (클래스 내의 다른 함수에서도 사용 가능)
        self.param=param
        print("self.param: ", self.param)

    def working(self):
        # instance 변수는 지역 변수와 달리 다른 메소드에서도 사용 가능
        print("self.param2: ", self.param)



# 파이썬은 들여쓰기가 되지 않은 Level0의 코드를 가장 먼저 실행시킨다.
# 클래스든, 메서드든 호출 되기 전에는 실행 되지 않는다.

# 객체: 객체란 변수들과 그와 관련된 메서드들이 모여서 이룬 하나의 꾸러미(붕어빵)
# 객체, 인스턴스의 차이? : 객체는 실체, 인스턴스는 클래스와의 관계에 집중한 용어이다.
# 즉, 클래스로 만든 객체를 인스턴스라고도 한다.

# jake는 객체다, 그리고 jake 객체는 hunam이라는 클래스의 인스턴스이다.
# "jake는 인스턴스" : X
# "jake는 객체" : O
# "jake는 human의 객체" : X
# "jake는 human의 인스턴스" : O
jake = human()
merry = human()

jake.dancing()
jake.singing("jake에게 파라미터를 넘겨주자!")

print("jake.param: ", jake.param)
jake.working()

merry.singing("merry에게 파라미터를 넘겨주자!")

print("merry.param: ", merry.param)









print("\n*************************************ex2*************************************")
# [계산기 프로그램 만들기 예제]
# class : 붕어빵 틀
# 즉, calc는 붕어빵 틀
class calc():
    # 메서드(method) : 클래스 내부에 정의 된 함수
    def setting_param(self,a,b):
        # self.a : instance 변수
        self.a, self.b= a, b
    def add(self):
        return self.a + self.b
    def sub(self):
        return self.a / self.b
    def mul(self):
        return self.a * self.b
    def mod(self):
        return self.a / self.b


# A, B 는 팥이 아직 안 들어간 같은 붕어빵
# ctrl을 누른 상태로 함수, 변수 클릭 하면 선언부로 이동
A = calc()
B = calc()

# A 붕어빵에는 1,2 라는 팥을 넣음
A.setting_param(1,2)
# B 붕어빵에는 3,4 라는 팥을 넣음
B.setting_param(3,4)

# A라는 인스턴스의 add 메소드를 호출하고 return(반환) 되는 self.a+self.b 결과가 answer라는 변수 안에 저장 된다.
answer = A.add()
print("answer : ",  answer)

# 위에서는 A.add() 의 결과를 answer에 담고 answer를 출력했지만, 변수에 담지 않아도 바로 return 결과를 출력 할 수 있다.
print("A.add() : ",  A.add())

# 똑같이 add() 메소드를 호출 했지만, 3,4 라는 다른 팥을 위에서 넣었기 때문에 다른 결과가 출력 된다.
print("B.add() : ", B.add())


print("\n*************************************ex3*************************************")
class calc():
    # [생성자]
    # 생성자(Constructor): 객체가 생성될 때 자동으로 호출되는 메서드.
    # 파이썬 메서드 이름으로 __init__를 사용하면 이 메서드는 생성자가 된다.
    # __init__ 메서드의 init 앞뒤로 붙은 __는 언더스코어(_) 두 개를 붙여 쓴 것이다.
    def __init__(self, a, b):
        self.a, self.b= a, b
    def add(self):
        return self.a + self.b
    def sub(self):
        return self.a / self.b
    def mul(self):
        return self.a * self.b
    def mod(self):
        return self.a / self.b

# ex2와 비교 시 간결한 코드
A = calc(1,2)
B = calc(3,4)
answer = A.add()
print("answer : ",  answer)
print("A.add() : ",  A.add())
print("B.add() : ", B.add())



