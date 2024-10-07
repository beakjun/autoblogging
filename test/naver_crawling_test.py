import requests
from bs4 import BeautifulSoup
import json
import time
import urllib.parse


agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'

url = 'https://m.map.naver.com/search2/search.naver?query=홍대 버우드&sm=hty&style=v5'


headers = {
    'User-Agent': agent
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

# <script> 태그 내의 JSON 문자열 찾기
script_tag = soup.find('script', string=lambda t: t is not None and 'requirejs' in t)
if script_tag:
    # script 내의 코드로부터 searchResult 데이터 찾아서 추출
    code = script_tag.string.split('requirejs([')[-1]  # 'requirejs([' 이후 내용 가져오기
    if 'search' in code:
        # 예시로 가정된 searchResult 객체를 찾는 부분
        search_result_start = code.find('searchResult = {')
        search_result_end = code.find('};', search_result_start) + 1
        search_result_json = code[search_result_start:search_result_end]
        
                # JSON 문자열을 Python 객체로 변환
        search_result = json.loads(search_result_json.replace('searchResult = ', ''))
        
        # 버우드의 고유 ID 추출
        store_id = search_result['site']['list'][0]['id']
        print("버우드의 고유 ID:", store_id)
else:
    print("requirejs가 포함된 <script> 태그를 찾을 수 없습니다.")
    
    
time.sleep(1)

place_name = "홍대 버우드"
encoded_place_name = urllib.parse.quote(place_name)
print(encoded_place_name)
new_url = f'https://m.place.naver.com/restaurant/{store_id}/home'

headers = {
    'referer': f'https://m.map.naver.com/search2/search.naver?query={encoded_place_name}&sm=hty&style=v5',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Connection' : 'keep-alive',
    'Upgrade-Insecure-Requests' : '1',
    'Sec-Fetch-Dest' : 'document',
    'Sec-Fetch-Mode' : 'navigate',
    'Sec-Fetch-Site' : 'cross-site',
    'Sec-Fetch-User' : '?1', 
}

response = requests.get(new_url,headers=headers)

if response.encoding.lower() != 'utf-8':
    response.encoding = 'utf-8'  # 또는 'euc-kr' 등 적절한 인코딩으로 설정


soup = BeautifulSoup(response.text, 'html.parser')
target_div = soup.find('div', class_='nZapA')

# <span> 태그 제거 (내용을 유지하지 않고 제거)
for span in target_div.find_all('span'):
    span.decompose()

# 텍스트 추출
cleaned_text = target_div.get_text(strip=True)
print(cleaned_text+'m')