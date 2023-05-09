import re
import os
from datetime import datetime
# DEMO import hvac
# DEMO from hvac_token import HVAC_TOKEN, HVAC_URL

NUMBER_FOR_SHOWING_IP = int(os.environ["NUMBER_FOR_SHOWING_IP"])
PROTOCOL = str(os.environ["PROTOCOL"])

# DEMO date = datetime.today()
date = datetime(2023, 4, 25)

if PROTOCOL == "SMTP":
    # DEMO file_to_open = open("/var/log/exim_mainlog", "r")
    file_to_open = open("./exim_mainlog", "r")
    TODAY = date.strftime("%Y-%m-%d")
elif PROTOCOL == "SSH":
    # DEMO file_to_open = open("/var/log/secure", "r")
    file_to_open = open("./secure", "r")
    TODAY = date.strftime("%b %d")
else:
    # DEMO file_to_open = open("/var/log/access-log", "r")
    file_to_open = open("./access-log", "r")
    TODAY = date.strftime("%m/%d/%Y")

class IP:
    def __init__(self, ip="0.0.0.0", count=0, number=0):
        self.ip = ip
        self.count = count
        self.number = number

    def __str__(self):
        return str(self.number)+"    "+str(self.ip)+"  :  "+str(self.count)


class WhiteList:
    def __init__(self):
        # DEMO client = hvac.Client(
        # DEMO     url=HVAC_TOKEN,
        # DEMO     token=HVAC_URL,
        # DEMO     verify=False
        # DEMO )
        # DEMO read_response = client.secrets.kv.v2.read_secret_version(mount_point="IPWhiteList", path='List')
        # DEMO self.white_list = read_response['data']['data']['IP']
        # DEMO self.white_list = self.white_list.split(",")
        self.white_list = ["127.0.0"] # Use IP as a mask

    def white_list_check(self, ip):
        ip_to_check = ip.split(".")
        ip_to_check_3 = str(ip_to_check[0]) + "." + str(ip_to_check[1]) + "." + str(ip_to_check[2])
        ip_to_check_2 = str(ip_to_check[0]) + "." + str(ip_to_check[1])
        for white_list_element in self.white_list:
            if str(white_list_element[-2]) == "." and str(white_list_element[-1]) == "0":
                white_list_element_2 = white_list_element.split(".")
                white_list_element_2 = str(white_list_element_2[0]) + "." + str(white_list_element_2[1])
                if str(ip_to_check_2) == str(white_list_element_2):
                    return True
            else:
                white_list_element_3 = white_list_element.split(".")
                white_list_element_3 = str(white_list_element_3[0]) + "." + str(white_list_element_3[1]) + "." + str(white_list_element_3[2])
                if str(ip_to_check_3) == str(white_list_element_3):
                    return True
        return False


def already_in_ban():
    already_in_ban_list = os.popen('iptables-save').read()
    already_in_ban_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', already_in_ban_list)
    return already_in_ban_list


valids = {}

# DEMO with open('/var/log/exim_mainlog') as file:
with file_to_open as file:
    for line in file:
        if TODAY in line:
            ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
            if ip:
                if ip[0] in valids:
                    valids[ip[0]] += 1
                else:
                    valids[ip[0]] = 1

valids = dict(sorted(valids.items(), key=lambda item: item[1]))

ips = []
number = 0
white_list = WhiteList()

# DEMO in_ban_list = already_in_ban()

for ip, ip_count in valids.items():
        # DEMO if ip_count >= NUMBER_FOR_SHOWING_IP and not white_list.white_list_check(ip) and ip not in in_ban_list:
        if ip_count >= NUMBER_FOR_SHOWING_IP and not white_list.white_list_check(ip):
            ips.append(IP(ip=ip, count=ip_count, number=number))
            number += 1

for ip in ips:
    print(ip)

while True:

    print("Enter: ")
    print("number - to block IP")
    print("blockall - to block all IPs in list")
    print("any other char - to quit")
    input_data = input("Enter:")

    if input_data.isdigit():
        input_data = int(input_data)
        if input_data >= len(ips):
            print("Wrong input")
        else:
            # DEMO os.system("iptables -I INPUT -s "+str(ips[input_data].ip)+" -j DROP")
            print(str(ips[input_data].ip)+" is blocked.")
    elif input_data == "blockall":
        for ip in ips:
            # DEMO os.system("iptables -I INPUT -s "+str(ip.ip)+" -j DROP")
            print(str(ip.ip)+" is blocked.")
        print("DONE")
    else:
        break

