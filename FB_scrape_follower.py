import os
import json
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import re
import requests

def extract_follower(name,link):
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """})
    browser.get(link)
    time.sleep(2.5)
    soup = BeautifulSoup(browser.page_source,'lxml')
    #id_bar = soup.select('.sjgh65i0')[0]
    try:
        like = soup.find_all('span','d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 jq4qci2q a3bd9o3v knj5qynh oo9gr5id',string=re.compile('\d人'))[0].text
    except:
        like = ''
    try:
        follower = soup.find_all('span','d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 jq4qci2q a3bd9o3v knj5qynh oo9gr5id',string=re.compile('\d*.追蹤'))[0].text
    except:
        follower = ''
    if follower == '':
        try:
            follower = soup.find_all('a','oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p',string=re.compile('\d*.追蹤者'))[0].text
        except:
            follower  = ''
    

    print(name)
    print(follower)
    print(like)
    j_item = {'page_name':name,
              'link':link,
              'follower':follower,
              'like':like}

    with open('FB_otherpagefollower.json','a',encoding='utf8') as f:
        json.dump(j_item,f,indent=2,ensure_ascii=False)

if __name__ == '__main__':

    
    #chromedriver setting
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # if you don't want to open browser, add 18th line
    #chrome_options.add_argument("--headless")

    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--in-process-plugins")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    chrome_options.add_argument("user-agent={}".format(ua))
    driverPath = "/home/tingyang0518/chromedriver"
    browser = webdriver.Chrome(driverPath,chrome_options=chrome_options)

    #FB login
    login_url = 'https://upload.facebook.com/'
    browser.get(login_url)
    browser.find_element(By.ID, "email").send_keys(input('account : ')) #input account
    browser.find_element(By.ID, "pass").click()
    browser.find_element(By.ID, "pass").send_keys(input('password: ')) #input password
    browser.find_element(By.NAME,"login").click()
    time.sleep(2)
    with open('FB_notparselink.json','r',encoding='utf8') as f:
        r = json.load(f)
        for item in r:
            name = item['page_name']
            #link = 'https://www.facebook.com/' + str(item['page_id'])
            link = item['link']
            extract_follower(name,link)
