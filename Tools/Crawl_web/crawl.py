import requests
import re
from bs4 import BeautifulSoup
import redis
import unidecode
import config

re = requests.get(config.LINK_WEB)
html_raw = re.text

def crawl_link(html):
    lists=[]
    soup = BeautifulSoup('{}' .format(html), 'html.parser')
    artical = soup.find_all('article')
    for i in artical:  
        id_name = i.get('id')  
        author = i.find_all(class_="post-author")
        href_name = i.a.get('href')
        for i in author:
            title_name = i.a.get('title')
            auth_name= title_name[9:]
            auth_link = i.a.get('href')
            auth = (id_name, href_name, auth_name, auth_link)
            lists.append(auth)
    return lists

def info_web(list_id, token, chat_id):
    lists_key = []
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
    list_byte_key = redis_db.keys()
    for i in list_byte_key:
        cv_str = i.decode("utf-8")
        lists_key.append(cv_str)
    for i in list_id:
        post_id = i[0] 
        post_link = i[1] 
        author = i[2] 
        post_auth = unidecode.unidecode(author) 
        auth_link = i[3]
        if post_id not in lists_key:
            dict_a = {"id_post": post_id, "link_post": post_link,
                     "auth_post": post_auth, "link_auth": auth_link}
            redis_db.hmset(post_id, dict_a)
            redis_db.
            requests.get(
                "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text= {}&parse_mode=Markdown"
                .format(token, chat_id, post_link))
    return

if __name__ == "__main__":
    list_inf_id = crawl_link(html_raw)

    info_web(list_inf_id, config.TOKEN, config.CHAT_ID)