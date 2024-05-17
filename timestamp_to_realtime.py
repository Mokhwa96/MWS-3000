import pandas as pd

# CSV 파일 불러오기
file_path = 'dev_02.csv'
data = pd.read_csv(file_path)

# 'timestamp' 컬럼을 사용하여 'real_time' 컬럼을 생성
data['real_time'] = pd.to_datetime(data['timestamp'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')

# 결과 확인
data.head()