import requests
import pandas as pd
from urllib.parse import urljoin

SERVER, PORT = '0000', 00  # AWS
DEV_ID = 'dev_02'
BASE_URL = f'http://{SERVER}:{PORT}/api/'

def receive_data():
    url = urljoin(BASE_URL, DEV_ID)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # HTTP 오류 코드를 예외로 변환
        return response.json()  # JSON 응답을 파싱하여 반환
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"Failed to parse JSON: {e}")
    return None

if __name__ == '__main__':
    data = receive_data()
    if data:
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s').strftime('%Y-%m-%d %H:%M:%S')
        if data['weather_ref'] == "True":
            pass
        else :  # 바람 방향을 조정
            adjusted_wd = (float(data["wd"]) - float(data["north_direction"]) + 360) % 360
            # 바람 방향을 문자열로 변환
            directions = ["북", "북서", "서", "남서", "남", "남동", "동", "북동"]
            index = int(adjusted_wd / 45)
            wd_kr = directions[index] if adjusted_wd % 45 < 22.5 else directions[(index + 1) % 8]

        data["wd"] = wd_kr

        print(data)