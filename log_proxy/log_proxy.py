import os
import uiautomator2 as u2
import time
from multiprocessing import Process
import subprocess

XPATH = {
    'app': "com.vat.proxyconnector",
    'protocol_type': '//*[@resource-id="com.vat.proxyconnector:id/spinnerItemText"]',
    'ip_address': '//*[@resource-id="com.vat.proxyconnector:id/edtAddressContainer"]',
    'port': '//*[@resource-id="com.vat.proxyconnector:id/edtPortContainer"]',
    'username': '//*[@resource-id="com.vat.proxyconnector:id/edtUsernameContainer"]',
    'password': '//*[@resource-id="com.vat.proxyconnector:id/edtPasswordContainer"]',
    'connect': '//*[@text="CONNECT"]|//*[@resource-id="com.vat.proxyconnector:id/btConnect"]',
    'connect_vn': '//*[@text="KẾT NỐI"]',
    'connect_rs': '',
    'socks5': '//*[@text="socks5"]',
    'https': '//*[@text="https"]',
    'time-zone': '//androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.Switch[1][@checked="true"]',
    'menu': '//*[@resource-id="com.android.settings:id/sesl_action_bar_overflow_button"]',
}

Device_ID = [
]

Proxy = [
]
ADB_PATH = r""

def parse_data(data):
    ip, port, username, password = data.split(":")
    return ip, port, username, password

def rotate(device_id):
    subprocess.run([
        ADB_PATH, "-s", device_id,
        "shell", "settings", "put",
        "system", "accelerometer_rotation",
        "0"
    ])

def choose_zone(d):
    d.xpath('//*[@text="Select time zone"]').click()
    time.sleep(2)
    d.xpath(XPATH['menu']).click()
    time.sleep(2)
    d.xpath('//*[@text="Select by UTC offset"]').click()
    time.sleep(2)
    d.swipe(500, 1500, 500, 500, duration=0.2)
    time.sleep(1)
    d.swipe(500, 1500, 500, 500, duration=0.2)
    time.sleep(1)
    d.swipe(500, 1500, 500, 500, duration=0.2)
    time.sleep(2)
    d.xpath('//*[@text="GMT+08:00"]').click()
    

def main(device_id, proxy):
    ip, port, username, password = parse_data(proxy)
    d = u2.connect(device_id)
    d.press("home")
    d.app_clear("com.genfarmer.uiautomator")
    d.app_start(XPATH['app'])
    rotate(device_id)
    time.sleep(10)
    d.xpath(XPATH['protocol_type']).click()
    rotate(device_id)
    time.sleep(5)
    d.xpath(XPATH['socks5']).click()

    time.sleep(2)
    d.xpath(XPATH['ip_address']).click()

    time.sleep(2)
    d.send_keys(ip)
    time.sleep(2)
    d.xpath(XPATH['port']).click()
    rotate(device_id)
    time.sleep(2)
    d.send_keys(port)
    time.sleep(2)
    d.xpath(XPATH['username']).click()
    rotate(device_id)
    time.sleep(2)
    d.send_keys(username)
    time.sleep(2)
    d.xpath(XPATH['password']).click()
    rotate(device_id)
    time.sleep(2)
    d.send_keys(password)
    time.sleep(2)
    d.xpath(XPATH['connect']).click()
    rotate(device_id)
    time.sleep(5)
    if d.xpath('//*[@text="OK"]').exists:
        d.xpath('//*[@text="OK"]').click()
        time.sleep(2)
    if d.xpath('//*[@text="Allow"]').exists:
        d.xpath('//*[@text="Allow"]').click()
        time.sleep(2)
    d.press("home")
    time.sleep(2)
    # subprocess.run([
    #     ADB_PATH, "-s", device_id,
    #     "shell", "am", "start", "-a","android.settings.DATE_SETTINGS"
    # ])
    # rotate(device_id)
    # time.sleep(5)
    # if d.xpath(XPATH['time-zone']).exists:
    #     d.xpath(XPATH['time-zone']).click()
    #     choose_zone(d)
    # else:
    #     choose_zone(d)
    # time.sleep(2)
    # d.press("home")
        


if __name__ == "__main__":
    processes = []
    for device_id, proxy in zip(Device_ID, Proxy):
        p = Process(target=main, args=(device_id, proxy))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
