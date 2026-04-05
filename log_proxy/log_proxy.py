import os
import uiautomator2 as u2
import time
from multiprocessing import Process
from log_unity.unity_login import get_bold_phone_rows

XPATH = {
    'app': "com.vat.proxyconnector",
    'protocol_type': '//*[@resource-id="com.vat.proxyconnector:id/spinnerItemText"]',
    'ip_address': '//*[@resource-id="com.vat.proxyconnector:id/edtAddressContainer"]',
    'port': '//*[@resource-id="com.vat.proxyconnector:id/edtPortContainer"]',
    'username': '//*[@resource-id="com.vat.proxyconnector:id/edtUsernameContainer"]',
    'password': '//*[@resource-id="com.vat.proxyconnector:id/edtPasswordContainer"]',
    'connect': '//*[@text="CONNECT"]',
}

data_list = get_bold_phone_rows("1KLUV3_u3XS0VtdrwcvzgpRBfoud-drdKDfyYB1Y2xjM", "Sheet1")

def parse_data(data):
    ip, port, username, password = data.split(":")
    return ip, port, username, password


def main(data):
    proxy = data['proxy']
    device_id = data['Phone_ID']
    ip, port, username, password = parse_data(proxy)
    d = u2.connect(device_id)
    d.app_start(XPATH['app'])
    os.system(f"adb -s {device_id} shell settings put system accelerometer_rotation 0")
    time.sleep(6)
    d.xpath(XPATH['protocol_type']).click()
    os.system(f"adb -s {device_id} shell settings put system accelerometer_rotation 0")
    time.sleep(2)
    d.xpath('//*[@text="socks5"]').click()
    os.system(f"adb -s {device_id} shell settings put system accelerometer_rotation 0")
    time.sleep(2)
    d.xpath(XPATH['ip_address']).click()
    os.system(f"adb -s {device_id} shell settings put system accelerometer_rotation 0")
    time.sleep(2)
    d.send_keys(ip)
    time.sleep(2)
    d.xpath(XPATH['port']).click()
    os.system(f"adb -s {device_id} shell settings put system accelerometer_rotation 0")
    time.sleep(2)
    d.send_keys(port)
    time.sleep(2)
    d.xpath(XPATH['username']).click()
    os.system(f"adb -s {device_id} shell settings put system accelerometer_rotation 0")
    time.sleep(2)
    d.send_keys(username)
    time.sleep(2)
    d.xpath(XPATH['password']).click()
    os.system(f"adb -s {device_id} shell settings put system accelerometer_rotation 0")
    time.sleep(2)
    d.send_keys(password)
    time.sleep(2)
    d.xpath(XPATH['connect']).click()
    os.system(f"adb -s {device_id} shell settings put system accelerometer_rotation 0")
    time.sleep(5)
    if d.xpath('//*[@text="OK"]').exists:
        d.xpath('//*[@text="OK"]').click()
    time.sleep(2)
    if d.xpath('//*[@text="Allow"]').exists:
        d.xpath('//*[@text="Allow"]').click()


if __name__ == "__main__":
    processes = []
    for data in data_list:
        p = Process(target=main, args=(data,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

