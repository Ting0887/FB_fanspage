import requests
import re
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from set_driver import driver_setting
from output_sample import json_output
from handle_elements import handle_likes,handle_share,handle_comment,handle_posttime
import time
import json

def read_fb_account():
    #read credentials
    user = []
    passw_f = 'credentials.txt'
    with open(dirpath + '/' + passw_f,'r') as f:
        for line in f:
            a = line.split('=')[1].split('"')[1]
            user.append(a)
        return user
    
def login_fb():
    #FB login
    login_url = 'https://upload.facebook.com/'
    browser.get(login_url)
    browser.find_element(By.ID, "email").send_keys(read_fb_account()[0]) #input account
    browser.find_element(By.ID, "pass").click()
    browser.find_element(By.ID, "pass").send_keys(read_fb_account()[1]) #input password
    browser.find_element(By.ID, "u_0_b").click()
    
def scroll_down(link):
    js = 'window.scrollTo(0, document.body.scrollHeight)'
    browser.execute_script(js)
    soup = BeautifulSoup(browser.page_source,'lxml')               
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
              continue
           
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
         try:
             browser.set_script_timeout(10)
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
             post_time = handle_posttime(post_time)
             print(post_time)
                
             if post_time < '2020年01月01日':
                 break             
             #if scroll down to bottom
             new_height = browser.execute_script("return document.body.scrollHeight")
             if new_height == last_height:
                 break
             last_height = new_height
         except Exception as e:
             pass
    browser.refresh()
    return postlist

def scrape(link):
     #scrape fans page post
     articlelist = []
     num = 1
     for post in scroll_down(link):              
         #time.sleep(0.5)
         
         pid = num
                
         #source(fans page name)
         try:
             source = post.find('h3',{'data-gt':'{"tn":"C"}'}).strong.text
         except:
             source = ''
                    
         #datetime
         try:                   
             date_time = post.find('abbr').text
         except:
             date_time = ''            
         date_time = handle_posttime(date_time)    
         #likes total
         try:
             likes = post.find('div','_1g06').text.replace(',','')
         except:
             likes = '0'
         likes = handle_likes(likes)
                
         #comments total
         try:
             comment_count = post.find('span',{'data-sigil':'comments-token'}).text.replace(',','').replace('則留言','')
         except:
             comment_count = '0'
         comment_count = handle_comment(comment_count)
            
         #shares count
         try:
             share_count = post.find_all('span','_1j-c',string = re.compile('次分享$'))[0].text.replace(',','').replace('次分享','')
         except:
             share_count = '0'
         share_count = handle_share(share_count)
                
         #scrape content
         try:
             article_content = post.find('div','_5rgt _5nk5 _5msi').text.replace('… 更多','')
         except:
             article_content = ''
                    
         try:
            post_link = 'https://m.facebook.com' + post.find('a','_5msj')['href'].replace('&substory_index=0','')
            post_link = post_link.split('&')[0] + '&' + post_link.split('&')[1] 
         except:
            post_link = ''
                    
         article = json_output(pid,source,date_time,likes,share_count,comment_count,article_content,post_link)
         
         # if datetime and link is null,don't append them
         if date_time == "" or post_link == "":
             continue
         else:
             articlelist.append(article)
             num += 1
           #  print('第',pid,'筆資料已經完成')
         #print(article)

     return articlelist
def write_to_json(link):
     file = file_name +'_' + time.strftime('%Y-%m-%d')+ '_post.json'
     with open(dirpath+'/'+file,'w',encoding='utf8') as f:
         json.dump(scrape(link),f,ensure_ascii=False,indent=2)
     f.close()   
    

if __name__ == '__main__':

    #absoulte path
    dirpath = os.path.dirname(os.path.abspath(__file__))
  
    driverPath = 'c:\\users\csr\chromedriver.exe'
    browser = webdriver.Chrome(driverPath,chrome_options=driver_setting())
    browser.set_window_size('900','800')
    
    login_fb()
    time.sleep(3)
    #from all fb_fans_link to parse data
    file1 = 'm_follow.txt'
    with open(dirpath+'/'+file1,'r',encoding='utf8') as f:
        for links in f:
            link = links.replace('\n','')
            file_name = links.split('/')[-1].replace('\n','')
            browser.get(link)
            print(link)
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
                    continue
            except:
                print('link is ok')

            #if '載入中' in page ,write into notparselink.txt
            try:
                ele = soup.find('div','_39jv').text
                if '載入中……' in ele:
                    continue
            except:
                print('link is ok')

            #if Sorry, something went wrong in page,write into notparselink.txt
            try:
                ele = soup.find('div','area error').strong.text
                if 'Sorry, something went wrong.' in ele:
                    continue
            except:
                print('link is ok')

            complete_link = 'complete.txt'
            with open(dirpath+'/'+complete_link,'a',encoding='utf-8') as f:
                 f.write(link)
                 f.write('\n')

            write_to_json(link)
            
