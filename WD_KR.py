wd = 45  # 바람이 불어오는 방향의 각도
nd = 227  # 북쪽 방향의 각도
wd_kr = ""

if wd < nd:
    wd += 360  # wd가 nd보다 작을 경우, 360을 더하여 조정

# 수정된 범위 조건
if wd-nd >= 0 and wd-nd < 22.5:
    wd_kr = "북"
elif wd-nd < 67.5:
    wd_kr = "북서"
elif wd-nd < 112.5:
    wd_kr = "서"
elif wd-nd < 157.5:
    wd_kr = "남서"
elif wd-nd < 202.5:
    wd_kr = "남"
elif wd-nd < 247.5:
    wd_kr = "남동"
elif wd-nd < 292.5:
    wd_kr = "동"
elif wd-nd < 337.5:
    wd_kr = "북동"
else:
    wd_kr = "북"  # 마지막 범위를 넘어선 경우 (360도에 가까운 경우)

print(wd_kr)