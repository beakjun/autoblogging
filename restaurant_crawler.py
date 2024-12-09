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
from logger_config import get_logger
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

GOOGLE_API_KEY = 'AIzaSyCW9fwk8jBkVQ45fiKvVHFLj1971yI1X-o'

class RestaurantInfo:
    """
    음식점 클래스 초기화 메서드

    Args:
        name (str): 음식점 이름
        location (str): 음식점 위치
        menu (list): 음식점 메뉴 리스트
    """
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.restaurant_reviews = []
        self.menu_reviews = {}
        self.logger = get_logger(self.__class__.__name__)



    def __str__(self):
        return f"음식점 이름: {self.name} , 장소: {self.location}"
    
    def crawling_restaurant(self):
        
        self.logger.info(f"{self.name} 크롤링 시작")
        input_sch_txt=""
        input_loc_txt=""
        input_reviews_txt = ""
        
     
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
        review_url = f"https://m.place.naver.com/restaurant/{store_id}/review/visitor"
        time.sleep(2)
        
        driver.get(url)
        
        # 가게 위치 추출
        loc_text = self.extract_location(driver)
        input_loc_txt = f"가게 위치: {loc_text}"
        self.logger.info("가게 위치 크롤링 완료")
        
        # 영업시간 추출
        schedule_txt = self.extract_schedule(driver)
        input_sch_txt = f"영업시간:\n{schedule_txt}"
        self.logger.info("영업시간 크롤링 완료")
        
        try:
        # 리뷰 추출
            time.sleep(3)
            n= 5 # 몇 번이나 더보기 버튼을 누를 것인가
            driver.get(review_url)
            reviews = self.extract_reviews(driver,n)
            reviews_inte=", \n".join(reviews)
            input_reviews_txt = f"리뷰 :{reviews_inte}"
        
            self.logger.info("리뷰 크롤링 완료")
        
        except Exception as e :
            put_reviews_txt = f"리뷰 :{", \n".join(reviews)}"
            self.logger.error(f"{self.name} 크롤링 중 오류 발생 :{e}")
        
        finally : 
            driver.quit()
            display.stop()
            self.logger.info(f"{self.name} 크롤링 종료")
            
            restaurant_info = {
                'name' : self.name,
                'loc' : input_loc_txt,
                'reviews' : input_reviews_txt,
                'schedule' : input_sch_txt
            }
            
            return restaurant_info
         
        
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
        else:
            store_id=None
            self.logger.info("requirejs가 포함된 <script> 태그를 찾을 수 없습니다.")
        
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


    def extract_reviews(self, driver,n):
        
        
        # 리뷰 추출 로직을 여기에 추가
        # review_tab = WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, '//a[@class="tpj9w _tab-menu"]/span[text()="리뷰"]'))
        # )
        # review_tab.click()
        
        # # 페이지가 로드될 때까지 대기
        self.logger.info(driver.current_url)
        self.logger.info("Review Tab 화면 정상 호출")
        
        try :
            for i in range(n):
                more_reviews_btn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.fvwqf'))
                )
                if more_reviews_btn.is_displayed():
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')
                    elements = soup.find_all(class_ = 'pui__xtsQN-')
            
                    actions = ActionChains(driver)
                    time.sleep(3)
                    actions.move_to_element(more_reviews_btn).perform()
            
                    time.sleep(3)
                    more_reviews_btn.click()
                    self.logger.info(f"{i+1} 번째 더보기 클릭 완료")
                else : 
                    self.logger.info(f"{i+1} 번째에서 더보기 버튼 찾을 수 없음")
        finally :
            time.sleep(3)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            elements = soup.find_all(class_ = 'pui__xtsQN-')
            text_list = [element.get_text().strip() for element in elements]
        
            
        return text_list
    

def main():
    restaurant=RestaurantInfo("텐노아지","등촌역")
    restaurant_info =restaurant.crawling_restaurant()
    print(restaurant_info)

if __name__ == "__main__":
    main()
    



