'''
并发下载器雏形
'''
import time
import requests
from concurrent.futures import ThreadPoolExecutor,as_completed

urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]

def long(url):
    print(f'开始{url}')
    re = requests.get(url)
    print(f'结束{url}')
    return len(re.content)

#串行
start = time.perf_counter()
for url in urls:
    long(url)
end = time.perf_counter()
print(f'串行耗时:{end-start}')

#并发
start = time.perf_counter()
with ThreadPoolExecutor(max_workers = 10) as executor:
    fuls = [executor.submit(long,url)for url in urls]
    for ful in as_completed(fuls):
        result = ful.result()
        print(result)
end = time.perf_counter()
print(f'并发耗时:{end - start}')
    
