from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import requests
import warnings
import serial
import time
import os
import requests
import xml.etree.ElementTree as ET

warnings.filterwarnings('ignore')

temp_start, temp_end = 1, 6
humidity_start, humidity_end = 6, 11
ws_start, ws_end = 11, 15
wd_start, wd_end = 15, 18
north_direction_start, north_direction_end = 18, 23
atmospheric_pressure_start, atmospheric_pressure_end = 23, 29
rainfall_start, rainfall_end = 29, 36
voltage_start, voltage_end = 36, 40

DEV_ID = 'test'
DATA_PATH = f'sensor_data/{DEV_ID}.csv'
SERVER, PORT = '00.000.000.000', 0000 # AWS
url = f'http://{SERVER}:{PORT}/api/{DEV_ID}'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
RSS_url = "https://www.weather.go.kr/w/rss/dfs/hr1-forecast.do?zone=4617043000"  # 기상청 RSS

def initialize():
    time.sleep(5)
    print("Initilizing...")
    while True:
        try:
            ip = requests.get("http://api64.ipify.org").text #아이피 접속 사이트에 들어가서 현재 아이피 받아오기
            break
        except ConnectionError:
            print("No Internet Connection")
            time.sleep(10)
    not_sensor_cnt = 0 
    while True:
        try:
            print("Connecting to sensor...")
            device = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
            message = bytes("AT+AutoSend=60".encode())
            length = device.write(message) + 7
            result = device.read(length)
            if result: 
                print("Connected") # 센서가 연결이 되었을 때
                print(ip, result)
                time.sleep(3)
                break
        except:
            print('Sensor not Reachable')
            time.sleep(1)
            not_sensor_cnt += 1
            if not_sensor_cnt >= 3:
                print("No Sensor") # 센서가 연결이 안되었을 때
                print(ip, "no result")
                time.sleep(3)
                break
    
    if not os.path.exists(DATA_PATH):
        columns = 'timestamp,ip,temp,humidity,ws,wd,north_direction,atmospheric_pressure,rainfall,voltage,weather_ref'
        with open(DATA_PATH, mode='a') as f:
            f.writelines(f"{columns}\n")
    if not_sensor_cnt >= 3:
        return "No result", ip
    for _ in range(2): # ignore 2 old data
        try:
            _ = parse(device, ip) 
        except:
            time.sleep(3)
    return device, ip

def parse(device, ip):
    ret = device.read(43).decode()
    if len(ret) and ret.startswith('$'):
        try:
            data = {
                'timestamp': int(time.time()),
                'ip': ip,
                'temp': float(ret[temp_start:temp_end]),
                'humidity': float(ret[humidity_start:humidity_end]),
                'ws': float(ret[ws_start:ws_end]),
                'wd': int(ret[wd_start:wd_end]),
                'north_direction': float(ret[north_direction_start:north_direction_end]),
                'atmospheric_pressure': float(ret[atmospheric_pressure_start:atmospheric_pressure_end]),
                'rainfall': float(ret[rainfall_start:rainfall_end]),
                'voltage': float(ret[voltage_start:voltage_end]),
                'weather_ref' : "False"
            }
        except IndexError:
            data = parse(device, ip)
    else:
        data = parse(device, ip)
    return data

def write(data): # 라즈베리파이내에서 기록
    line = ''
    for value in data.values():
        line += str(value) + ','
    with open(DATA_PATH, mode='a') as f:
        f.writelines(f"{line[:-1]}\n") # removing the last char ','
    return

def remove_old(): # 라즈베리파이 내에서 오래된 데이터를 지움
    with open(DATA_PATH, mode='r+') as f:
        lines = f.readlines()
        if len(lines) > 1440 * 90:
            del lines[1:1+1440] # removing 1 day
            f.seek(1)
            f.truncate()
            for line in lines:
                f.writelines(line)
    return

if __name__ == '__main__':
    # initilizing
    device, ip = initialize() 
    if device == "No result":
        # GET 요청 보내기
        response = requests.get(RSS_url)

        # 응답 상태 코드 확인
        if response.status_code == 200:
            try:
                # XML 파싱
                root = ET.fromstring(response.content)
               # 각 item 요소를 순회하며 데이터 추출
                for item in root.findall('channel/item'):
                    description = item.find('description').find('body').find('data')
                    temp = description.find('temp').text # 현재 시간 온도
                    pcp = description.find('pcp').text # 1시간 예상강수량
                    ws = description.find('ws').text # 풍속(m/s)
                    wdKor = description.find('wdKor').text # 풍향한국어 [동, 북, 북동, 북서, 남, 남동, 남서, 서]
                    reh = description.find('reh').text #습도%
                data = {
                'timestamp': int(time.time()),
                'ip': ip,
                'temp': float(ret[temp_start:temp_end]),
                'humidity': float(ret[humidity_start:humidity_end]),
                'ws': float(ret[ws_start:ws_end]),
                'wd': int(ret[wd_start:wd_end]),
                'north_direction': float(ret[north_direction_start:north_direction_end]),
                'atmospheric_pressure': float(ret[atmospheric_pressure_start:atmospheric_pressure_end]),
                'rainfall': float(ret[rainfall_start:rainfall_end]),
                'voltage': float(ret[voltage_start:voltage_end]),
                'weather_ref' : "False"
                }
            except ET.ParseError:
                print("응답을 XML 형식으로 파싱할 수 없습니다.")
        else:
            print("API 요청 실패. 상태 코드:", response.status_code)
            print("응답 내용:", response.text)
    else:
        # start parsing
        while True:
            try:
                data = parse(device, ip)
            except:
                time.sleep(3)
                continue
            remove_old()
            write(data)
            print(data)
            try:
                requests.post(url, headers=headers, json=data, timeout=5)
            except:
                print("Destination not Reachable")
                time.sleep(10)
