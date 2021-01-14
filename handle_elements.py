import re
import time
import datetime
def handle_likes(likes):
     if '萬' in likes:
         likes = int(float(re.findall(r'\d+\.\d+',likes)[0])*10000)
     elif '人' in likes:
         likes = re.findall(r'\d+',likes)[0]
    
     return likes

def handle_comment(comment_count):
    if '萬' in comment_count:
        comment_count = int(float(comment_count[:-2])*10000)
    
    return comment_count

def handle_share(share_count):
     if '萬' in share_count:
         share_count = int(float(share_count[:-2]*10000))
     return share_count

def handle_posttime(post_time):
    if '年' in post_time:
        d = re.findall(r'\d+',post_time)
        post_time = datetime.date(int(d[0]),int(d[1]),int(d[2]))
        post_time = post_time.strftime('%Y年%m月%d日')
    elif '分'  in post_time:
        post_time = time.strftime('%Y年%m月%d日')
    elif '秒' in post_time:
        post_time = time.strftime('%Y年%m月%d日')
    elif '昨' in post_time:
        post_time = time.strftime('%Y年%m月%d日')
    else:
        post_time = time.strftime('%Y年') + post_time
        d = re.findall(r'\d+',post_time)
        p = datetime.date(int(d[0]),int(d[1]),int(d[2]))
        post_time = p.strftime('%Y年%m月%d日')
    return post_time