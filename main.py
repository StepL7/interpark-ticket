# exe试验
# 谷歌浏览器
# 按座位图选择
import sys
from datetime import datetime
import os
import pickle
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
import base64
import re
import traceback


# from infodemo import *
from info import *
from SeatArea import *
import logging
import os

def loginit():
    log_folder = 'log'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S');
    # 配置日志输出到文件
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 创建 debug 日志处理器
    debug_handler = logging.FileHandler(f'log/info-{now}.log')
    debug_handler.setLevel(logging.INFO)
    debug_handler.setFormatter(formatter)

    # 创建其他级别日志处理器
    other_handler = logging.FileHandler(f'log/error-{now}.log')
    other_handler.setLevel(logging.ERROR)
    other_handler.setFormatter(formatter)

    # 获取根日志记录器并添加处理器
    logger = logging.getLogger()
    logger.addHandler(debug_handler)
    logger.addHandler(other_handler)

# interpark主页
main_url = "https://www.globalinterpark.com/main/main"
# 登录地址
login_url = "https://www.globalinterpark.com/user/signin?redirectUrl=aHR0cDovL3d3dy5nbG9iYWxpbnRlcnBhcmsuY29tL21haW4vbWFpbg=="
# 抢购地址
#target_url = "https://www.globalinterpark.com/detail/edetail?prdNo=23008837&dispNo=01011"
target_url = "https://www.globalinterpark.com/detail/edetail?prdNo=23007165&dispNo=undefined"
# 登录 打开抢购页面
def Login():
    # 输入账号 账号输入框：#memEmail
    driver.find_element(By.ID, "memEmail").send_keys(Email)
    # 输入密码 密码输入框：#memPass
    driver.find_element(By.ID, "memPass").send_keys(Password)
    # 点击登录 登录按钮：#sign_in
    driver.find_element(By.ID, "sign_in").click()
    time.sleep(1)
    # 打开抢购页面
    driver.get(target_url)

# 抢购页面点击预订 选择日期 处理弹窗 识别验证码
def Booking():
    # 点击预订
    WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.ID,'product_detail_area')))
    driver.switch_to.frame("product_detail_area")
    driver.find_element(By.CSS_SELECTOR,'body > div > div > div.wrap_Pinfo > div.bak > div.Py_Time > div.Date_Select > div.btn_Booking > img').click()
    time.sleep(1)
    #获取窗口并切换到新窗口
    global handles
    handles = driver.window_handles
    driver.switch_to.window(handles[1])

def Date(initCount):
    global CodeFlag
    # 选择观赏日期 默认选第二个
    # time.sleep(0.5)
    dateinnercount = 0
    # 这里高峰期会排队，所以一直循环就可以initCount 判断是第一次进来
    while True:
        try:
            dateinnercount = dateinnercount + 1
            driver.switch_to.frame("ifrmBookStep")
            driver.find_elements(By.ID, 'CellPlayDate')[1].click()
            # 如果还要选时间，这里就别注释，特别需要睡眠一会，不然点不动
            # time.sleep(0.5)
            # driver.find_elements(By.ID, 'CellPlaySeq')[0].click()
        except Exception as e:
            if initCount == 0:
                continue
            # 可能是登录状态变了，或者超20分钟了
            raise e
        break
    # 两次点击间要睡眠一会
    time.sleep(0.5)
    # 下一步
    driver.switch_to.parent_frame()
    dateinnercount3 = 0
    while True:
        try:
            dateinnercount3 = dateinnercount3 + 1
            driver.find_element(By.CSS_SELECTOR, '#LargeNextBtnImage').click()
        except:
            time.sleep(0.5)
            if initCount == 0:
                continue
                # 可能是登录状态变了，或者超20分钟了
            raise e
        break
    # Alert处理
    Alert()
    # 处理验证码
    WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.ID,'ifrmSeat')))
    dateinnercount4 = 0
    while True:
        try:
            dateinnercount4 = dateinnercount4 + 1
            driver.switch_to.frame("ifrmSeat")
        except:
            time.sleep(0.5)
            if initCount == 0:
                continue
                # 可能是登录状态变了，或者超20分钟了
            raise e
        break
    while CodeFlag:
        IsCodeExist()
        DoCode()
    dateinnercount5 = 0
    while True:
        try:
            dateinnercount5 = dateinnercount5 + 1
            driver.switch_to.frame("ifrmSeatDetail")
        except:
            time.sleep(0.5)
            if initCount == 0:
                continue
                # 可能是登录状态变了，或者超20分钟了
            raise e
        break
    time.sleep(0.5)
    ChooseSeat()

