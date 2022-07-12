# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
num_nickname = 2300
chrome_options = Options()
chrome_options.add_argument("--headless")
base_url = "https://www.bzcm88.com/wangming/"
driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options,
                          service_args=['--load-images=no'])
driver.get(base_url)
nickname = []
count = 0
i = 1
select = 1
while len(nickname) < num_nickname:
    time.sleep(1)
    tt = len(nickname)
    next_page = driver.find_element_by_xpath("//div[@class='article']/form/input")
    next_page.click()
    nick_str = re.findall('<span>.+</span>', driver.page_source)[2]
    nick_list = re.split('<span>|</span>', nick_str, maxsplit=0)[1::2]
    nickname.extend(nick_list)
    nickname = list(set(nickname))
    logging.info(len(nickname))
    if len(nickname) == tt:
        count += 1
    else:
        count = 0
    if count == 10 & select == 10:
        exec('next_type = driver.find_element_by_xpath("//div[@class=\'recomnav\']/a[' + str(i) + ']")')
        next_type.click()
        logging.info('Next type')
        i += 1
        select = 1
        count = 0
    elif count == 10:
        select += 1
        exec('next_style = driver.find_element_by_xpath("//div[@class=\'article\']/form/label/select/option[' + str(select) + ']")')
        next_style.click()
        logging.info('Next style')
        count = 0
driver.close()
nickname = nickname[:num_nickname]
nickname = [name+'\n' for name in nickname]
with open(r'resource\nickname.txt', "w") as file:
    file.writelines(nickname)
