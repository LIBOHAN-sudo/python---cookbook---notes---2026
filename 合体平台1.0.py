import platform
import uiautomator2 as u2
import sys
import time
import subprocess
from enum import Enum
import keyboard
import functools
import re

d = u2.connect()

def check(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        global stop,back
        stop = False
        back = False
        if keyboard.is_pressed('q'):
            back = True
            print('\n'+'>'*7+'程序已退出'+'<'*7)
            return False
        if keyboard.is_pressed('f')and not stop: 
            print('\n'+'>'*7+'程序已暂停'+'<'*7)
            stop = True

        while stop and not back:
            if keyboard.is_pressed('r'):
                print('\n'+'>'*7+'程序继续运行'+'<'*7)
                stop = False
                break
            if keyboard.is_pressed('q'):
                back = True
                print('\n'+'>'*7+'程序已退出'+'<'*7)

            time.sleep(0.1)

        if back == True:
            return False
        return func(*args,**kwargs)
    return wrapper

def self_sleep(sec):
    global stop,back
    start = time.time()
    while time.time() - start < sec:
        if keyboard.is_pressed('q'):
            back = True
            print('\n'+'>'*7+'程序已退出'+'<'*7)
            sys.exit(0)
        if keyboard.is_pressed('f') and not stop:
            print('\n'+'>'*7+'程序已暂停'+'<'*7)
            stop = True
        while stop and not back:
            if keyboard.is_pressed('r'):
                print('\n'+'>'*7+'程序继续运行'+'<'*7)
                stop = False
                break
            if keyboard.is_pressed('q'):
                back = True
                print('\n'+'>'*7+'程序已退出'+'<'*7)
            time.sleep(0.1)

        if back == True:
            sys.exit(0)
            
        time.sleep(0.1)
            
            

def long(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        for i in range(3):
            if not func(*args, **kwargs):
                print(f'重试尝试:{i+1}/3')
                self_sleep(1)
            else:
                return True
        print('执行失败,已尝试3次')
        return False
    return wrapper

class Platform(Enum):
    TAOBAO = '淘宝'
    PINDUODUO = '拼多多'

PLATFORM_CONFIG = {
    Platform.TAOBAO:{
        'package':'com.taobao.taobao',
        'activity':'com.taobao.tao.welcome.Welcome',
        'search_desc':'搜索',
        'sort_btn':'综合',
        'sort_target_desc':'价格从低',
        'sort_target_text':'价格',
        'sort_type':'price'
        },
    Platform.PINDUODUO:{
        'package':'com.xunmeng.pinduoduo',
        'activity':'com.xunmeng.pinduoduo.ui.activity.MainFrameActivity',
        'search_desc':'搜索',
        'sort_btn':'综合',
        'sort_target_desc':None,
        'sort_target_text':'好评',
        'sort_type':'rating'
        }
    }

def run_adb(cmd):
    result = subprocess.run(cmd,shell=True,capture_output=True,text=True)
    return result.stdout.strip()

def go_home():
    run_adb('adb shell input keyevent KEYCODE_HOME')
    print('已返回桌面')

def get_recent_apps_count():
    go_home()
    self_sleep(1)
    if platform.system() == 'Windows':
        result = run_adb('adb shell dumpsys activity recents | findstr "RecentTask"')
    else:
        result = run_adb('adb shell dumpsys activity recents | grep "RecentTask"')
    count = len([line for line in result.split('\n')if'RecentTask'in line])
    if count >0:
        print('开始清理')
        return count
    else:
        print('检测到后台无程序')
        return 0
    
def get_clear(count):
    try:
        result = run_adb('adb shell wm size')
        match = re.search(r'(\d+)x(\d+)',result)
        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            centerX = width/2
            Y1 = height * (2/3)
            Y2 = height/3
            b = height
            run_adb('adb shell input keyevent KEYCODE_APP_SWITCH')
            for i in range(count):
                run_adb(f'adb shell input swipe {centerX} {Y1} {centerX} {Y2} 150')
            print('清理完毕!')
            return True
        else:
            sys.exit(0)
    except Exception as e:
        print(f'错误:{e},程序已退出')
        sys.exit(1)         
        
@check
def start_app(platform_type):
    confing = PLATFORM_CONFIG[platform_type]
    package = confing['package']
    activity = confing['activity']

    cmd1 = f'adb shell am start -n {package}/{activity}'
    result = run_adb(cmd1)

    if 'Starting' in result:
        print(f'\n{platform_type.value}启动成功(方式1)')
        return True

    cmd2 = f'adb shell monkey -p {package} -c android.intent.category.LAUNCHER 1'
    result = run_adb(cmd2)

    if 'Events injected' in result:
        print(f'\n{platform_type.value}启动成功(方式2)')
        return True
    print(f'\n{platform_type.value}启动失败,请检查是否安装')
    return False

@check
def wait_for_app(platform_type,timeout=10):
    confing = PLATFORM_CONFIG[platform_type]
    package = confing['package']
    activity = confing['activity']

    print(f'{platform_type.value}加载中...',end='',flush = True)
    for i in range(timeout):
        if platform.system() == 'Windows':
            cmd = 'adb shell dumpsys window | findstr mCurrentFocus'
        else:
            cmd = 'adb shell dumpsys window | grep mCurrentFocus'

        output = run_adb(cmd)

        if package in output:
            print(f'\n{platform_type.value}已打开，耗时{i+1}秒')
            return True
        
        print('.',end='',flush=True)
        self_sleep(1)
    print(f'\n{platform_type.value}启动超时')
    return False
@check      
def search(platform_type, keyword):
    config = PLATFORM_CONFIG[platform_type]
    search_desc = config["search_desc"]
    search_btn = d(description=search_des).wait(timeout=3)
    
    if search_btn.exists:
        if platform_type == Platform.TAOBAO:
      
            btn_bounds = search_btn.info['bounds']
            x = btn_bounds['left'] - (btn_bounds['left'] / 2)
            y = (btn_bounds['top'] + btn_bounds['bottom']) // 2
            d.click(x, y)
        else:
            search_btn.click()
        
        print('已点击搜索框')
        self_sleep(1)
        
        d.clear_text()
        self_sleep(1)

        d.send_keys(keyword)
        self_sleep(1)

        v = d(text='搜索')
        if v.exists:
            v.click()
        else:
            d.press('enter')
        
        print('搜索完成')
        return True
    else:
        print('未找到搜索框')
        return False

@check
@long
def sort_by_condition(platform_type):
    config = PLATFORM_CONFIG[platform_type]  
    try:
        sort_btn = d(text=config["sort_btn"])
        if not sort_btn.exists:
            sort_btn = d(description=config["sort_btn"])
        
        if sort_btn.exists:
            sort_btn.click()
            print('已点击排序按钮')
            return True
        else:
            print('未找到排序按钮')
            return False
        
    except Exception as e:
        print(f'排序失败: {e}')
        return False

@check
@long
def sort_target(platform_type):
    confing = PLATFORM_CONFIG[platform_type]
    sort_type = confing["sort_type"]
    try:
        if sort_type == "price":
            target = d(descriptionContains=confing['sort_target_desc'])
            if target.exists:
                target.click()
                print(f'已按{confing["sort_target_text"]}从低到高排序')
                return True
            else:
                print(f'未找到{confing["sort_target_text"]}相关排序选项')
                return False
        else:
            target = d(textContains=confing["sort_target_text"])
            if target.exists:
                target.click()
                print(f'已按{confing["sort_target_text"]}排序')
                return True
            else:
                print(f'未找到{confing["sort_target_text"]}相关排序选项')
                return False
                
    except Exception as e:
        print(f'排序失败: {e}')
        return False

def main():
    global stop,back
    stop = False
    back = False
    print('''请选择平台:
1.淘宝
2.拼多多''')
    choice = input("请输入序号(1/2): ").strip()
    i = 0
    while True:
        if choice not in ['1','2']:
            i += 1
            if i <=3:
                print(f'请按要求规范输入,重试:{i}')
                choice = input("请输入序号(1/2): ").strip()
            else:
                print('已重试三次')
                break
        else:
            print('\n输入成功!')
            break
    if choice =='1':
        platform_type = Platform.TAOBAO
        platform_name = '淘宝'
    elif choice =='2':
        platform_type = Platform.PINDUODUO
        platform_name = '拼多多'
    else:
        print('无效选择，默认使用淘宝')
        platform_type = Platform.TAOBAO
        platform_name = '淘宝'

    keyword = input(f'\n请输入在{platform_name}搜索的内容:')
    self_sleep(0.5)
    print('''\n是否自动清理后台程序:

1.是
2.否''')
    clear = input('\n请输入序号(1/2):').strip()
    j = 0
    while True:
        if clear not in ['1','2']:
            j+=1
            if j<=1:
                print('请按要求重新输入:')
                clear = input('\n请输入序号(1/2):').strip()
            else:
                print('\n重试失败')
                break
        else:
            print('\n输入成功!')
            break
        
    print('''\n
您可以在运行过程中:
按"q"/"Ctrl+C"键退出程序
按"f"键暂停程序
按"r"键继续程序
''')
    self_sleep(1)
    print('开始执行任务')
    self_sleep(1)
    if clear =='1':
        print('\n正在检测后台程序')
        self_sleep(1)
        count = get_recent_apps_count()
        if count >0:
            print('共检测出'+str(count)+'个程序')
            self_sleep(1)
            get_clear(count)
        else:
            pass
    elif clear == '2':
        go_home()
    else:
        print('无效选择，默认清理后台程序')
        self_sleep(1)
        print('\n正在检测后台程序')
        self_sleep(1)
        count = get_recent_apps_count()
        if count >0:
            print('共检测出'+str(count)+'个程序')
            self_sleep(1)
            get_clear(count)
       
    self_sleep(0.8)

    print(f'\n开始启动{platform_name}')
    self_sleep(0.8)

    if not start_app(platform_type):
        sys.exit(1)
    if not wait_for_app(platform_type):
        sys.exit(1)
    self_sleep(1)

    for i in range(3):
        try:
            if search(platform_type,keyword):
                break
        except Exception as e:
            print(f'错误:{e},正在尝试重试')

        if i < 2:
            print('等待2秒后重试')
            self_sleep(2)
    else:
        print('搜索失败,已尝试3次')
        sys.exit(1)

    self_sleep(1)
    print('\n正在设置相关排序')
    if not sort_by_condition(platform_type):
        sys.exit(1)
    self_sleep(1)
    if not sort_target(platform_type):
        sys.exit(1)
    
    print('\n所有操作执行完毕!')
    self_sleep(1)
    return True

if __name__ == '__main__':
    i = 0
    try:
        while True:
            main()
            i+=1
            print('\n'+'='*50)
            print(f'第{i}次程序执行完毕！3秒后准备执行第{i+1}次')
            print('='*50)
            self_sleep(3)
    except KeyboardInterrupt:
        print('\n用户按Ctrl+C终止程序')
        sys.exit(0)
                
        



    

    
    

    



    
        
