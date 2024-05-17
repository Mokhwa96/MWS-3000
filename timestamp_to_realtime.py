import pandas as pd

# CSV 파일 불러오기
file_path = 'test.csv'
data = pd.read_csv(file_path)

# 'timestamp' 컬럼을 사용하여 'real_time' 컬럼을 생성
# data['real_time'] = pd.to_datetime(data['timestamp'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S') # 새로 붙이기
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S') # 대체 하기
# 결과 확인
print(data.head())