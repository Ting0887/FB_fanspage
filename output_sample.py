def json_output(pid,source,date_time,likes,share_count,comment_count,article_content,post_link):
    sample = {'pid':pid,
              'source':source,
              'date_time':date_time,
              'total_like':likes,
              'share_count':share_count,
              'comment_count':comment_count,
              'article_content':article_content,
              'link':post_link}
    
    return sample