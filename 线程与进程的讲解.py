'''
线程与进程
'''
#什么是线程，什么又是进程???
'''
我们来个比喻:

线程 = 一个工人
默认情况下，你的程序只有 1 个工人（主线程,就是Python里从上到下执行代码的程序）
如果你想要同时做多件事，就需要 多个工人（多线程）
多个工人一起干一个工程，同时干活。

进程 = 一个独立的工厂
一个程序运行起来，就是一个进程
一个进程里可以有多个线程（多个工人）
多个进程 = 多个独立的工厂，互不干扰

对比	         线程	                      进程
类比	 同一个工厂里的多个工人	        多个独立的工厂
内存	 共享同一个工厂的仓库	        各自独立的仓库
启动速度	  快	                       慢
资源占用	  小	                       大
适合场景   下载、爬虫、读写文件	        计算、加密、压缩
'''
#什么是线程池，什么是进程池？？？
'''
线程池 = 提前招好一批工人，有任务就派一个去干,反复使用这些工人(线程)
不用每次有任务都现招人（创建线程），也不用干完就辞退（销毁线程）。

同理，进程池 = 提前建好几个工厂，有任务就分配一个工厂去干
'''
#为了更直观的理解，下面举个例子:(关于多线程)
import threading
import time
def say_hello(name):
    print(f'{name}开始工作')
    time.sleep(2)
    print(f'{name}工作完成')

#创建两个线程
t1 =  threading.Thread(target = say_hello,args = ('工人1',))
t2 = threading.Thread(target = say_hello,args = ('工人2',))

#启动
t1.start()
t2.start()

# 等待两个线程都完成
t1.join()
t2.join()

print('所有工作完成')
'''
下面讲讲上面例子里的threading模块
threading译为多线程，只有导入这个模块才能启用多线程功能
Thread:译为线程类，创建一个线程对象(相当于一个工人)

target:目标函数，告诉线程：你要执行 say_hello 这个函数
args	参数	告诉线程：调用 say_hello 时，传入 ("工人A",) 作为参数
这里要说明一下:target,args是固定参数名,而且args传的必须为元组，所以()里有个','

如果没有threading，运行到t1.start()会停2秒，再运行t2.start()再停2秒，有了threading
t1与t2会同时进行，.join()是为了让主线程停下，不要运行print,等待t1与t2完成。
'''
#下面讲讲线程池
'''
线程池的导入方法是:from concurrent.futures import ThreadPoolExecutor
可以用map或submit+as_completed,下面来看map:
'''
from concurrent.futures import ThreadPoolExecutor

def square(n):
    return n * n

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(square, [1, 2, 3, 4, 5])
    print(list(results))  # [1, 4, 9, 16, 25]

'''
这里的max_workers是固定参数名,表示最多同时进行的数量
map()接收一个函数，后面加上一推导入的数据(可迭代对象)，最后按顺序返回值
'''
#下面来看submit+as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
def text(name,seconds):
    time.sleep(seconds)
    return f'{name}完成了'
with ThreadPoolExecutor(max_workers = 3) as executor:
    fuls = [executor.submit(text,'任务A',1),
            executor.submit(text,'任务B',3),
            executor.submit(text,'任务C',2)]
    for ful in as_completed(fuls):
        print(ful.result())
'''
这个例子利用submit+as_completed实现了谁快谁优先输出
submit 的功能
提交一个任务，拿到一个“任务凭证”（Future 对象）。

as_completed 的功能
监控一堆任务，谁先完成，就先处理谁的结果。
'''
#下面说进程
'''
其实进程和线程代码几乎一模一样，只需把threading改成multiprocessing
把threading.Thread()改成multiprocessing.Process()
再在运行t1的上面加个if __name__ == "__main__":
类似于:
if __name__ == "__main__":
    p1 = multiprocessing.Process(target=worker, args=("进程A",))
    p2 = multiprocessing.Process(target=worker, args=("进程B",))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
'''
#下面说说进程池
'''
和进程一样，只要改改导入模块和库就行，连参数max_workers都不用变
再在with上加个if __name__ == '__main__':
'''

'''
这里说说if __name__ == '__main__'在进程里的作用:
在Windows上运行时，当主进程运行到t.start()，
操作系统启动一个全新的 Python 解释器（相当于你双击了 python.exe）
这个新解释器重新导入你的 .py 文件，从头执行，这样反反复复，直到系统崩溃.....
'''
    
