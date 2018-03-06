
import urllib.request
from bs4 import BeautifulSoup
import requests
from itertools import count
import os
import datetime


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
current_year = datetime.datetime.now().year
print("서울 과거 날씨 csv 로 출력!!")
while True:
    try:  # 잘못된
        year_input = input("Year(연도)를 입력해주세요 1960 ~ 현재(%d) 공백일시에는 %d 년이 출력됩니다." % (
            current_year, (current_year-1)))
        if year_input == "":
            year_input = current_year-1
        if current_year >= int(year_input) > 1960:
            break
    except ValueError:
        print("숫자를 입력해주세요", end=", ")
    print("잘못된 값을 입력하였습니다.")
file_name = input(
    "경로와 파일명을 입력해주세요 경로가 없으면 현재 파이썬 파일 폴더에 저장 됩니다. 확장자는 .csv는 붙혀주시기 바랍니다. 공백일시에는 output.csv로 저장됩니다. 예시 : C:/Users/mgh33/outtest.csv : ")
if file_name == "":
    file_name = "output.csv"
print("프로그램 실행중입니다.")
outline = "날짜, 평균기온, 최고기온, 최저기온, 평균운량, 일강수량\n"
for i in range(0, 12):
    os.system('cls')
    print(str(i+1)+"월을 실행중입니다.")
    outline += output(year_input, i)
# print("Test")
# print(outline)
f = open(file_name, 'w')
f.write(str(outline))
f.close()
print("완료 되었습니다.")
