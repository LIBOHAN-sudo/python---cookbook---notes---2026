'''
collections的讲解
'''
#什么是collecions:python内置的一个模块，提供了很多有用的容器数据类型。
#其中deque是一个两端都可以快速插入和删除的列表，比如以下:

from collections import deque

#创建一个最多只能存3个元素的队列,这个参数maxlen很重要
q = deque(maxlen = 3)
q.append(1)
q.append(2)
q.append(3)
print(q)
q.append(4)
print(q)       #超出的部分左边的自动被挤掉
print(type(q))

'''
如果你不
设置最大队列大小，那么就会得到一个无限大小队列，你可以在队列的两端执行添加和弹
出元素的操作。
'''
s = deque()
s.append(1)
s.append(2)
s.append(3)
print(s)
s.appendleft(4)
print(s)
a = s.pop()
print(a)
print(s)
b = s.popleft()
print(b)
