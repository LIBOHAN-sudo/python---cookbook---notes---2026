'''
串行与并发的讲解
'''
#什么是串行，什么又是并发
'''
假如现在有3个2秒的计算程序，串行需要一个个执行，共需6秒
并发会同时开始执行，运行时长小于6秒，具体取决于CPU，任务类型，并发方式
并发可以用多线程去实现
并发不一定是"多个进程",一个进程里的多个线程，也是并发

如果要加上网络请求，并发会比串行更合适，因为:

线程1: [工作0.01秒][等1秒][工作0.01秒] → 完成
       然后
线程1: [工作0.01秒][等1秒][工作0.01秒] → 完成
       然后
线程1: [工作0.01秒][等1秒][工作0.01秒] → 完成

总耗时：3.03秒



线程1: [工作0.01秒][等1秒........................]
线程2:            [工作0.01秒][等1秒.............]
线程3:                       [工作0.01秒][等1秒]

时间线：
0.00秒：线程1开始，工作0.01秒，然后开始等
0.01秒：线程2开始，工作0.01秒，然后开始等
0.02秒：线程3开始，工作0.01秒，然后开始等
1.01秒：线程1等完了，工作0.01秒，完成
1.02秒：线程2等完了，工作0.01秒，完成
1.03秒：线程3等完了，工作0.01秒，完成

总耗时：约1.03秒
所以爬虫，并发会比串行更合适
'''
#下面看一个有关线程的串行与并发
import requests
import time

urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]
def text(url):
    print(f'开始{url}')
    re = requests.get(url)
    print(f'结束{url}')
start = time.perf_counter()
for url in urls:
    text(url)
end = time.perf_counter()
print(f'串行耗时:{end- start:.2f}s')
'''
这个例子就是串行，也就是一个一个读取里面网址的内容
'''
#下面对比一下并发(线程池)
from concurrent.futures import ThreadPoolExecutor,as_completed
import requests
import time

urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]
def text(url):
    print(f'开始{url}')
    re = requests.get(url)
    print(f'结束{url}')
    return len(re.content)

start = time.perf_counter()
with ThreadPoolExecutor(max_workers = 3) as executor:
    fuls = [executor.submit(text,url) for url in urls]
    for ful in as_completed(fuls):
        result = ful.result()
        print(f'得到结果:{result}')
end = time.perf_counter()
print(f'并发耗时:{end - start:.2f}s')
'''
并发的进程池，只需把导入的ThreadPoolExecutor 改成 ProcessPoolExecutor
再在start,上面加上if __name__ == '__main__':
'''
    
    
