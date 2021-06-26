import datetime
import re
import time
def handle_datetime(post_time):  
    today = datetime.datetime.today()
    if '週' in post_time:
        num = int(re.findall('\d+',post_time)[0])
        d = datetime.timedelta(weeks=num)
        post_time = (today - d).strftime('%Y-%m-%d')
        
    elif '天'  in post_time:
        num = int(re.findall('\d+',post_time)[0])
        d = datetime.timedelta(days=num)
        post_time = (today - d).strftime('%Y-%m-%d')

    elif '年' in post_time:
        num = int(re.findall('\d+',post_time)[0])
        d = datetime.timedelta(days=365*num)
        post_time = (today - d).strftime('%Y-%m-%d')
    else:
        post_time = time.strftime('%Y-%m-%d')
    return post_time

def json_output(pid,source,tag,link,comment,reply):
    sample = {'pid':pid,
              'source':source,
              'link':link,
              'comment':comment,
              'reply':reply}
    
    return sample
