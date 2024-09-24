from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)

url ="https://news.naver.com/section/105" #"https://map.naver.com/v5/search/버우드"
driver.get(url)

# 페이지 로드 시간 대기
time.sleep(5)
# 네이버 뉴스 첫 번째 제목 크롤링
try:
    first_news_title = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/div[1]/div[1]/ul/li[1]/div/div/div[2]/a")
    print(f"첫 번째 뉴스 제목: {first_news_title.text}")
except Exception as e:
    print(f"뉴스 제목을 찾는 중 오류 발생: {e}")
# 드라이버 종료
driver.quit()
