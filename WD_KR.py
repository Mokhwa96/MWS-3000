wd = 45  # 바람이 불어오는 방향의 각도
nd = 227  # 북쪽 방향의 각도

# 바람 방향을 조정
adjusted_wd = (wd - nd + 360) % 360

# 바람 방향을 문자열로 변환
directions = ["북", "북서", "서", "남서", "남", "남동", "동", "북동"]
index = int(adjusted_wd / 45)
wd_kr = directions[index] if adjusted_wd % 45 < 22.5 else directions[(index + 1) % 8]

print(wd_kr)