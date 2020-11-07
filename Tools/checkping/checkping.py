import os
import pingparsing
import json
import telebot

def check_ping(hosts):
    """
    pingparsing sử dụng các option 
    """
    a = os.popen('pingparsing '+ hosts +' -s 56 -c 5 --icmp-reply').read()
    results = json.loads(a)
    return results

def packet_1(results, hosts):
    """
    Xử lý dữ liệu của gói thứ nhất
    """
    dicts1 = results[hosts]['icmp_replies'][0]
    ttl1 = dicts1['ttl']
    time1 = dicts1['time']
    icmp_seq1 = dicts1['icmp_seq']
    Str1 = "bytes = 64"+"   icmp_seq="+str(icmp_seq1)
    Str1 = Str1 +"   ttl="+ str(ttl1)+"   time="+str(time1)+" ms"
    return Str1

def packet_2(results, hosts):
    """
    Xử lý dữ liệu của gói thứ hai
    """
    dicts2 = results[hosts]['icmp_replies'][1]
    ttl2 = dicts2['ttl']
    time2 = dicts2['time']
    icmp_seq2 = dicts2['icmp_seq']
    Str2 = "bytes = 64"+"   icmp_seq="+str(icmp_seq2)
    Str2 = Str2 +"   ttl="+ str(ttl2)+"   time="+str(time2)+" ms"    
    return Str2

def packet_3(results, hosts):
    """
    Xử lý dữ liệu của gói thứ ba
    """
    dicts3 = results[hosts]['icmp_replies'][2]
    ttl = dicts3['ttl']
    time = dicts3['time']
    icmp_seq = dicts3['icmp_seq']
    Str3 = "bytes = 64"+"   icmp_seq="+str(icmp_seq)
    Str3 = Str3 +"   ttl="+ str(ttl)+"   time="+str(time)+" ms"
    return Str3

def packet_4(results, hosts):
    """
    Xử lý dữ liệu của gói thứ tư
    """
    dicts4 = results[hosts]['icmp_replies'][3]
    ttl = dicts4['ttl']
    time = dicts4['time']
    icmp_seq = dicts4['icmp_seq']
    Str4 = "bytes = 64"+"   icmp_seq="+str(icmp_seq)
    Str4 = Str4 +"   ttl="+ str(ttl)+"   time="+str(time)+" ms"
    return Str4

def packet_5(results, hosts):
    """
    Xử lý dữ liệu của gói thứ năm
    """
    dicts5 = results[hosts]['icmp_replies'][4]
    ttl = dicts5['ttl']
    time = dicts5['time']
    icmp_seq = dicts5['icmp_seq']
    Str5 = "bytes = 64"+"   icmp_seq="+str(icmp_seq)
    Str5 = Str5 +"   ttl="+ str(ttl)+"   time="+str(time)+" ms"
    return Str5

def packet_avg(results, hosts):
    """
    Xử lý tổng hợp dữ liệu 
    """
    rtt_min = results[hosts]['rtt_min']
    rtt_max = results[hosts]['rtt_max']
    rtt_mdev = results[hosts]['rtt_mdev']
    packet_loss_count = results[hosts]['packet_loss_count']
    packet_transmit = results[hosts]['packet_transmit']
    packet_receive = results[hosts]['packet_receive']
    packet_loss_rate = results[hosts]['packet_loss_rate']
    str_rtt =  str(packet_loss_count) + " packets loss, "
    str_rtt =  str_rtt + str(packet_transmit) + " packets transmitted, "
    str_rtt = str_rtt + str(packet_receive)+ " received, "
    str_rtt = str_rtt + str(packet_loss_rate) + "% packet loss"
    str_rtt = str_rtt + "\n"
    str_rtt = str_rtt + "rtt min/max/mdev = " + str(rtt_min)
    str_rtt = str_rtt + "/" + str(rtt_max)
    str_rtt = str_rtt + "/" + str(rtt_mdev) + " ms"
    return str_rtt

def main(hosts):
    results = check_ping(hosts)
    return results

    