# 判断验证码是否存在
def IsCodeExist():
    try:
        global flag
        flag = False
        flag = driver.find_element(By.ID, 'divRecaptcha').is_displayed()
        return flag
    except:
        logging.info("###无须进行验证码操作1###")

# 百度云通用文字识别（标准版）
def CodeIdentify():
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    # f = open('D:/my_pythonProject/Interpark/yzm2.png', 'rb')
    f = open('yzm2.png', 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = '[24.35c9ee35a483db5c3fdf476bf5230d49.2592000.1690558228.282335-35370119]'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # logging.info(response.json())
        result = response.json()
        str = json.dumps(result)
        global code
        code = ''.join(re.findall(r'[A-Z]',str))

# 识别并输入验证码
def Identify_Input():
    # 定位验证码img截图并保存
    WebDriverWait(driver,30,0.5).until(EC.presence_of_element_located((By.ID,'imgCaptcha')))
    # driver.find_element(By.ID, 'imgCaptcha').screenshot(r'D:/my_pythonProject/Interpark/yzm2.png')
    driver.find_element(By.ID, 'imgCaptcha').screenshot(r'yzm2.png')
    CodeIdentify()
    logging.info(f'验证码为：{code}')
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, '#divRecaptcha > div.capchaInner.G2001 > div.validationTxt > span').click()
    logging.info("已点击span")
    time.sleep(0.5)
    # driver.find_element(By.ID, 'txtCaptcha').send_keys(code)
    driver.find_element(By.CSS_SELECTOR, '#txtCaptcha').send_keys(code)
    logging.info("已输入验证码")
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR,'#divRecaptcha > div.capchaInner.G2001 > div.capchaBtns > a:nth-child(2)').click()
    logging.info("已点击提交")
    # submit后再次判断验证码是否存在
    IsCodeExist()

# 验证码操作
def DoCode():
    while flag:
        Identify_Input()
        while flag:
            RefreshCode()
    global CodeFlag
    CodeFlag = False

# 验证失败，刷新图片重新验证
def RefreshCode():
    logging.info("###验证失败，刷新图片重新验证")
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'refreshBtn')))
    driver.find_element(By.CLASS_NAME, 'refreshBtn').click()
    Identify_Input()

# 处理弹窗 alert（警告信息）和confirm（确认信息）
def Alert():
    try:
        driver.switch_to.alert.accept()
        logging.info("###已处理日期页弹窗###")
    except:
        logging.info("###日期页无弹窗###")

# 判断选座失败弹窗是否弹出
def SeatAlert():
    global Seatflag
    Seatflag = True
    try:
        driver.switch_to.alert.accept()
        logging.info("### 有弹窗 座位被占 重新选座###")
        return Seatflag
    except:
        logging.info("###无弹窗 选座成功###")
        Seatflag = False
        return Seatflag

