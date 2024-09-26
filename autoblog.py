import textwrap
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import google.generativeai as genai
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

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
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        options.add_argument(
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        url = f"https://map.naver.com/v5/search/{self.location} {self.name}"
        driver.get(url)
        driver.switch_to.parent_frame()
        iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
        driver.switch_to.frame(iframe)
        time.sleep(3)
        review = driver.find_element_by_css_selector('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz') 
        # xpath는 가게마다 다르게 설정되어 있었기 때문에 css selector를 이용해서 review text가 있는 tag에 접근
        review_text = review.find_elements_by_tag_name('span')

        
        print(review_text)
        
        

        
restuarant = Restaurant("버우드", "홍대", ["스파게티"])
print(restuarant.crawl_reviews())
 

