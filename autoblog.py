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
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 로그 설정
logging.basicConfig(
    filename="/home/wjsqorwns93/bj/autoblogging/logs/restaurant_info.log",         # 로그 파일 이름
    level=logging.INFO,                      # 로그 레벨 (INFO 이상의 레벨만 기록)
    format="%(asctime)s - %(levelname)s - %(message)s"  # 로그 출력 형식
)

GOOGLE_API_KEY = 'AIzaSyCW9fwk8jBkVQ45fiKvVHFLj1971yI1X-o'

class Restaurant_Info:
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



    def __str__(self):
        return f"음식점 이름: {self.name} , 장소: {self.location}"
    
    def crawling_restaurant(self):
        
        logging.info(f"{self.name} 크롤링 시작")
        
        
        try : 
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
            input_loc_txt = f"가게 위치: {loc_text}"
            logging.info("가게 위치 크롤링 완료")
            
            # 영업시간 추출
            schedule_txt = self.extract_schedule(driver)
            input_sch_txt = f"영업시간:\n{schedule_txt}"
            logging.info("영업시간 크롤링 완료")
            
            # 리뷰 추출
            time.sleep(3)
            n= 10 # 몇 번이나 더보기 버튼을 누를 것인가
            reviews = self.extract_reviews(driver,n)
            input_reviews_txt = f"리뷰 :{", \n".join(reviews)}"
            logging.info("리뷰 크롤링 완료")
        
        except Exception as e :
            logging.error(f"{self.name} 크롤링 중 오류 발생 :{e}")
        
        finally : 
            driver.quit()
            display.stop()
            logging.info(f"{self.name} 크롤링 종료")
            
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


    def extract_reviews(self, driver,n):
        # 리뷰 추출 로직을 여기에 추가
    
        review_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="tpj9w _tab-menu"]/span[text()="리뷰"]'))
        )
        review_tab.click()
        logging.info("Review Tab 화면 정상 호출")
        
        for i in range(n):
            try : 
                
                more_reviews_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.fvwqf'))
                )
                if more_reviews_btn.is_displayed():
                
                    driver.execute_script("arguments[0].scrollIntoView(true);", more_reviews_btn)
                    time.sleep(5)
                    more_reviews_btn.click()
                    time.sleep(3) 
                    
                    logging.info(f"{i} 번째 더보기 클릭 완료")
                else:
                    logging.info('더보기 버튼이 더이상 존재하지 않습니다.')
                    break
            except  (TimeoutException, NoSuchElementException):
                logging.info(f'더보기 버튼을 찾을 수 없거나 로딩이 완료되었습니다.')
                break
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        elements = soup.find_all(class_ = 'pui__xtsQN-')
        text_list = [element.get_text().strip() for element in elements]
            
        return text_list
    


#실행 코드
# restaurant=Restaurant_Info("텐노아지","등촌역")
# restaurant_info =restaurant.crawling_restaurant()

# print(restaurant_info)



## json 파일 떨구는 코드
import json


# with open("/home/wjsqorwns93/bj/autoblogging/restaurant_data.json", "w", encoding="utf-8") as json_file:
#     json.dump(restaurant_info, json_file, ensure_ascii=False, indent=4)
#     print('저장 성공')

file_path = '/home/wjsqorwns93/bj/autoblogging/restaurant_data.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)


import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY = 'AIzaSyCW9fwk8jBkVQ45fiKvVHFLj1971yI1X-o'
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel('gemini-1.5-flash',
                              generation_config=generation_config)

data['menu'] =['아지텐동','에비텐카레']
data['visit_date'] = '2024-08-30'

                
# response = model.generate_content(f"""{data} 이와같은 음식점 정보를 
#                                  바탕으로 블로그 포스팅을 할껀데 제목을 아래의 예제와 같이 지을꺼야
#                                  예제) [연남] 마포 브런치 맛집 '버우드' / 서이추환영 ,[안국역/북촌] 힐링되는 찻집 카페 '티테라피' / 서이추환영
#                                 - 첫번째로 들어가는 것은 []안에 지역을 넣어줘 역을 기준으로 넣어주는게 제일 좋고 아니라면 그 음식점이 있는 유명한 지명을 넣어줘도 돼
#                                 - 두번째 이 음식점의 대표메뉴나 대표표현을 이용해서 이 음식점의 특징을 넣어줘 예를 들어 힐링되는 찻집 카페 처럼 말이야
#                                 - 그리고 세번째는 ''안에 음식점 이름을 넣어줘
#                                 - 마지막으로는 / 서이추환영을 꼭 넣어주길 바라
#                                 - 다른 옵션이나 부가 설명은 답변안에 넣지말고 제목만 추출해서 쓸 수 있게 짧게 답변 줬으면 좋겠어
#                                 """)                   
# print(response.text)



# response = model.generate_content(f"""{data} 이와 같은 음식점 정보를 바탕으로 블로그 포스팅을 할꺼야 아래는 내가 예전에 쓴 글이니
#                                 이와 같이 써줘.
                                
#                                 내가 쓴 블로그 글: 
#                                 안녕하세요 👋🏻👋🏻
#                                 추석 연휴 잘 보내셨나요~~?
#                                 벌써 연휴가 다 끝나가네요ㅜ

#                                 오늘은 행복했던 추석연휴 시작 전 날! 
#                                 퇴근하고 여자친구와 같이 저녁 먹은 카이센동 맛집 여의도 '오복수산'을 소개드려요~
#                                 (여기서 카이센동이란 해산물이 들어간 돈부리 즉 덮밥이라고 합니다~)

