import textwrap
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

class Restaurant:
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
        self.menu_reviews = []

    def add_menu(self, menu):
        self.menu.append(menu)

    def remove_menu(self, menu):
        self.menu.remove(menu)

    def __str__(self):
        menu_str = ', '.join(self.menu)
        return f"음식점 이름: {self.name} , 장소: {self.location}, 대표 메뉴: {menu_str}"
    
    def crawl_reviews(self):
        # pyvirtualdisplay
        display = Display(visible=0, size=(1920, 1080))
        display.start()

        # selenium options
        chrome_options = Options()
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')
        chrome_options.add_argument("--disable-dev-shm-usage")

        # selenium driver
        driver = webdriver.Chrome(options=chrome_options)
        url = f"https://m.place.naver.com/restaurant/1198311937/home"
        time.sleep(5)
        driver.get(url)
        
        # 가게 위치 추출
        loc_text = self.extract_location(driver)
        print(f"가게 위치: {loc_text}")
        
        # 영업시간 추출
        schedule_txt = self.extract_schedule(driver)
        print(f"영업시간:\n{schedule_txt}")
        
        # 리뷰 추출
        reviews = self.extract_reviews(driver)
        print(f"리뷰:\n{reviews}")
        
        driver.quit()
        display.stop()

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
        # 예시로 빈 문자열 반환
        return "리뷰 정보를 찾을 수 없습니다."

restuarant = Restaurant("가장맛있는 족발", "등촌", ["스파게티"])
print(restuarant.crawl_reviews())
 
