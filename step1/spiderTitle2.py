from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree
import math
import random
import os
import csv
import time
from datetime import datetime
from urllib.parse import urlencode

def open_url(url, params, refer=None, delay_range=(1,3), max_retries=10):
    "功能：发起一次http请求，返回一个response"
    headers = get_request_headers(refer)
    query_string = urlencode(params)  # 将参数转换为查询字符串
    full_url = f"{url}?{query_string}"  # 拼接完整 URL

    for attempt in range(max_retries):
        try:
            # 避免请求被拒绝，随机延迟几秒后请求服务器
            # delay = random.randint(*delay_range)
            # print(f"等待 {delay} 秒后请求...")
            # time.sleep(delay)
            
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # 隐藏浏览器界面
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--enable-unsafe-swiftshader") 
            if refer:
                options.add_argument(f"--referer={refer}")
            options.add_argument(f"user-agent={headers['User-Agent']}")

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(full_url)

            # 等待网页加载完成
            time.sleep(1)  

            response = driver.page_source

            driver.quit()

            print(f"请求成功: {full_url}")
            return response

        except Exception as e:
            print(f"第 {attempt + 1} 次尝试发生异常: {e}")

    print("超过最大重试次数，返回None")
    return None

def get_request_headers(referer=None):
    "返回一个http请求头"
    user_agents1 = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    ]

    ua = random.choice(user_agents1)
    headers= {
        "Referer": referer,
        'Host': 'search.ccgp.gov.cn',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep - alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua,
        'Cookie': 'Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1650939609,1651830589,1652150458,1652234205; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1650076632,1651830642,1652150461,1652234207; JSESSIONID=wt3AifLykOW8vb0IzXfwXbcfRCRSWLzNDS6bzKIwGZ-Sw8VjFORl!-1094063090; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1652498396; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1652499001'
    }
    
    return headers

def crawler_ccgp(start_time,end_time,page,ttype,type,sheetdata):
    "这是一个关于《中国政府采购网》中标信息的爬虫；返回二维列表 "
    url = 'http://search.ccgp.gov.cn/bxsearch?'

    params = {
        'searchtype': 1,
        'page_index': page,
        'bidSort': 0,
        'buyerName': '',
        'projectId': '',
        'pinMu':'',
        'bidType': type,
        'dbselect': 'bidx',
        'kw': '',
        'start_time': start_time,
        'end_time': end_time,
        'timeType': 6,
        'displayZone': '黑龙江',
        'zoneId': '23',
        'pppStatus': 0,
        'agentName': ''
    }
    retries = 0
    retry_delay = 2
    total = 0
    while retries < 20 and total==0:
        if retries > 10:
            time.sleep(60)
        response = open_url(url, params)  # 假设 open_url 是自定义的请求函数
        if not response:
            print("请求失败，返回空数据。")
            retries += 1
            time.sleep(retry_delay)
            continue  # 继续下一次尝试

        with open("response.txt", "w", encoding="utf-8") as file:
            file.write(response)

        # 解析 HTML 并提取数据
        tree = etree.HTML(response)
        elements = tree.xpath('/html/body/div[5]/div[1]/div/p[1]/span[2]')
        if elements:  # 检查是否找到匹配的元素
            try:
                total = int(elements[0].text.strip())
                print('从网页发现数据。Total: ' + str(total))
                break
            except ValueError:
                print("提取的数据无法转换为整数。")
        else:
            print(f"第 {retries + 1} 次尝试未找到 total 元素，重新请求...")
            retries += 1
            time.sleep(retry_delay)  # 等待一段时间后重试
            continue  # 继续下一次尝试

    pagesize = 0
    status= False
    curr_page = page
    if total > 0:
        
        pagesize = math.ceil(total / 20)  # 计算出有多少页
        if pagesize >=100:
            return sheetdata,1,status,-1
        sheetdata = sheetdata  # 存储抓取的数据
        retrytimes=0
        while curr_page <= pagesize:
            # 开始抓取项目信息
            list = tree.xpath('/html/body/div[5]/div[2]/div/div/div[1]/ul/li')

            if not list:
                print(f"第 {curr_page} 页加载失败，重新加载...")
                retrytimes+=1
                if retrytimes >5:
                    break
                time.sleep(4)
                response = open_url(url, params)
                if not response:
                    continue
                tree = etree.HTML(response)
                list = tree.xpath('/html/body/div[5]/div[2]/div/div/div[1]/ul/li')
                continue
            else:
                retrytimes=0
            rp3 = ttype
            for li in list:
                title = li[0]
                span = li[2]
                info = span.xpath('string()').replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')


                str1 = info[:info.index(rp3)]
                str2 = info[info.index(rp3):].replace(rp3, '')
                str3 = str2.split('|', 1)
                strs = str3[1].split('|')
                if len(strs) > 1:
                    row = []
                    row.insert(0, (curr_page-1)*20 + len(sheetdata) % 20+1)
                    row.insert(1, rp3.replace('|', ''))
                    row.insert(2, title.text.strip())
                    href = title.get('href')
                    retry_count = 0
                    while href == 'javascript:void(0)' and retry_count < 3:
                        # Retry extracting href
                        href = title.xpath('.//a/@href')
                        href = href[0] if href else 'javascript:void(0)'
                        retry_count += 1
                    row.insert(7, href)

                    str1s = str1.split('|')
                    row.insert(3, str1s[0])
                    row.insert(4, str1s[1].replace('采购人：', ''))
                    row.insert(5, str1s[2].replace('代理机构：', ''))
                    row.insert(6, strs[1])

                    sheetdata.append(row)
            print(f"第 {curr_page} 页抓取完成。")
            if curr_page == pagesize:
                status=True
            # 抓取下一页
            curr_page += 1
            if curr_page <= pagesize:
                params['page_index'] = curr_page
                print('共{}页，当前{}页'.format(pagesize, curr_page))

                response = open_url(url, params)
                if not response:
                    continue

                tree = etree.HTML(response)
    elif total==0:
        status=True

    return sheetdata,curr_page,status,0

