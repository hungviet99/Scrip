import logging
import os, time
import subprocess, select
import requests

log = logging.getLogger('wpalert')
log.setLevel(logging.INFO)

# token and message id

#TOKEN = ""
#CHAT_ID = 

# hostname
HOSTNAME = os.popen('hostname').read()

# Su dung tail de doc file
def poll_logfile(filename):

    f = subprocess.Popen(["tail", "-f", "-n", "0", filename], encoding="utf8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    while True:
        if p.poll(1):
            process_log_entry(f.stdout.readline())
        time.sleep(1)

# Kiem tra logline phu hop voi noi dung can tim
def process_log_entry(logline):

    if ('GET /wp-admin/ HTTP/2.0') in logline:
        if '200' in logline:
            send_sms(logline)
    elif ('GET /wp-admin/ HTTP/1.1') in logline:
        if '200' in logline: 
            send_sms(logline)
    return

# Gui canh bao ve telegram
def send_sms(msg):

    response = requests.post(
        "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Wordpress Accepted From : {} \n{}"
        .format(TOKEN, CHAT_ID, HOSTNAME, msg))

# main
if __name__ == "__main__":
#        poll_logfile("")