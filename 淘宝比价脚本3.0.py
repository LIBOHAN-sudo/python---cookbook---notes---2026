'''
淘宝比价脚本1.0
'''
import platform
import subprocess       #执行系统命令(调用ADB)
import time             # 延时、等待
import sys              # 退出程序(sys.exit)
#subprocess是Python调用外部命令的核心库，所有adb shell xxx都靠它
 
def run_adb(cmd):
    '''执行ADB命令并返回输出'''
    result = subprocess.run(cmd,shell=True,capture_output=True,text=True)
    return result.stdout.strip()
'''
shell=True	在系统 shell 中执行命令（Windows 用 cmd，Mac/Linux 用 bash）
capture_output=True	捕获命令的输出（而不是打印到终端）
text=True	以字符串形式返回（而不是 bytes）
返回值： 命令的标准输出（stdout），并去掉首尾空白字符（.strip()）
'''
def go_home():
    run_adb('adb shell input keyevent 3')
    print('已返回桌面')

def start_taobao():
    '''启动淘宝(两种方式，自动降级)'''
    #方式1，标准am start(优先)
    cmd1 = 'adb shell am start -n com.taobao.taobao/com.taobao.tao.welcom.Welcome'
    result = run_adb(cmd1)
    '''
am start    Activity Manager 启动 Activity
-n	    指定包名/类名
com.taobao.taobao	        淘宝包名
com.taobao.tao.welcome.Welcome	淘宝启动页的 Activity 类名
'''

    if 'Starting' in result and 'Error' not in result:
        print("淘宝启动成功(方式1)")
        return True
    '''
成功时输出类似：Starting: Intent { cmp=com.taobao.taobao/.tao.welcome.Welcome }

失败时输出：Error: xxx
'''
    #方式2:monkey兜底
    cmd2 = 'adb shell monkey -p com.taobao.taobao -c android.intent.category.LAUNCHER 1'
    result = run_adb(cmd2)
    '''
monkey	                                安卓自带的自动化测试工具
-p com.taobao.taobao	                指定包名
-c android.intent.category.LAUNCHER	只启动 LAUNCHER Activity
1	                                执行 1 个事件（即启动）
'''

    if 'Events injected' in result:
        print("淘宝启动成功(方式2)")
        return True
    print('淘宝启动失败，请检查是否已安装')
    return False

def wait_for_taobao(timeout = 10):
    '''动态等待淘宝前台出现'''
    print('等待淘宝加载...',end = '',flush=True)
    '''flush = True:立即输出(不缓存)
Python 的 print() 默认有缓冲区：        
                                     
缓冲区满了才真正输出
或者程序结束了才输出
或者遇到换行符 \n 才输出

想象你在食堂打饭：
厨师炒好一盘菜
不是炒好一块肉就立刻跑出来给你
而是先攒满一盘菜，再一起端出来
这个“盘子”就是缓冲区。

当你写:
print("A")
print("B")
print("C")
实际上 Python 不一定立刻显示，而是：
把 "A" 放进缓冲区（盘子）
把 "B" 放进缓冲区
把 "C" 放进缓冲区
等缓冲区满了 / 遇到换行符 \n / 程序结束
一次性显示 "ABC"
'''

    for i in range(timeout):
        if platform.system() == 'Windows':           
            #获取当前前台应用包名
            cmd = 'adb shell dumpsys window | findstr mCurrentFocus'
        else:
            cmd = 'adb shell dumpsys window | grep mCurrentFocus'
        output = run_adb(cmd)
        #dumpsys window:输出当前窗口状态,grep/findstr mCurrentFocus:过滤出当前焦点窗口
        '''
adb shell dumpsys window,这条命令会输出几百行窗口相关的信息，包括：

所有窗口的层级

窗口大小

当前焦点窗口

等等
grep/findstr mCurrentFocus的作用就是把其余的内容都过滤，只留下当前焦点窗口
'''

        if 'com.taobao.taobao' in output:
            print(f'\n淘宝已打开(耗时{i+1}秒)')
            return True

        print(".",end = '',flush = True)
        time.sleep(1)
    print('\n淘宝启动超时')
    return False
def main():
    go_home()
    time.sleep(0.5)

    #启动淘宝，失败则退出
    if not satrt_taobao():
        sys.exit(1)
    #等待淘宝前台出现。超时则退出
    if not wait_for_taobao():
        sys.exit(1)
    print('\n淘宝已就绪')

if __name__ == '__main__':
    main()

###搜索查询

def search(n):
    search_btn = d(description = '搜索')
    if search_btn.exists:
        btn_bounds = search_btn.info['bounds']

        x = btn_bounds['left']-(btn_bounds['left']/2)
        y = (btn_bounds['top'] + btn_bounds['bottom']) // 2
        d.click(x,y)

        print('已点击搜索框')
        time.sleep(1)
    
         # 清除已有文字（全选 + 删除）
        d.press("select_all")  # 全选
        time.sleep(0.3)
        d.press("delete")      # 删除
        time.sleep(0.3)

        d.send_keys(n)
        time.sleep(1)
        

        search_btn.click()
        print('搜索完成！')
        return True
    else:
        print('搜索失败')
        return False
