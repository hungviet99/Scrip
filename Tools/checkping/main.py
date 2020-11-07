import telebot
from checkping import packet_1, packet_2, packet_3, packet_4, packet_5, packet_avg, main 
import config

bot = telebot.TeleBot(config.TOKEN_TELE)

@bot.message_handler(commands=["start"])
def send_devices(message):
    """
    Tạo lệnh start để hướng dẫn sử dụng
    """
    bot.reply_to(message, "Nhập vào /ping <hosts> " +
                        "để xem thông tin. VD: /ping 10.10.10.10")

if __name__ == "__main__":
    @bot.message_handler(commands=["ping"])
    def send_subdomain(message):
        """
        Tạo lệnh để truyền vào host từ telegram
        """
        hosts = message.text[6:]
        results = main(hosts)
        str_rtt = packet_avg(results, hosts)
        if not results[hosts]['icmp_replies']:
            bot.reply_to(message, "Request timed out!!" + "\n\n" + str(str_rtt))
        elif len(results[hosts]['icmp_replies']) == 1:
            Str1 = packet_1(results, hosts)
            bot.reply_to(message, str(Str1) + "\n\n" + str(str_rtt))
        elif len(results[hosts]['icmp_replies']) == 2:
            Str1 = packet_1(results, hosts)
            Str2 = packet_2(results, hosts)
            bot.reply_to(message, str(Str1) + "\n" + str(Str2) +
                             "\n\n" + str(str_rtt))
        elif len(results[hosts]['icmp_replies']) == 3:
            Str1 = packet_1(results, hosts)
            Str2 = packet_2(results, hosts)
            Str3 = packet_3(results, hosts)
            bot.reply_to(message, str(Str1) + "\n" + str(Str2) +
                             "\n" + str(Str3) + "\n\n" + str(str_rtt))
        elif len(results[hosts]['icmp_replies']) == 4:
            Str1 = packet_1(results, hosts)
            Str2 = packet_2(results, hosts)
            Str3 = packet_3(results, hosts)
            Str4 = packet_4(results, hosts)
            bot.reply_to(message, str(Str1) + "\n" + str(Str2) +
                             "\n" + str(Str3) + "\n" +
                             str(Str4) + "\n\n" + str(str_rtt))
        elif len(results[hosts]['icmp_replies']) == 5:
            Str1 = packet_1(results, hosts)
            Str2 = packet_2(results, hosts)
            Str3 = packet_3(results, hosts)
            Str4 = packet_4(results, hosts)
            Str5 = packet_5(results, hosts)
            bot.reply_to(message, str(Str1) + "\n" + str(Str2) +
                             "\n" + str(Str3) + "\n" +
                             str(Str4) + "\n" + str(Str5) +
                             "\n\n" + str(str_rtt))
    bot.polling()