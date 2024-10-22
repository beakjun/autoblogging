import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import google.generativeai as genai
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

GOOGLE_API_KEY = 'AIzaSyCW9fwk8jBkVQ45fiKvVHFLj1971yI1X-o'

class Restaurant_Info:
    """
    음식점 클래스 초기화 메서드

    Args:
        name (str): 음식점 이름
        location (str): 음식점 위치
        menu (list): 음식점 메뉴 리스트
    """
    def __init__(self, name, location, date):
        self.name = name
        self.location = location
        self.date = date
        self.menu = []
        self.restaurant_reviews = []
        self.menu_reviews = {}

    def add_menu(self, menu):
        self.menu.append(menu)

    def remove_menu(self, menu):
        self.menu.remove(menu)

    def __str__(self):
        menu_str = ', '.join(self.menu)
        return f"음식점 이름: {self.name} , 장소: {self.location}, 대표 메뉴: {menu_str}"
    
    def crawling_restaurant(self):
        # pyvirtualdisplay
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        # selenium options
        chrome_options = Options()
        chrome_options.add_argument(f'--user-agent={agent}')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # selenium driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # getting naver store_id
        store_id=self.extract_store_id()
        
        
        # 크롤링 시작
        url = f"https://m.place.naver.com/restaurant/{store_id}/home"
        time.sleep(2)
        
        driver.get(url)
        
        # 가게 위치 추출
        loc_text = self.extract_location(driver)
        print(f"가게 위치: {loc_text}")
        
        # 영업시간 추출
        schedule_txt = self.extract_schedule(driver)
        print(f"영업시간:\n{schedule_txt}")
        
        # 리뷰 추출
        reviews = self.extract_reviews(driver)
        print(f"리뷰:\n{reviews[0]}")
        
        driver.quit()
        display.stop()
        
        
    def extract_store_id(self):
        url = f'https://m.map.naver.com/search2/search.naver?query={self.location} {self.name}&sm=hty&style=v5'
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        headers = { 'User-Agent': agent }

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        
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
                print(f"{self.name} 네이버 고유 ID:", store_id)
        else:
            store_id=None
            print("requirejs가 포함된 <script> 태그를 찾을 수 없습니다.")
        
        return store_id
    
    

    def extract_location(self, driver):
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        target_div = soup.find('div', class_='nZapA')
        
        if target_div:
            for span in target_div.find_all('span'):
                span.decompose()
            extracted_text = target_div.get_text(strip=True)
            return extracted_text + 'm'
        return "위치 정보를 찾을 수 없습니다."

    def extract_schedule(self, driver):
        driver.find_element(By.CSS_SELECTOR, 'a.gKP9i').click()
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements = soup.find_all(class_='w9QyJ')
        schedule_txt = ""
        for element in elements[1:]:
            text = element.get_text(strip=True)[:-2]
            if element.get_text(strip=True) in ('접기'):
                text = element.get_text(strip=True)[:-2]
            schedule_txt += text + '\n'
        return schedule_txt


    def extract_reviews(self, driver):
        # 리뷰 추출 로직을 여기에 추가
    
        driver.find_element(By.XPATH, '//a[@class="tpj9w _tab-menu"]/span[text()="리뷰"]').click()
        time.sleep(2) 
        
        n=3
        for i in range(n):

            driver.find_element(By.CSS_SELECTOR, 'a.fvwqf').click()
            time.sleep(2) 
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        elements = soup.find_all(class_ = 'pui__xtsQN-')
        
        text_list = [element.get_text().strip() for element in elements]
            
        return text_list












restaurant=Restaurant_Info("텐노아지","등촌역","2024-08-02")
restaurant.add_menu('파스타')
restaurant.crawling_restaurant()