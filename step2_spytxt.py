import random
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_request_headers(referer=None):
    "返回一个http请求头"
    user_agents1 = [
        # 移动设备用户代理
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 12; Pixel 5 Build/SQ1A.210205.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.70 Mobile Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.78 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.78 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 9; SM-J600G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36',

        # 桌面设备用户代理
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.5; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/104.0.1293.70',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/90.0.4480.82 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/102.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/105.0.1343.27',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/91.0.4516.50 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.0; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro Build/TKQ1.220305.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.1; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/106.0.1370.42',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
    ]

    ua = random.choice(user_agents1)
    headers = {
        "Referer": referer if referer else '',
        'Host': 'search.ccgp.gov.cn',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua,
        'Cookie': 'Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1650939609,1651830589,1652150458,1652234205; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1650076632,1651830642,1652150461,1652234207; JSESSIONID=wt3AifLykOW8vb0IzXfwXbcfRCRSWLzNDS6bzKIwGZ-Sw8VjFORl!-1094063090; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1652498396; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1652499001'
    }
    
    return headers

def open_url(url,refer=None, max_retries=2):
    "功能：发起一次http请求，返回一个response"
    headers = get_request_headers(refer)
    full_url = url

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
            # 可选：禁用图片加载以加快加载速度
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(full_url)
            # 等待特定元素加载完成，假设等到一个div或者body元素加载完成
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vF_detail_content_container"))
            )

            response = driver.page_source

            driver.quit()

            print(f"请求成功: {full_url}")
            return response

        except Exception as e:
            print(f"第 {attempt + 1} 次尝试发生异常")

    print("超过最大重试次数，返回None")
    return None
    

if __name__ == "__main__":
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

    for index in range( 1,13):
        csv_file_path = f'data/{types[index]}/failed_requests.csv'
        if not os.path.exists(f'data/{types[index]}/content'):
            os.makedirs(f'data/{types[index]}/content')
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                serial_number = row[0]
                url = row[1]
                
                for attempt in range(1):
                    response = open_url(url)
                    if response:
                        # 解析 HTML 并提取数据
                        tree = etree.HTML(response)
                        # 使用XPath选择指定div下的所有文本节点
                        texts = tree.xpath('/html/body/div[2]/div/div[2]/div/div[3]/div//text()')

                        # 过滤并清理文本
                        clean_texts = [text.strip() for text in texts if text.strip()]

                        if clean_texts:
                            print(f"请求成功，序号: {serial_number}, URL: {url}")
                            
                            break
                        else:
                            print(f"未提取到文本，序号: {serial_number}, URL: {url}，重试第 {attempt + 1} 次")
                    else:
                        print(f"请求失败，序号: {serial_number}, URL: {url}，重试第 {attempt + 1} 次")
                    time.sleep(5)
                
                if not response or not clean_texts:
                    print(f"最终请求失败，序号: {serial_number}, URL: {url}")
                    with open(f'data/{types[index]}/failed_requests1.csv', 'a', encoding='utf-8', newline='') as failed_file:
                        writer = csv.writer(failed_file)
                        writer.writerow([serial_number, url])
                    continue

                # 将所有文本写入文件，每行一个文本
                with open(f'data/{types[index]}/content/output_{serial_number}.txt', 'w', encoding='utf-8') as output_file:
                    for text in clean_texts:
                        output_file.write(text + '\n')