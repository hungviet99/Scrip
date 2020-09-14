import requests
import re
from bs4 import BeautifulSoup
import redis
import unidecode
import config

# Get html 
re = requests.get(config.LINK_WEB)
html_raw = re.text

def crawl_web(html):
    """Lấy thông tin web
    :param html: là đoạn html get được từ trang web cần lấy thông tin. 

    :response: trả về danh sách các thông tin như: 
               id post, post link, author name, author link. 
    """
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

def write_data_redis(list_if, token, chat_id):
    """Xử lý dữ liệu và ghi vào redis
    :param list_if: là list thông tin về:
                    id post, link post, author name, author link.

    :param token,chat_id: Truyền vào token bot và chatid của telegram.
    
    :response: Xử lý dữ liệu ghi vào redis,
                nếu có dữ liệu mới thì gửi lên telegram.
    """
    lists_key = []
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
    list_byte_key = redis_db.keys()
    for i in list_byte_key:
        cv_str = i.decode("utf-8")
        lists_key.append(cv_str)
    for i in list_if:
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
    list_inf_web = crawl_web(html_raw)

    write_data_redis(list_inf_web, config.TOKEN, config.CHAT_ID)