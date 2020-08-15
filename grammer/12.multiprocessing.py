import multiprocessing
import time


def double(val):
    time.sleep(1)
    print(val)
    return val * 2


def single_process(num_list):
    # 시작시간
    start_time = time.time()

    results = []
    for num in num_list:
        results.append(double(num))

    print(results)
    print(f"Single: {time.time() - start_time} seconds")


def multi_process(num_list):
    start_time = time.time()
    # 멀티 쓰레딩 Pool 사용
    # 코어수의 두배를 하는게 가장 빠르다는데
    print("multiprocessing.cpu_count() :", multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(double, num_list)

    print(results)
    print(f"multi: {time.time() - start_time} seconds")


if __name__ == '__main__':
    num_list = [i for i in range(10)]
    single_process(num_list)
    multi_process(num_list)



