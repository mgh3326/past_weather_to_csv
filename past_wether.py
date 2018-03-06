
import urllib.request
from bs4 import BeautifulSoup
import requests
from itertools import count
import os


def get_html(url):  # 날씨 코드를 받아오기
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html


def getPastWeather(result, year, month):  # 결과값을 년도, 달별로 받기
    my_url = "http://www.weather.go.kr/weather/climate/past_cal.jsp?stn=108&yy=%s&mm=%s&obs=1&x=28&y=11" % (
        str(year), str(month + 1))  # 년도와 달을 매개변수를 이용하여 주소값을 입력
    html = get_html(my_url)  # html로 문자열 반환 자료값을 받기
    soup_data = BeautifulSoup(html, 'html.parser')  # beautiful함수로 실행
    store_table = soup_data.find('table', attrs={'class': 'table_develop'})
    tbody = store_table.find('tbody')  # tbody에 있는 정보만 가져오기
    b_end = True
    for store_tr in tbody.findAll('td'):
        b_end = False

        tr_tag = list(store_tr.strings)  #
        for index in tr_tag:  # 순차적으로 불러온 값을 출력한다
            if str(index).startswith('평균기온'):
                result.append(index)
            if str(index).startswith('최고기온'):
                result.append(index)
            if str(index).startswith('최저기온'):
                result.append(index)
            if str(index).startswith('평균운량'):
                result.append(index)
            if str(index).startswith('일강수량'):
                result.append(index)
    if b_end:  # 결과값을 옆으로 정리해서 출력
        return

    return


def output(year, month):  # 연도와 달을 입력 받아서
    result = []  # 리스트 생성
    outline = ""
    getPastWeather(result, year, month)  # 연도와 달을 입력해서 result 리스트에 담음
    index = 0
    oh_index = 0
    for i in result:
        if index % 5 == 0:
            # print("%d-%d-%d" %
            #       (year, (month + 1), (oh_index + 1)), end=", ")
            # outline.append("%d-%d-%d" %
            #                (year, (month + 1), (oh_index + 1)))
            outline += (str(year)+"-"+str(month+1)+"-"+str(oh_index+1)+", ")

            oh_index += 1
        index += 1
        if index % 5 != 0:
            # 평균기온 : 여기서 : 를 기준으로 오른쪽으로 사용해서 split(":")을 사용 구분자를 ,로 주기 위함
            # print(i.split(':')[1], end=", ")
            outline += (i.split(':')[1]+",")
            # outline += (",")
        if index % 5 == 0:  # 마지막은 default 인 \n 을 end로 사용하기 위함
            # print(i.split(':')[1])
            outline += (i.split(':')[1]+"\n")
            # outline += ("\n")
    return outline


# 평균기온
# 최고기온
# 평균운량
# 일강수량
# print("날짜, 평균기온, 최고기온, 최저기온, 평균운량, 일강수량")
# input("")
print("프로그램 실행중입니다.")
outline = "날짜, 평균기온, 최고기온, 최저기온, 평균운량, 일강수량\n"
for i in range(0, 12):
    os.system('cls')
    print(str(i+1)+"월을 실행중입니다.")
    outline += output(2016, i)
# print("Test")
# print(outline)
f = open('output.csv', 'w')
f.write(str(outline))
f.close()
print("완료 되었습니다.")