#                                 여의도 IFC몰 근처에 있었구요~ 
#                                 오후 5시까지 브레이크 타임이었는데 우연히 딱 5시에 도착해서 저희가 1등으로 들어갔답니다~ 
#                                 (저희가 들어오고 사람들이 줄줄이 오더라구요)
#                                 아주 고급스러운 분위기의 일식당이었구요~ 연인과 아니면 친구와 분위기있게 먹기 좋은 곳이었어요!
#                                 [사진]

#                                 메뉴를 보니 카이센동뿐만 아니라 사시미, 스시 등 다양한 해산물 요리를 판매하고 있어요 ~ 
#                                 주류도 사케, 하이볼, 맥주, 소주 등 친구들과 술한잔 하러 오는 것도 좋을 것 같아요!
#                                 [사진]

#                                 저희는 밥이 메인이었기 때문에 카이센동을 시켰어요! 우선 전체사진 한번 보여드릴게요ㅎㅎ
#                                 [사진]

#                                 하나씩 메뉴를 소개 드리자면
#                                 저는 생참다랑어 속살, 뱃살, 생연어가 들어간 혼마구로 사케 이구라동을 먹었구요,
#                                 [사진]
#                                 생연어 뿐만 아니라 참치회를 맛보고 싶다면 
#                                 제가 먹었던 이 메뉴 추천드려요!

#                                 여자친구는 생연어가 듬뿍 들어간 사케동을 먹었답니다~
#                                 [사진]
#                                 연어를 특히 좋아하신다면 사케동 추천드릴게요! 
#                                 두터운 생연어를 한점 한점 먹을 때 마다 너무 행복했답니다~~​

#                                 이렇게 맛있는 음식과 함께 술이 빠질 수 있나요!!!!
#                                 여자친구가 맛있는 하이볼 하나 시켜줬어요~
#                                 [사진]
#                                 이름하여 가을 단풍 하이볼 !!!
#                                 가을처럼 약간 씁쓸~하고 동시에 달콤한 하이볼이었어요ㅎㅎ
#                                 다음에 다시 찾아온다면 꼭 사시미와 함께 사케나 소주를... 아니 콜라를...
#                                 (술은 몸에 해로와요!)
#                                 먹고 싶네요~!

#                                 여러분들도 여의도에서 저녁을 드시게 된다면 정말 한번 꼭 드셔보셔요!
#                                 이번 포스팅은 여기서 마치겠습니다!
#                                 먹바!

#                                 - 내 블로그 닉네임이 "먹찐 커플"이야 그러니깐 첫 문장은 "먹찐 커플"임을 밝히고 시작했으면 좋겠어
#                                 - 여자친구와 함께 간 음식점에 대한 블로그글이어서 이 점 꼭 참고해서 작성해줘
#                                 - 내가 쓴글의 말투와 문장의 수와 비슷하게 참고해서 작성해줬으면 좋겠어
#                                 - 니가 거리에 대한 정보는 알아서 몇 분정도 걸어가면 있다던지로 대체해줘
#                                 - 중간중간 글 아래 해당하는 글에 대한 '[사진]' 한개를 넣어줘
#                                 - 내가 준 정보의 menu가 내가 시킨 음식이니깐 이것에 대해서만 글을 써야해
#                                 - 글의 첫 부분에는 어떻게 가게 됐는지 설명이 들어가야해 젊은 커플이 왜 그 음식점을 갔는지 잘 지어내서 써줘
#                                 - 그리고 음식점의 분위기, 음식의 후기는 지어내지 말고 내가 입력한 리뷰 정보를 기반으로 사실적으로 작성할 수 있도록 해
#                                 - 가격은 시간에 따라서 변할 수 있으니 언급해주지 않았으면 좋겠어
#                                 - 글의 순서는 소개 -> 음식점 분위기 -> 메뉴 소개 -> 나와 여자친구가 시킨 음식 리뷰 -> 추천글 ->끝맺음 순으로 써줬으면 좋겠어
#                                 - 사진은 가게내부사진, 메뉴판사진, 시킨 메뉴의 전체사진, 각 메뉴의 사진만으로 구성해줘
#                                 - 가게에서 다루는 메뉴에 대해서 소개할 때 내가 준 리뷰 정보에 나와있는 음식이거나 내가 시킨 음식들 정도만 언급하고 다양한 음식들이 있다 이정도 수준만 언급해봐
#                                 - 각 메뉴리뷰는 한개씩 사진과 함께 글을 작성해줘 또한 메뉴에 대해서 설명할 때 리뷰정보에 있는 재료들만 사실적으로 언급해줘
#                                 - 리뷰에서 봤다 이런 표현은 자제해줘
#                                 - 글의 마지막에는 이번 포스팅은 여기서 마치겠습니다!!! 먹바! 가 들어가야돼
#                                 """)
# print(response.text)


response = model.generate_content(f"""{data['schedule']}은 음식점의 영업시간 정보야 이를 블로그에 정보로 넣을 건데 다음과 같이 적어줘
                                - 영업시간 이라는 단어로 시작해줘 이부분에만 '*'는 빼줘
                                - 영업시간이 같은 요일끼리 묶어줘 예) 월요일 - 금요일, 토요일 - 일요일
                                - 요일 뒤, 라스트 오더, 브레이크 타임뒤에는 한줄 띄고 시간을 적어줘
                                - 영업시간을 두개로 쪼개지말고 브레이크 타임 고려하지 말고 꼭 한줄에 적어줘
                                - 브레이크 타임이나 라스트 오더 시간이 있다면 적어줘
                                - 정기 휴무가 있다면 제일 마지막에 적어줘 없으면 적지마
                                - 마지막으로 네이버에 등록된 업체 등록 영업 시간입니다* 를 이대로 똑같이 맨 아래에 꼭 넣어줘, 영업 시간입니다 뒤에 * 잊지말고 넣어주고
                                """)
print(response.text)






