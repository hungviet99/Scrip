import shodan
import requests
import telebot
import re
import json
import config

bot = telebot.TeleBot(config.TOKEN)

api = shodan.Shodan(config.ApiKeyShodan) 

# Hiển thị những port đang mở
def list_port(ipaddr):

    """
    Hàm trả về giá trị là thông tin của 1 Port khi truyền vào IP bằng cách sử dụng API của shodan
    để lấy dữ liệu về port, các giao thức và dịch vụ trên port đó.   
    """

    ipinfo = api.host(ipaddr)
    infData = ipinfo['data']
    InfoPort = "**" + 'Port' + " : " + 'Service' + " : " + 'Protocol' + "**" + '\n'
    try: 
        for data in infData: 
            Port = str(data['port'])
            Service = str(data['_shodan']['module'])
            Protocol = str(data['transport'])
            InfOutPut = "`" + Port + " : " + Service + " : " + Protocol + "`"
            InfoPort = InfoPort + "\n" + InfOutPut + '\n' 
    except:
        InfoPort = "Lỗi Port"
    return InfoPort

def list_reverseIP(ipaddr):

    """
    Sử dụng API của hackertarget để lấy dữ liệu về A record đang trỏ đến địa chỉ IP đó
    """
    try : 
        checksite = requests.get("https://api.hackertarget.com/reverseiplookup/?q={}".format(ipaddr))
        site=checksite.text
    except: 
        site = "Hết lượt truy xuất !!"
    return site

# Lấy thông tin của IP
def info_ip(ipaddr):

    """
    Sử dụng API của rapidapi 
    Truyền vào địa chỉ IP sau đó hàm trả về thông tin người sở hữu địa chỉ IP đó
    """

    payload = {"format":"json","domain":"{}" .format(ipaddr)}
    response1 = requests.request("GET", config.url, params=payload, headers=config.headers)
    InfIP = response1.json()
    ContactName = InfIP['contacts']['admin'][0]['name']
    ContactAddr = InfIP['contacts']['admin'][0]['address']
    ContactPhone = InfIP['contacts']['admin'][0]['phone']
    INFO_IP = 'Người sở hữu: ' + ContactName + '\n\n' 
    INFO_IP = INFO_IP + 'Địa Chỉ : ' + ContactAddr + '\n\n' 
    INFO_IP = INFO_IP + 'Số điện thoại: ' + ContactPhone
    return INFO_IP

# Lấy thông tin về domain
def info_domain(domain):

    """
    Sử dụng API của rapidapi
    Truyền vào 1 domain, hàm sẽ trả về thông tin của domain. 
    """
    payload = {"format":"json","domain":"{}" .format(domain)}
    response2 = requests.request("GET", config.url, params=payload, headers=config.headers)
    InfDomain = response2.json()
    IPS = InfDomain['ips']
    Domain = InfDomain['name']
    try: 
        DNS = InfDomain['nameserver']
        Create = InfDomain['created']
        Expires = InfDomain['expires']
        Registrar = InfDomain['registrar']['name']
    except:
        DNS = ' '
        Create = ' '
        Expires = ' '
        Registrar = ' '
    INFO_DOMAIN ='Domain: ' + Domain + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'IPS: ' + IPS + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'Name Server: ' + str(DNS) + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'Nhà đăng ký: ' + Registrar + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'Ngày tạo: ' + Create + '\n\n' 
    INFO_DOMAIN = INFO_DOMAIN + 'Ngày hết hạn: ' + Expires 
    return INFO_DOMAIN

# Reply hướng dẫn
@bot.message_handler(commands=["start"])
def send_welcome(message):
    """
    Hàm mô tả các hướng dẫn để thao tác với bot trên telegram
    """
    bot.reply_to(message, "Nhập vào /port <IP> để xem port. VD: /port 10.10.10.10"+ '\n\n' +
        "Nhập vào /reverseip <IP> để xem những tên miền đang trỏ đến IP. VD: /reverseip 10.10.10.10" + '\n\n' +
        "Nhập vào /info <IP> để xem thông tin người sở hữu. VD: /info 10.10.10.10" + '\n\n' +
        "Nhập vào /info <domain> để xem thông tin của domain. VD: /info hungnv99.com", parse_mode='Markdown')

# Regex địa chỉ IP
ReIP = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

if __name__ == "__main__":

    # Tạo lệnh check port 
    @bot.message_handler(commands=["port"])
    def check_port(message):

        """
        Hàm sẽ lấy ra địa chỉ IP được nhập vào, sau đó sẽ gọi lại hàm list_port 
        và truyền địa chỉ IP vào đó. Hàm trả về kết quả sẽ lấy kết quả và gửi về telegram
        """
        IP = message.text[6:]
        SameIP = ReIP.match(IP)
        if SameIP :
            port = list_port(IP)
            string_port  = str(port)
            sendMessage = bot.reply_to(message, string_port, parse_mode='Markdown')
        else:
            sendMessage = bot.reply_to(message, "Không Phải địa chỉ IP", parse_mode='Markdown')

    @bot.message_handler(commands=["reverseip"])
    def check_RevIP(message):
        IP = message.text[11:]
        SameIP = ReIP.match(IP)
        if SameIP :
            revip = list_reverseIP(IP)
            string_revip = str(revip)
            if len(string_revip) > 4096: 
                for x in range(0, len(string_revip), 4096):
                    sendMessage = bot.reply_to(message, string_revip[x:x+4096], parse_mode='Markdown')
            else:
                sendMessage = bot.reply_to(message, string_revip, parse_mode='Markdown')
        else:
            sendMessage = bot.reply_to(message, "Không Phải địa chỉ IP", parse_mode='Markdown')

    @bot.message_handler(commands=["info"])
    def check_info(message):
        IP_Domain = message.text[6:]
        SameIP = ReIP.match(IP_Domain)
        print(IP_Domain)
        if SameIP: 
            mess = info_ip(IP_Domain)
            string_infip = str(mess)
            sendMessage = bot.reply_to(message, string_infip, parse_mode='Markdown')
        else: 
            mess = info_domain(IP_Domain)
            string_infdomain = str(mess)
            sendMessage = bot.reply_to(message, string_infdomain, parse_mode='Markdown')
    bot.polling()


#def list_cve(ipaddr):
#    ipinfo = api.host(ipaddr)
#    listcve=[]
#    try:
#        for item in ipinfo['vulns']:
#            CVE = item.replace('!','')
#            listcve.append(item)
#    except:
#        response = requests.post("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Không có CVE".format(TOKEN, CHAT_ID))
#    return listcve

# Hiển thị những tên miền đang trỏ đến địa chỉ IP 


    #os = str(data['os'])
    #if os == 'None':
    #    OS = OS + ''
    #else: 
    #    OS = OS + os
    #InfoPort = InfoPort + '\n' + InfOutPut 