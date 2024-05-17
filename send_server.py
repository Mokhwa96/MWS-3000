import requests
from urllib.parse import urljoin

SERVER, PORT = '00.000.000.000', 0000  # AWS
DEV_ID = 'test'
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
        print(data)