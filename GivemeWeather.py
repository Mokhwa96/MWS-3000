import requests
import xml.etree.ElementTree as ET

# API 엔드포인트 RSS_url
RSS_url = "https://www.weather.go.kr/w/rss/dfs/hr1-forecast.do?zone=4617043000"  # 기상청 RSS

# GET 요청 보내기
response = requests.get(RSS_url)

# 응답 상태 코드 확인
if response.status_code == 200:
    try:
        # XML 파싱
        root = ET.fromstring(response.content)

        # XML 데이터에서 필요한 정보 추출
        title = root.find('channel/title').text
        pub_date = root.find('channel/pubDate').text

        print("제목:", title)
        print("발행일:", pub_date)

        # 각 item 요소를 순회하며 데이터 추출
        for item in root.findall('channel/item'):
            author = item.find('author').text
            category = item.find('category').text
            weather_title = item.find('title').text
            description = item.find('description').find('body').find('data')

            hour = description.find('hour').text # 1일 8회 [02, 05, 08, 11, 14, 17, 20, 23시]
            day = description.find('day').text # 0 : 오늘
            temp = description.find('temp').text # 현재 시간 온도
            tmx = description.find('tmx').text # 최고 온도 -999.0: 값이 없을경우
            tmn = description.find('tmn').text # 최저 온도 -999.0: 값이 없을경우
            sky = description.find('sky').text # 하늘 상태 코드 [1: 맑음, 3: 구름많음, 4: 흐림]
            pty = description.find('pty').text # 강수 상태 코드 [0: 없음, 1: 비, 2: 비, 3: 눈, 4: 소나기, 5 : 빗방울, 6 : 빗방울/눈날림, 7 : 눈날림]
            wf_kor = description.find('wfKor').text # 날씨한국어 [맑음, 구름 많음, 흐림, 비, 비/눈, 눈, 소나기, 빗방울, 빗방울/눈날림, 눈날림]
            wfEn = description.find('wfEn').text # 날씨영어 [Clear, Mostly Cloudy, Cloudy, Rain, Rain/Snow, Snow, Shower, Raindrop, Raindrop/Snow Drifting, Snow Drifting]
            pcp = description.find('pcp').text # 1시간 예상강수량
            sno = description.find('sno').text # 1시간 예상적설량
            pop = description.find('pop').text # 강수확률%
            ws = description.find('ws').text # 풍속(m/s)
            wd = description.find('wd').text # 풍향 0~7 [북, 북동, 동, 남동, 남, 남서, 서, 북서]
            wdKor = description.find('wdKor').text # 풍향한국어 [동(E), 북(N), 북동(NE), 북서(NW), 남(S), 남동(SE), 남서(SW), 서(W)]
            wdEn = description.find('wdEn').text # 풍향영어 [E(동), N(북), NE(북동), NW(북서), S(남), SE(남동), SW(남서), W(서)]
            reh = description.find('reh').text #습도%

            print("\n작성자:", author)
            print("카테고리:", category)
            print("날씨 제목:", weather_title)
            print("시간:", hour)
            if day == "0":
                print("측적한 날: 오늘")
            print("최고 기온 (tmx):", tmx)
            print("최저 기온 (tmn):", tmn)
            print("하늘 상태 (sky):", sky)
            print("강수 형태 (pty):", pty)
            print("현재 기온 (temp):", temp)
            print("날씨 예보 (한국어) (wfKor):", wf_kor)
            print("날씨 예보 (영어) (wfEn):", wfEn)
            print("1시간 예상강수량 (pcp):", pcp)
            print("1시간 예상적설량 (sno):", sno)
            print("강수 확률 (pop):", pop,"%")
            print("풍속 (ws):", ws)
            print("풍향 (wd):", wd)
            print("풍향 (한국어) (wdKor):", wdKor)
            print("풍향 (영어) (wdEn):", wdEn)
            print("습도 (reh):", reh,"%")

    except ET.ParseError:
        print("응답을 XML 형식으로 파싱할 수 없습니다.")
else:
    print("API 요청 실패. 상태 코드:", response.status_code)
    print("응답 내용:", response.text)

#예시
#{'timestamp': '2024-04-25 07:56:37', 'ip': '192.168.1.1', 'temp': '25.0', 'humidity': '50.0', 'ws': '5.0', 'wd': '180', 'north_direction': '0.0', 'atmospheric_pressure': '1013.25', 'rainfall': '0.0', 'voltage': '12.0', 'wd_kr': '남'}
# temp : temp, 
# humidity :reh 
# ws : ws 
# wd : wdKor 
# north_direction : 0.0
# atmospheric_pressure : "--"
# rainfall : pcp
# voltage : ws*2