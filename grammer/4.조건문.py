print("\n*************************************ex1*************************************")
# [ 비교연산자 ]
# x < y	x가 y보다 작다
# x > y	x가 y보다 크다
# x == y	x와 y가 같다
# x != y	x와 y가 같지 않다
# x >= y	x가 y보다 크거나 같다
# x <= y	x가 y보다 작거나 같다

# [if ~ else 조건문]
a=1
b=2

if a==b:
 print("같다.")
else:
 print("다르다")










print("\n*************************************ex2*************************************")
# [ if ~ elif ~ else 조건문 ]
a=1
b=2

if a>b:
 print("a가 크다")
elif a<b:
 print("b가 크다")
else:
 print("a와 b는 같다.")









print("\n*************************************ex3*************************************")
#[ bool 자료형 ]

# True : 참
a=True

# False : 거짓
b=False

# and , or , not 연산자
   # x or y: x와 y 둘중에 하나만 참이어도 참
   # x and y:	x와 y 모두 참이어야 참
   # not x	: x가 거짓이면 참이다


print("True and False:", a and b)
print("True or False:", a or b)
print("True and True:", a and a)
print("True or True:", a or a)
print("False and False:", b and b)
print("False or False:", b or b)
print("not True:", not a)
print("not False:", not b)






print("\n*************************************ex4*************************************")
# 컴퓨터에서 1은 True, 0은 False로 해석 가능
a=1
b=0
print("1 and 0:", a and b)
print("1 or 0:", a or b)
print("1 and 1:", a and a)
print("1 or 1:", a or a)
print("0 and 0:", b and b)
print("0 or 0:", b or b)
print("not 1:", not a)
print("not 0:", not b)
