import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json

#chromedriver setting
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
# if you don't want to open browser, add 18th line 
#chrome_options.add_argument("--headless")

prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option('prefs', prefs)
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096, 'intl.accept_languages': 'en-US'}
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('blink-settings=imagesEnabled=false') 
chrome_options.add_argument("--disable-javascript") 
chrome_options.add_argument("--disable-images")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--in-process-plugins")
chrome_options.add_argument('--no-sandbox')


ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
chrome_options.add_argument("user-agent={}".format(ua))
driverPath = 'c:\\users\csr\chromedriver.exe'
browser = webdriver.Chrome(driverPath,chrome_options=chrome_options)
browser.set_window_size('900','800')

#read credentials
user = []
passw_f = 'credentials.txt'
with open(passw_f,'r') as f:
    for line in f:
        a = line.split('=')[1].split('"')[1]
        user.append(a)
    
#FB login
login_url = 'https://upload.facebook.com/'
browser.get(login_url)
browser.find_element(By.ID, "email").send_keys(user[0]) #input account
browser.find_element(By.ID, "pass").click()
browser.find_element(By.ID, "pass").send_keys(user[1]) #input password
browser.find_element(By.ID, "u_0_b").click()

time.sleep(3)

def fb_scrape():
    #from all fb_fans_link to parse data
    file1 = 'm_follow.txt'
    with open(file1,'r',encoding='utf8') as f:
        for links in f:
            link = links.replace('\n','')
            file_name = links.split('/')[-1].replace('\n','')
            
            browser.get(link)
            soup = BeautifulSoup(browser.page_source,'lxml')
           
          
            #some links can't change to phone link
            if 'www' in browser.current_url:
                link = browser.current_url.replace('www','m')
                browser.get(link)
                soup = BeautifulSoup(browser.page_source,'lxml')
                [x.extract() for x in soup.findAll(['script'])]

            #if 404 link, write into notparselink.txt 
            try:
                ele = soup.find('div','_7nyw').text
                if '你點擊進來的連結可能已失效' in ele:
                    with open('notparselink.txt','a',encoding='utf8') as f:
                        f.write(link)
                        f.write('\n')
                    continue
            except:
                print('link is ok')
            
            #if '載入中' in page ,write into notparselink.txt
            try:
                ele = soup.find('div','_39jv').text
                if '載入中……' in ele:
                   with open('notparselink.txt','a',encoding='utf8') as f:
                        f.write(link)
                        f.write('\n')
                   continue
            except:
                print('link is ok')
                
            #if Sorry, something went wrong in page,write into notparselink.txt
            try:
                ele = soup.find('div','area error').strong.text
                if 'Sorry, something went wrong.' in ele:
                   with open('notparselink.txt','a',encoding='utf8') as f:
                        f.write(link)
                        f.write('\n')
                   continue
            except:
                print('link is ok')
                
                
            
                
            js = 'window.scrollTo(0, document.body.scrollHeight)'
            browser.execute_script(js)
                   
            postlist = soup.select('._55wo')
            postN = len(postlist)
            
            last_height = browser.execute_script("return document.body.scrollHeight")
            #when post > 2 break
            while postN < 2:
                browser.execute_script(js)
                time.sleep(2)
                browser.execute_script('videos = document.querySelectorAll("video"); for(video of videos) {video.pause()}')
                soup = BeautifulSoup(browser.page_source,'lxml')
                postlist = soup.select('._55wo')
                postN = len(postlist)
                print(postN)
                
                #if scroll down to bottom
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            # if no posts, continue
            if postN == 1:
                with open('notparselink.txt','a',encoding='utf8') as f:
                    f.write(link)
                    f.write('\n')
                continue
            
            
            last_height = browser.execute_script("return document.body.scrollHeight")
            while True:
                try:
                    browser.execute_script(js)
                    soup = BeautifulSoup(browser.page_source,'lxml')   
                    postlist = soup.select('._55wo')
                    for post in postlist:
                        try:
                            post_time = post.find('abbr').text                     
                        except:
                            pass
                    time.sleep(3)
    
                    post_time = soup.find_all('abbr')[-1].text
                    print(post_time)
                    
                    if post_time.startswith('2019') or\
                       post_time.startswith('2018') or\
                       post_time.startswith('2017') or\
                       post_time.startswith('2016') or\
                       post_time.startswith('2015') or\
                       post_time.startswith('2014') or\
                       post_time.startswith('2013') or \
                       post_time.startswith('2012') or\
                       post_time.startswith('2011') or\
                       post_time.startswith('2010') :
                        break             
                    #if scroll down to bottom
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                except Exception as e:
                    pass
     
            
            #scrape fans page post
            articlelist = []
            num = 1
            for post in postlist:              
                time.sleep(0.5)
                
                pid = num
                
                #source(fans page name)
                try:
                    source = post.find('h3',{'data-gt':'{"tn":"C"}'}).strong.text
                except:
                    source = ''
                    
                #datetime
                try:                   
                    date_time = post.find('abbr').text
                    if '年' in date_time:
                        date_time = post.find('abbr').text
                    elif '時' in date_time:
                        date_time = time.strftime('%Y年%m月%d日')
                    elif '分' in date_time:
                        date_time = time.strftime('%Y年%m月%d日')
                    elif '秒' in date_time:
                        date_time = time.strftime('%Y年%m月%d日')
                    elif '昨' in date_time:
                        date_time = time.strftime('%Y年%m月%d日')
                    else:
                        date_time = time.strftime('%Y年') + post.find('abbr').text
                except:
                    date_time = ''
        
                #likes total
                try:
                    likes = post.find('div','_1g06').text.replace(',','')
                    if '萬' in likes:
                        likes = int(float(re.findall(r'\d+\.\d+',likes)[0])*10000)
                    elif '人' in likes:
                        likes = re.findall(r'\d+',likes)[0]
                    else:
                        likes = post.find('div','_1g06').text.replace(',','')
                except:
                    likes = '0'
                
                #comments total
                try:
                    comment_count = post.find('span',{'data-sigil':'comments-token'}).text.replace(',','').replace('則留言','')
                    if '萬' in comment_count:
                        comment_count = int(float(comment_count[:-2])*10000)
                    else:
                        comment_count = post.find('span',{'data-sigil':'comments-token'}).text.replace(',','').replace('則留言','')
                except:
                    comment_count = '0'

                
                #shares count
                try:
                    share_count = post.find_all('span','_1j-c',string = re.compile('次分享$'))[0].text.replace(',','').replace('次分享','')
                    if '萬' in share_count:
                        share_count = int(float(share_count[:-2]*10000))
                    else:
                        share_count = post.find_all('span','_1j-c',string = re.compile('次分享$'))[0].text.replace(',','').replace('次分享','')
                except:
                    share_count = '0'
                
                
                #scrape content
                #more content clink
                try:
                    ele = browser.find_element_by_xpath("//span[data-sigil='more']").click()
                except:
                    pass
                
                time.sleep(0.5)
                    
                try:
                    article_content = post.find('div','_5rgt _5nk5 _5msi').text.replace('… 更多','')
                except:
                    article_content = ''
                    
                try:
                    link = 'https://m.facebook.com' + post.find('a','_5msj')['href'].replace('&substory_index=0','')
                    link = link.split('&')[0] + '&' + link.split('&')[1] 
                except:
                    link = ''
                    
                article = {'pid':pid,
                           'source':source,
                           'date_time':date_time,
                           'total_like':likes,
                           'share_count':share_count,
                           'comment_count':comment_count,
                           'article_content':article_content,
                           'link':link}
                
                #print(article)
             
                
                # if datetime and link is null,don't append them
                if date_time == "" or link == "":
                    continue
                else:
                    articlelist.append(article)
                    num += 1
                    print('第',pid,'筆資料已經完成')
            #write to json file
            file = file_name + '_post.json'
            with open(file,'w',encoding='utf8') as f:
                json.dump(articlelist,f,ensure_ascii=False,indent=2)
            f.close()   
fb_scrape()