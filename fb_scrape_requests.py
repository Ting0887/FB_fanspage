import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re
import os
from element_format import handle_element,json_format

class FB_Crawler:
    def __init__(self, account, password, driver_location):
        self.account = account
        self.password = password
        self.driver_location = driver_location
        self.cookies = []
        self.article = []
    def login(self):
        #driver setting
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--incognito")
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

        browser = webdriver.Chrome(self.driver_location,chrome_options=chrome_options)
        
        #login
        browser.get('https://www.facebook.com')
        time.sleep(1)
        browser.find_element_by_xpath("//input[@name='email']").send_keys(account) #input account
        browser.find_element_by_xpath("//input[@name='pass']").send_keys(password) #input password
        browser.find_element_by_css_selector("button[name='login']").click()
        time.sleep(1.5)

        #get cookies
        cookies = browser.get_cookies()
        self.cookies = cookies
        browser.close()

    def read_post_url(self,post_path,file_name):
        collect_link = []
        with open(post_path,'r',encoding='utf8') as f:
            r = json.load(f)
            for item in r:
                link = item['link'].replace('https://m','https://mbasic').replace('https://upload','https://mbasic').replace('https://wwww','https://mbasic')# I hope parse mobile link
                source = item['source']
                collect_link.append(link)

        return collect_link,source

    def crawl(self,post_path,file_name):
        self.login()

        s = requests.Session()
        
        #cookies put into session
        for cookie in self.cookies:
            s.cookies.set(cookie['name'],cookie['value'])
            print(cookie)

        self.article = []
        #headers
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
        data = self.read_post_url(post_path,file_name)

        num = 1
        
        source = data[1]

        for link in data[0]: 
            print(link)
            try:
                response = s.get(link,headers=headers)
                time.sleep(1)
                if response.status_code != 200:
                    time.sleep(60)
                    response = s.get(link,headers=headers)
            except Exception as e:
                pass
            try:
                ufi = re.findall('id="ufi_\d+', response.text)[0].split('"')[1]
                print(ufi)
                soup = BeautifulSoup(response.text,'lxml')
                bar = soup.find_all('div',id=ufi)
            except Exception as e:
                pass
            
            #pid
            pid = num

            #comment
            comment_data = []
            try:
                comment_id = re.findall('id="[0-9]+',str(bar))
                for i in comment_id:
                    id_num = i.split('"')[1]
                    all_c = soup.find_all('div',id=id_num)
                    for c in all_c:
                        try:
                            name = c.find('h3').text
                        except:
                            name = ''
                        try:
                            profile_link = 'https://m.facebook.com' + c.find('h3').a.get('href').replace('?refid=18&__tn__=R','').replace('&rc=p&refid=52&__tn__=R','').replace('?rc=p&refid=52&__tn__=R','')
                        except:
                            profile_link = ''
                        try:
                            date_time = c.find('abbr').text
                        except:
                            date_time = ''
                        date_time = handle_element().caculate_date(date_time)

                        try:
                            comment_text = c.find('div').div.text
                        except:
                            comment_text = ''
                        comment_data.append({'comment_name':name,
                                             'profile_link':profile_link,
                                             'comment_time':date_time,
                                             'comment_text':comment_text})
            except:
                print('no comment')
        

            #reply
            link_list = []
            try:
                reply_id = re.findall('id="comment_replies_more_1:\d+_\d+',str(bar))
                for r in reply_id:
                    r_num = r.split('"')[1]
                    all_reply_url = soup.find_all('div',id=r_num)
                    for a in all_reply_url:
                        r_link = 'https://mbasic.facebook.com' + a.find('a')['href']
                        link_list.append(r_link)
            except:
                print('no reply')
            
            if link_list == []:
                reply_data = []
            else:
                reply_data = []
                for reply_link in link_list:
                    try:
                        response = s.get(reply_link,headers=headers)
                        time.sleep(1)
                        if response.status_code != 200:
                            time.sleep(60)
                            response = s.get(reply_link,headers=headers)
                    except Exception as e:
                        pass

                    soup = BeautifulSoup(response.text,'lxml')
                    reply_bar = soup.find_all('div','bd')
                    for r in reply_bar[1:]:
                        try:
                            reply_name = r.find('h3').text
                        except:
                            reply_name = ''
                        try:
                            profile_link = 'https://m.facebook.com' + c.find('h3').a.get('href').replace('?refid=18&__tn__=R','').replace('&rc=p&refid=52&__tn__=R','').replace('?rc=p&refid=52&__tn__=R','')
                        except:
                            profile_link = ''
                        try:
                            reply_date = r.find('abbr').text
                        except:
                            reply_date= ''
                        reply_date = handle_element().caculate_date(reply_date)
                        try:
                            reply_comment = r.find('div').div.text
                        except:
                            reply_comment = ''
                        reply_data.append({'reply_name':reply_name,
                                           'profile_link':profile_link,
                                           'reply_time':reply_date,
                                           'reply_text':reply_comment})
                    
            #tag
            tag_list = []
            try:
                full_text = soup.find_all('div','z ba')
                tag_re = re.findall('href="/hashtag/\w+',str(full_text))
                for t in tag_re:
                    tag = t.split('/')[-1]
                    tag_list.append(tag)
            except:
                print('no tag')
            
            time.sleep(1)
            #reaction
            try:
                reaction_re = re.findall('/ufi/reaction/profile/browser/\D\w+=\d+',str(bar))[0]
                reaction_url = 'https://m.facebook.com' + reaction_re
                response = s.get(reaction_url,headers=headers)
                soup = BeautifulSoup(response.text,'lxml')
                try:
                    like = soup.find('span',{"data-store":'{"reactionType":1}'}).text.replace(',','')
                except:
                    like = '0'
                try:
                    love = soup.find('span',{"data-store":'{"reactionType":2}'}).text.replace(',','')
                except:
                    love = '0'
                try:
                    wow = soup.find('span',{"data-store":'{"reactionType":3}'}).text.replace(',','')
                except:
                    wow = '0'
                try:
                    haha = soup.find('span',{"data-store":'{"reactionType":4}'}).text.replace(',','')
                except:
                    haha = '0'
                try:
                    sad = soup.find('span',{"data-store":'{"reactionType":7}'}).text.replace(',','')
                except:
                    sad = '0'
                try:
                    angry = soup.find('span',{"data-store":'{"reactionType":8}'}).text.replace(',','')
                except:
                    angry = '0'
                try:
                    support = soup.find('span',{"data-store":'{"reactionType":16}'}).text.replace(',','')
                except:
                    support = '0'

                like = handle_element().handle_reaction(like)
                love = handle_element().handle_reaction(love)
                wow = handle_element().handle_reaction(wow)
                haha = handle_element().handle_reaction(haha)
                sad = handle_element().handle_reaction(sad)
                angry = handle_element().handle_reaction(angry)
                support = handle_element().handle_reaction(support)
            
                reaction_data = {'like':like,
                                 'love':love,
                                 'wow':wow,
                                 'haha':haha,
                                 'sad':sad,
                                 'angry':angry,
                                 'support':support}
            except Exception as e:
                reaction_data = {}
                print('no reaction')
                pass
            print(reaction_data)
            print('第{}筆資料完成'.format(pid))

            self.article.append(json_format().data_form(pid,source,tag_list,link,reaction_data,comment_data,reply_data))        
            num += 1

    def save_json(self,post_path,file_name):
        file = file_name + '_' + time.strftime('%Y-%m-%d') + '_comment' + '.json'
        with open(dirpath + '/' + file,'w',encoding='utf8') as f:
            json.dump(self.article,f,ensure_ascii=False,indent=2)

if __name__ == '__main__':
    #absolute path
    dirpath = os.path.dirname(os.path.abspath(__file__))

    #user info
    account = input('account:')
    password = input('password:')
    driver_location = '/home/tingyang0518/chromedriver'

    #read fb_post_path.txt
    FB = FB_Crawler(account=account,password=password,driver_location=driver_location)
    with open('fb_post_path.txt','r') as f:
        for p in f:
            post_path = p.replace('\n','')
            file_name = p.replace('\n','').split('/')[-1].split('_')[0]
            FB.crawl(post_path,file_name)
            FB.save_json(post_path,file_name)
    
