import requests
import re
from datetime import datetime
from datetime import timedelta



def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code


def timeconvert(timestr):
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")


now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
file_time = now.strftime("%Y%m%d")
token = "URcWh4jqXmWSxmpiPoraXBDeTXu0WWcFO0fFMkIdyHp"
allen_token = "gZs6t8RLPVzdfA2ZTZCq4qRnRtOpnWyV208fraEmyYM"
refused_list = []
pattern_time = re.compile(r'\d{4}-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Cache-Control": "no-store",
    "Connection": "close"
}
url = "https://shop.eckare.com/snm/api_order_err/etmall_" + file_time + ".txt"
req = requests.get(url, headers=headers)
with open("./etmall_" + str(file_time) + ".txt", "wb") as code:
    code.write(req.content)
with open("./etmall_" + file_time + ".txt", "r+", encoding="utf-8-sig") as f:
    data = f.readlines()
for i in data:
    if "curl" in i:
        result = pattern_time.search(i)
        compare_time_base = now + timedelta(minutes = -10)
        log_time = timeconvert(result[0])
        if log_time >= compare_time_base:
            refused_list.append(i)
refused_string = ""
if len(refused_list) > 0:
    for refused_content in refused_list:
        refused_string += refused_content
    if len(refused_string) > 250:
        msg_content = "[shop.eckare.com call api.u-mall.com.tw connection error]" + "\n" + refused_string[:250]
        lineNotify(token, msg_content)
        #lineNotify(allen_token, msg_content)
        with open("./etmall_" + str(file_time) + "scheduler.log", "a+") as fw:
            fw.write(current_time + " " + msg_content)
    else:
        msg_content = "[shop.eckare.com call api.u-mall.com.tw connection error]" + "\n"
        lineNotify(token, msg_content)
        #lineNotify(allen_token, msg_content)
        with open("./etmall_" + str(file_time) + "scheduler.log", "a+") as fw:
            fw.write(current_time + " " + msg_content)
else:
    with open("./etmall_" + str(file_time) + "scheduler.log", "a+") as fw:
        fw.write(current_time + " Check Done! \n")