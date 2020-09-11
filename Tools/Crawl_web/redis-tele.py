import telebot
import redis
import config

bot = telebot.TeleBot(config.TOKEN_TELE)

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

result = []
cur,key=redis_db.scan(cursor=0, count=10)
result.extend(key)

lists_key = []
for i in result:
    cv_str = i.decode("utf-8")
    lists_key.append(cv_str)

list_auth = []
for i in lists_key:
    a = redis_db.hget(i, "auth_post")
    auth = a.decode("utf-8")
    list_auth.append(auth)

link_auth = []
for i in lists_key:
    b = redis_db.hget(i, "link_auth")
    link = b.decode("utf-8")
    link_auth.append(link)

author = []
for x in list_auth:
    if x not in author:
        author.append(x)

@bot.message_handler(commands=["author"])
def send_devices(message):
    for a in author:
        bot.send_message(config.CHAT_ID, a ,parse_mode='Markdown')

@bot.message_handler(commands=["post"])
def send_devices(message):
    for i in lists_key:
        a = redis_db.hget(i, "link_post")
        auth = a.decode("utf-8")
        bot.send_message(config.CHAT_ID, str(auth) ,parse_mode='Markdown')
@bot.message_handler(commands=["link"])
def send_devices(message):
    bot.send_message(config.CHAT_ID, str(link_auth) ,parse_mode='Markdown')

bot.polling()