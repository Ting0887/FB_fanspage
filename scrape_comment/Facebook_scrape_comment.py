from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import json
from element_convert import handle_datetime,json_output

all_data = []
def login_fb():
    #FB login
    login_url = 'https://www.facebook.com/'
    browser.get(login_url)
    browser.find_element(By.ID, "email").send_keys('yanglu0518@yahoo.com') #input account
    browser.find_element(By.ID, "pass").click()
    browser.find_element(By.ID, "pass").send_keys('chizuru0518') #input password
    browser.find_element(By.NAME, "login").click()

def scrape(url):
    pid = 1
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    
    #hashtag
    tag = []
    soup = BeautifulSoup(browser.page_source,'lxml')
    try:
        hashtag = soup.find_all('a','oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl q66pz984 gpro0wi8 b1v8xokw')
        for h in hashtag:
            tag.append(h.text)
    except:
        pass
    
    #click more comment
    try:
        element = browser.find_elements_by_xpath("//div[@class='cwj9ozl2 tvmbv18p']")[0]
        more_comment = element.find_elements_by_xpath("//span[@class='j83agx80 fv0vnmcu hpfvmrgz']")
        for e in more_comment:
            print(e.text)
            browser.execute_script("arguments[0].click()",e)
    except Exception as e:
        print(e)
        pass
    #click more
    try:
        element = browser.find_elements_by_xpath("//div[@class='cwj9ozl2 tvmbv18p']")[0]
        more_comment = element.find_elements_by_xpath("//div[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p']")
        for m in more_comment:
            print(m.text)
            browser.execute_script("arguments[0].click()",m)
    except Exception as e:
        print(e)
        pass
    
    #scrape comment
    soup = BeautifulSoup(browser.page_source,'lxml')
    all_comments = soup.find_all('div','rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc')
    comment_data = []
    for c in all_comments:
        try:
            comment_name = c.find('span','nc684nl6').text
        except:
            comment_name = ''
        try:
            p_link = c.find('a','oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8')['href']
            if '&comment_id=' in p_link:
                profile_link = p_link.split('&comment_id=')[0]
            elif '?comment_id=' in p_link:
                profile_link = p_link.split('?comment_id=')[0]
            else:
                profile_link = ''
        except:
            profile_link = ''
        try:
            comment_text = c.find('div','kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql').text
        except:
            comment_text = ''
        try:
            comment_time = c.find('a','oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl m9osqain gpro0wi8 knj5qynh').text
        except:
            comment_time = ''
        comment_time = handle_datetime(comment_time)
        
        comment_data.append({'comment_name':comment_name,
                             'profile_link':profile_link,
                             'comment_time':comment_time,
                             'comment_text':comment_text})
        
        #print(comment_name,comment_text,comment_time)
    #scrape reply
    soup = BeautifulSoup(browser.page_source,'lxml')
    reply_bar = soup.find_all('div','kvgmc6g5 jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso')
    reply_data = []
    for r in reply_bar:
        all_reply = r.find_all('div','rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc')
        for r in all_reply:
            try:
                reply_name = r.find('span','pq6dq46d').text
            except:
                reply_name = ''
            try:
                p_link = c.find('a','oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8')['href']
                if '&comment_id=' in p_link:
                    profile_link = p_link.split('&comment_id=')[0]
                elif '?comment_id=' in p_link:
                    profile_link = p_link.split('?comment_id=')[0]
                else:
                    profile_link = ''
            except:
                profile_link = ''
            try:
                reply_text = r.find('div','kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql').text
            except:
                reply_text = ''
            try:
                reply_time = r.find('a','oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl m9osqain gpro0wi8 knj5qynh').text
            except:
                reply_time = ''
            reply_time = handle_datetime(reply_time)
            
            reply_data.append({'reply_name':reply_name,
                               'profile_link':profile_link,
                               'reply_time':reply_time,
                               'reply_text':reply_text})
   
    all_data.append(json_output(pid,source,tag,url,comment_data,reply_data))
    print(all_data)
    pid += 1

       

if __name__ == '__main__':
 
    driverPath = 'c:\\users\lutin\chromedriver.exe'
    #chromedriver setting
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # if you don't want to open browser, add 18th line 
    #chrome_options.add_argument("--headless")
    
  

    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
   
    #chrome_options.add_argument("--disable-javascript") 
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--in-process-plugins")
    chrome_options.add_argument('--no-sandbox')

    
    
    ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    chrome_options.add_argument("user-agent={}".format(ua))
    
    browser = webdriver.Chrome(driverPath,options=chrome_options)
    login_fb()
    time.sleep(1)
    with open('1614154305476347_2021-06-21_post.json','r',encoding='utf-8') as f:
        for item in json.load(f):
            source = item['source']
            url = item['link'].replace('//m','//www')
            scrape(url)