'''
search_btn = d(description = '搜索'):
使用 uiautomator2 在当前屏幕查找 description 属性为 "搜索" 的 UI 元素。
d() 返回一个 UIObject 对象，代表这个元素。

if search_btn.exists:
检查这个 UI 元素是否存在。exists 是 UIObject 的一个属性，会返回 True 或 False。
注意：访问 exists 会触发一次屏幕扫描，如果元素不存在会等待一小段时间（默认约 1-2 秒）。

info 可以获取控件的完整属性，包括 text、bounds、className 等

btn_bounds = search_btn.info['bounds']
获取元素的位置和大小信息。search_btn.info 返回一个字典，包含元素的详细信息，比如:
{'bounds': {'bottom': 386, 'left': 965, 'right': 1183, 'top': 288},
'childCount': 0, 'className': 'android.view.View', 'contentDescription': '搜索',....等等

top	顶部	元素上边缘到屏幕顶部的距离
bottom	底部	元素下边缘到屏幕顶部的距离
left	左边	元素左边缘到屏幕左边的距离
right	右边	元素右边缘到屏幕左边的距离
'''
###价格排序

def sort_by_price():
    try:
        print('正在设置价格排序')

        s = d(description='综合')
        if s.exists:
            s.click()
            time.sleep(1)
        else:
            print("未找到相关按键")
            return False
        v = d(descriptionContains='价格从低')
        if v.exists:
            v.click()
            print('已排序"价格从低到高"')
            time.sleep(1)
            return True
        else:
            print("未找到相关排序按键")
            return False
    except Exception as e:
        print(f'价格排序失败:{e}')
        return False

'''
'''
###完成实例
import platform
import uiautomator2 as u2
import subprocess
import time
import sys

d = u2.connect()

def run_adb(cmd):
    result = subprocess.run(cmd,shell=True,capture_output=True,text=True)
    return result.stdout.strip()

def go_home():
    run_adb('adb shell input keyevent 3')
    print('已返回桌面')

def start_taobao():
    cmd1 = 'adb shell am start -n com.taobao.taobao/com.taobao.tao.welcome.Welcome'
    result = run_adb(cmd1)

    if 'Starting' in result:
        print("淘宝启动成功(方式1)")
        return True

    cmd2 = 'adb shell monkey -p com.taobao.taobao -c android.intent.category.LAUNCHER 1'
    result = run_adb(cmd2)

    if'Events injected' in result:
        print("淘宝启动成功(方式2)")
        return True
    print('淘宝启动失败，请检查是否安装')
    return False

def wait_for_taobao(timeout = 10):
    print('淘宝加载中...',end = '',flush=True)
    for i in range(timeout):
        if platform.system() == 'Windows':
            cmd = 'adb shell dumpsys window | findstr mCurrentFocus'

        else:
            cmd = 'adb shell dumpsys window | grep mCurrentFocus'

        output = run_adb(cmd)
        if 'com.taobao.taobao' in output:
            print(f'\n淘宝已经打开(耗时{i+1}秒)')
            return True
        print('.',end = '',flush=True)
        time.sleep(1)
    return False

def search(n):
    search_btn = d(description = '搜索')
    if search_btn.exists:
        btn_bounds = search_btn.info['bounds']

        x = btn_bounds['left']-(btn_bounds['left']/2)
        y = (btn_bounds['top'] + btn_bounds['bottom']) // 2
        d.click(x,y)

        print('已点击搜索框')
        time.sleep(1)

        d.press('select_all')
        time.sleep(0.5)
        d.press('delete')
        time.sleep(0.3)

        d.send_keys(n)
        time.sleep(1)
        

        search_btn.click()
        print('搜索完成！')
        return True
    else:
        print('搜索失败')
        return False


def sort_by_price():
    try:
        print('正在设置价格排序')

        s = d(description='综合')
        if s.exists:
            s.click()
            time.sleep(1)
        else:
            print("未找到相关按键")
            return False
        v = d(descriptionContains='价格从低')
        if v.exists:
            v.click()
            print('已排序"价格从低到高"')
            time.sleep(1)
            return True
        else:
            print("未找到相关排序按键")
            return False
    except Exception as e:
        print(f'价格排序失败:{e}')
        return False

def main(n):
    go_home()
    time.sleep(1)

    if not start_taobao():
        sys.exit(1)
    if not wait_for_taobao():
        sys.exit(1)
    print('\n淘宝已就绪，开始搜索')
    for i in range(3):
        try:
            if search(n):
                break
        except Exception as e:
            print(f'错误:{e},正尝试重试')
        if i < 2:
            print('等待2秒后重试...')
            time.sleep(2)
    else:
        print('搜索失败，已重试3次')
        sys.exit(1)

    time.sleep(1)
    if sort_by_price():
        pass
    else:
        return False
    print('\n所有操作执行完成!')
    
        

if __name__ == '__main__':
    n = input('请输入您要查找的内容:')
    print('开始启动查找脚本3.0,祝一切顺利！')
    time.sleep(1)
    main(n)


