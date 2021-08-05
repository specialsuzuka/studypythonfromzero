import smtplib
from email.mime.text import MIMEText
import socket
import httplib2
import  time
import random
import requests
import importlib
import sys
importlib.reload(sys)
from bs4 import BeautifulSoup
def get_content(url, data=None):
    header = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4557.4 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers = header, timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print ('3:', e)
            time.sleep(random.choice(range(8, 15)))
        except socket.error as e:
            print ('4:', e)
            time.sleep(random.choice(range(20, 60)))
        
    return rep.text

def get_data(html_text):
    bs = BeautifulSoup(html_text, "html.parser")# 创建BeautifulSoup对象
    body = bs.body # 获取body部分
    data = body.find('div', {'id':'7d'}) # 找到id=7d的div
    ul = data.find('ul', {'class':'t clearfix'})
    li = ul.find_all('li')
    # print li
 
    day=li[1]
    temp = []
    date = day.find('h1').string # 找到日期
    temp.append(date)
    inf = day.find_all('p') # 找到li标签中所有的p标签
    temp.append(inf[0].string) # 将第一个p标签中的内容（天气状况）加入到temp中
    if inf[1].find('span') is None:
        emperature_higgest = None # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加一个判断，来输出最低气温
    else:
        temperature_higgest = inf[1].find('span').string # 找到最高气温
        # temperature_higgest = temperature_higgest.replace('℃', '') # 到了晚上网站内容会有变动，去掉这个符号
    if inf[1].find('i') is None:
         temperature_lowest = None
    else:    
         temperature_lowest = inf[1].find('i').string # 找到最低温度
    if inf[2].find("i") is None:
         wind_level=None
    else:
        wind_level=inf[2].find("i").string
        # temperature_lowest = temperature_lowest.replace('℃', '')
        temp.append(temperature_higgest)
        temp.append(temperature_lowest)
        temp.append(wind_level)
        
    return temp


url = 'http://www.weather.com.cn/weather/101010100.shtml'
html = get_content(url)
result = get_data(html)


content=','.join(result)
print(content)
title="明天北京天气"
#设置服务器所需信息
#163邮箱服务器地址
mail_host = 'smtp.163.com'  
#163用户名
mail_user = 'specialsuzuka'
#密码(部分邮箱为授权码) 
mail_pass = 'EEDWSVEXJHVJVUAK'
#邮件发送方邮箱地址
sender = 'specialsuzuka@163.com' 
#邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ["2391604943@qq.com"]  

#设置email信息
#邮件内容设置
message = MIMEText(content,'plain','utf-8')
#邮件主题       
message['Subject'] = title 
#发送方信息
message['From'] = sender 
#接受方信息     
message['To'] = receivers[0]  

#登录并发送邮件
try:
    smtpObj = smtplib.SMTP() 
    #连接到服务器
    smtpObj.connect(mail_host,25)
    #登录到服务器
    smtpObj.login(mail_user,mail_pass) 
    #发送
    smtpObj.sendmail(
        sender,receivers,message.as_string()) 
    #退出
    smtpObj.quit() 
    print('success')
except smtplib.SMTPException as e:
    print('error',e) #打印错误    