def writer_excel(data, directory, filename, head):
    """
    把数据写入 CSV 文件。如果文件存在，则续写；否则新建文件。
    """
    file_path = os.path.join(directory, filename + '.csv')
    os.makedirs(directory, exist_ok=True)  # 确保目录存在

    # 检查文件是否已存在
    file_exists = os.path.exists(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # 如果文件不存在，先写入表头
        if not file_exists:
            writer.writerow(head)
        
        # 写入数据
        writer.writerows(data)

    print(f"数据已保存至 {file_path}")

if __name__ == "__main__":
    start_year = 2024  # 从哪年开始抓取数据
    types = {
        1: "公开招标",
        2: "询价公告",
        3: "竞争性谈判",
        4: "单一来源",
        5: "资格预审",
        6: "邀请招标公告",
        7: "中标公告",
        8: "更正公告",
        9: "其他公告",
        10: "竞争性磋商",
        11: "成交公告",
        12: "终止公告"
    }
    
    curr_time = datetime.now()
    year = 2024

    head = ['序号','类型','名称','日期','采购人','代理机构','品目','链接']
    
    for type in range(1,13):
        
        curr_date = datetime.now()
        curr_year = curr_date.year
        y = curr_year - int(year)
    
        
        start_time=f"{year}:12:15"
        end_time=f"{year}:12:31"

        page,flag=1,False

        while flag!=True:
            if page > 1:
                time.sleep(60)
            sheetdata = []
            print(str(year))
            sheetdata,page,flag,Maxpage = crawler_ccgp(start_time,end_time,page,types[type],type,sheetdata)
            if Maxpage == -1 and flag==False:
                end_time1 = f"{year}:12:22"
                start_time1 = f"{year}:12:23"
                while flag!=True:
                    if page > 1:
                        time.sleep(60)
                        sheetdata = []
                    sheetdata,page,flag,Maxpage = crawler_ccgp(start_time1,end_time,page,types[type],type,sheetdata)
                    
                    print('获取到： ' + str(len(sheetdata)), '条数据')
                    output_dir = os.path.join('data', types[type])
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    writer_excel(sheetdata ,output_dir,str(type)+"file",head)
                flag = False
                page=1
                while flag!=True:
                    if page > 1:
                        time.sleep(60)
                        sheetdata = []
                    sheetdata,page,flag,Maxpage = crawler_ccgp(start_time,end_time1,page,types[type],type,sheetdata)
                    
                    print('获取到： ' + str(len(sheetdata)), '条数据')
                    output_dir = os.path.join('data', types[type])
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    writer_excel(sheetdata ,output_dir,str(type)+"file",head)
                    
            else:    
                print('获取到： ' + str(len(sheetdata)), '条数据')
                output_dir = os.path.join('data', types[type])
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                writer_excel(sheetdata ,output_dir,str(type)+"file",head)