def ChooseSeat():
    global n
    global i
    global x
    global y
    i = 0
    while i < SeatTotal:
        m = 0
        while m < 1:
            n = list_order[x]
            y = list_AreaName[x]
            chooseSeatCount = 0
            while True:
                try:
                    chooseSeatCount = chooseSeatCount + 1
                    element = driver.find_element(By.XPATH, f'//*[@id="TmgsTable"]/tbody/tr/td/map/area[{n}]')
                    driver.execute_script("arguments[0].click();", element)
                except:
                    time.sleep(0.5)
                    continue
                break

            logging.info(f'进入了：{y}区')
            try:
                elements = driver.find_elements(By.XPATH, "//*[@id='TmgsTable']/tbody/tr/td/span[not(@class='SeatR' or @class='SeatT') and @class!='']")

                elements[0].click()
                # driver.find_elements(By.ID, 'Seats')[i].click()
                i += 1
                m += 1
            except:
                logging.info(f'{y}区无票 正在刷新')
                # logging.info("###无票 正在刷新###")
                driver.refresh()
                x += 1
                if x >= len(list_order):
                    x = 0
                # Alert()
                Date(1)
                return
    # 下一步
    logging.error(f'{y}区找到了！！')
    while True:
        try:
            driver.switch_to.parent_frame()
            driver.find_element(By.ID,"NextStepImage").click()
        except:
            logging.error(f'{y}区找到了但是后续发生异常，请关注')
            continue
        break
    # 无须返回iframe（0） 直接识别弹窗
    time.sleep(0.5)
    SeatAlert()

# 再次选座
def ChooseSeatAgain():
    driver.switch_to.frame("ifrmSeatDetail")
    global i
    global x
    global y
    # 取消选择第一个（取消后该座位仍可以点击）
    # 选择后一个
    try:
        driver.find_elements(By.ID,'Seats')[0].click()
        driver.find_elements(By.ID,'Seats')[i].click()
    except:
        # 分区无票 刷新
        logging.info(f'{y}区无票 正在刷新')
        # logging.info("###整场或该分区无票 正在刷新###")
        driver.refresh()
        x += 1
        if x >= len(list_order):
            x = 0
        Date(1)
    i += 1
    # 下一步
    driver.switch_to.parent_frame()
    driver.find_element(By.ID, "NextStepImage").click()
    time.sleep(0.5)
    SeatAlert()

# 选择价格
def Price():
    # 2.2.3 选择价格
    time.sleep(0.5)
    # 切换窗口
    global hansles
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    # 选择数量
    driver.switch_to.frame(0)
    # 下拉框选择最后一项
    select = driver.find_element(By.NAME, "SeatCount")
    options_list = Select(select).options
    selectLen = len(options_list)
    Select(select).select_by_index(selectLen - 1)
    # 下一步
    driver.switch_to.parent_frame()
    driver.find_element(By.ID, "SmallNextBtnImage").click()
    UserCertify()

# 用户须知确认（在选择价格后出现）费时
def UserCertify():
    try:
        driver.switch_to.frame("ifrmBookCertify")
        driver.find_element(By.ID,'Agree').click()
        driver.find_element(By.CSS_SELECTOR,'#information > div.inforbtn > a:nth-child(1) > img').click()
        # 下一步
        driver.switch_to.parent_frame()
        driver.find_element(By.ID, "SmallNextBtnImage").click()
    except:
        logging.info("###无agree步骤###")

# 输入基本信息
def InputInfo():
    # 不使用UserCertify()无须切换窗口
    global handles
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    # 2.2.4 输入订购者信息
    driver.switch_to.frame(0)
    # 姓名
    driver.find_element(By.ID, "MemberName").send_keys(Name)
    # 年
    year = driver.find_element(By.ID, "BirYear")
    Select(year).select_by_visible_text(Year)
    # 月
    month = driver.find_element(By.ID, "BirMonth")
    Select(month).select_by_visible_text(Month)
    # 日
    day = driver.find_element(By.ID, "BirDay")
    Select(day).select_by_visible_text(Day)
    # 联系电话
    driver.find_element(By.ID, "PhoneNo").send_keys(PhoneNo)
    # 手机号码
    driver.find_element(By.ID, "HpNo").send_keys(HpNo)
    # 下一步
    driver.switch_to.parent_frame()
    driver.find_element(By.ID, "SmallNextBtnImage").click()

# 付款方式
def PayWay():
    # 2.2.5 付款
    driver.switch_to.frame(0)
    # 选择信用卡种类
    driver.find_elements(By.ID, "PaymentSelect")[1].click()
    card = driver.find_element(By.ID, "DiscountCardGlobal")
    Select(card).select_by_visible_text("Visa")
    # 输入卡号
    driver.find_element(By.ID, "CardNo1").send_keys(CardNo1)
    driver.find_element(By.ID, "CardNo2").send_keys(CardNo2)
    driver.find_element(By.ID, "CardNo3").send_keys(CardNo3)
    driver.find_element(By.ID, "CardNo4").send_keys(CardNo4)
    # 选择卡有效期
    validMonth = driver.find_element(By.ID, "ValidMonth")
    Select(validMonth).select_by_visible_text(ValidMonth)
    validYear = driver.find_element(By.ID, "ValidYear")
    Select(validYear).select_by_visible_text(ValidYear)
    # 下一步
    driver.switch_to.parent_frame()
    driver.find_element(By.ID, "SmallNextBtnImage").click()

# 最终确认
def Finaly():
    # # 最终确认
    driver.switch_to.frame(0)
    driver.find_element(By.ID, "CancelAgree").click()
    driver.find_element(By.ID, "CancelAgree2").click()
    # 付款
    driver.switch_to.parent_frame()
    driver.find_element(By.ID, "LargeNextBtnImage").click()

def getErrorLine():
    # 获取异常信息
    exc_type, exc_value, exc_traceback = sys.exc_info()

    # 获取异常所在的堆栈跟踪信息
    tb_info = traceback.extract_tb(exc_traceback)

    # 获取异常发生的文件名
    filename = tb_info[-1].filename

    # 获取异常发生的行号
    lineno = tb_info[-1].lineno
    return lineno

if __name__ == '__main__':
    # 浏览器配置对象
    options = webdriver.ChromeOptions()
    # 禁用自动化栏
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 屏蔽保存密码提示框
    prefs = {'credentials_enable_service': False, 'profile.password_manager_enable': False}
    options.add_experimental_option('prefs', prefs)
    # 反爬虫特征处理
    options.add_argument('--disable-blink-features=AutomationControlled')
    count = 0
    global maxCount
    maxCount = 10
    while True:
        try:
            loginit()
            # 打印当前时间f
            logging.error("当前时间进入登录页面：%s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # 打开浏览器
            driver = webdriver.Chrome(options=options)

            # 打开主页 登录页面
            driver.get(login_url)

            Login()

            # 切换英文
            while True:
                try:
                    count = count + 1
                    driver.find_element(By.ID, 'lang_title').click()
                    driver.find_element(By.ID, 'lang_en').click()
                except Exception as e:
                    time.sleep(0.5)
                    if count > 20:
                        lineno = getErrorLine()
                        logging.error(f'Exception line {lineno}: {e}')
                        break
                    continue
                break

            time.sleep(1)

            global n
            global x
            global CodeFlag
            CodeFlag = True
            n = 1
            x = 0

            Booking()
        except:
            lineno = getErrorLine()

            logging.error("当前时间进入选座前发生异常：%s，异常行数: %s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), lineno)
            continue
        dateCount = 0
        try:
            dateCount = dateCount + 1
            logging.error("当前时间进入选座页面：%s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            global initCount
            initCount = 0
            Date(0)
        except Exception as e:
            time.sleep(0.5)
            # 获取异常发生的行号
            lineno = getErrorLine()

            # 记录异常信息，包括行号
            logging.error("当前时间退出选座：%s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            logging.error(f'Exception line {lineno}: {e}')
            # 这里是防止登录失效或者超过20分钟，需要重新登录下
            continue
        break

    # 下面的代码没经过测试，这里加声音
    # 播放系统默认的提示音10s
    logging.error("当前时间找到座位：%s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        os.system("afplay /System/Library/Sounds/Ping.aiff -t 10")
    except:
        logging.error("当前时间报警异常：%s, 发生异常:%s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(e))

    try:
        while Seatflag:
            ChooseSeatAgain()
        Price()
        InputInfo()
        PayWay()
        Finaly()
    except Exception as e:
        logging.error("当前时间退出后续操作：%s, 发生异常:%s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(e))
        while True:
            # 提醒人工介入处理
            try:
                os.system("afplay /System/Library/Sounds/Ping.aiff -t 10")
            except:
                logging.error("当前时间报警异常：%s, 发生异常:%s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(e))
