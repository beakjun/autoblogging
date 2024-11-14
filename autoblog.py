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
            
            return input_loc_txt, input_sch_txt, input_reviews_txt
         
        
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


restaurant_nm = '텐노아지'
restaurant_loc = '등촌역'
visit_date = '2024-08-02'
menu_1 = '아지텐동'
menu_2 = '에비텐카레'
# #실행 코드
# restaurant=Restaurant_Info("텐노아지","등촌역","2024-08-02")
# restaurant.add_menu('파스타')
# loc , schedule, reviews =restaurant.crawling_restaurant()
# print(reviews)



# ### json 파일 떨구는 코드
# # import json

# # data = {
# #     "location": loc,
# #     "schedule": schedule,
# #     "reviews": reviews
# # }

# # with open("restaurant_data.json", "w", encoding="utf-8") as json_file:
# #     json.dump(data, json_file, ensure_ascii=False, indent=4)
import json
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



# ## 일단 종합적인 정보 통합
# text_summary = f"""
#                 음식점 정보 요약
#                 음식점 이름 : {restaurant_nm}
#                 위치 : {restaurant_loc}
#                 메뉴 : {menu_1}
#                 방문일시 : {visit_date}
#                 리뷰 : {'/n ,'.join(data['reviews'])}                
#                 """

text_summary = f"""
                음식점 정보 요약
                음식점 이름 : {restaurant_nm}
                위치 : {restaurant_loc}
                방문일시 : {visit_date}
                리뷰 : {'/n ,'.join(data['reviews'])}                
                """

                
# # response = model.generate_content(f"""{text_summary} 정보를 
# #                                  바탕으로 블로그 포스팅을 할껀데 제목을
# #                                  예제) [연남] 마포 브런치 맛집 '버우드' / 서이추환영 ,[안국역/북촌] 힐링되는 찻집 카페 '티테라피' / 서이추환영
# #                                  과 같은 형식으로 []안에는 지역만 그다음은 음식점에 대한 대표 표현 혹은 대표메뉴에 대한 대표 표현 그리고 ''안에는 음식점이름 그리고 /서이추 환영을 꼭 넣어서 지어줘""")
# # print(response.text)



response = model.generate_content(f"""위치 : {restaurant_loc}, 음식점이름 :{restaurant_nm}, 
                                리뷰 정보 : {data['reviews']}, 나와 여자친구가 시킨 음식 : [{menu_2},{menu_1}],
                                내가 쓴 블로그 글: 
                                안녕하세요 👋🏻👋🏻
                                추석 연휴 잘 보내셨나요~~?
                                벌써 연휴가 다 끝나가네요ㅜ

                                오늘은 행복했던 추석연휴 시작 전 날! 
                                퇴근하고 여자친구와 같이 저녁 먹은 카이센동 맛집 여의도 '오복수산'을 소개드려요~
                                (여기서 카이센동이란 해산물이 들어간 돈부리 즉 덮밥이라고 합니다~)

                                여의도 IFC몰 근처에 있었구요~ 
                                오후 5시까지 브레이크 타임이었는데 우연히 딱 5시에 도착해서 저희가 1등으로 들어갔답니다~ 
                                (저희가 들어오고 사람들이 줄줄이 오더라구요)
                                아주 고급스러운 분위기의 일식당이었구요~ 연인과 아니면 친구와 분위기있게 먹기 좋은 곳이었어요!
                                [사진]

                                메뉴를 보니 카이센동뿐만 아니라 사시미, 스시 등 다양한 해산물 요리를 판매하고 있어요 ~ 
                                주류도 사케, 하이볼, 맥주, 소주 등 친구들과 술한잔 하러 오는 것도 좋을 것 같아요!
                                [사진]

                                저희는 밥이 메인이었기 때문에 카이센동을 시켰어요! 우선 전체사진 한번 보여드릴게요ㅎㅎ
                                [사진]

                                하나씩 메뉴를 소개 드리자면
                                저는 생참다랑어 속살, 뱃살, 생연어가 들어간 혼마구로 사케 이구라동을 먹었구요,
                                [사진]
                                생연어 뿐만 아니라 참치회를 맛보고 싶다면 
                                제가 먹었던 이 메뉴 추천드려요!

                                여자친구는 생연어가 듬뿍 들어간 사케동을 먹었답니다~
                                [사진]
                                연어를 특히 좋아하신다면 사케동 추천드릴게요! 
                                두터운 생연어를 한점 한점 먹을 때 마다 너무 행복했답니다~~​

                                이렇게 맛있는 음식과 함께 술이 빠질 수 있나요!!!!
                                여자친구가 맛있는 하이볼 하나 시켜줬어요~
                                [사진]
                                이름하여 가을 단풍 하이볼 !!!
                                가을처럼 약간 씁쓸~하고 동시에 달콤한 하이볼이었어요ㅎㅎ
                                다음에 다시 찾아온다면 꼭 사시미와 함께 사케나 소주를... 아니 콜라를...
                                (술은 몸에 해로와요!)
                                먹고 싶네요~!

                                여러분들도 여의도에서 저녁을 드시게 된다면 정말 한번 꼭 드셔보셔요!
                                이번 포스팅은 여기서 마치겠습니다!
                                먹바!

                                - 내가 새로운 블로그글을 작성할꺼야 우리 닉네임은 먹찐 커플이야
                                - 여자친구와 함께 간 음식점에 대한 블로그글이어서 이 점 꼭 참고해서 작성해줘
                                - 내가 쓴글의 말투와 문장의 수와 비슷하게 참고해서 작성해줬으면 좋겠어
                                - 중간중간 [사진] 은 글과 함께 잘 어울리도록 작성해줘
                                - 나랑 여자친구가 시킨 음식은 위에 써두었으니 꼭 시킨 음식에 대해서만 언급해줬으면 좋겠어
                                - 글의 첫 부분에는 어떻게 가게 됐는지 설명이 들어가야해 젊은 커플이 왜 그 음식점을 갔는지 잘 지어내서 써줘
                                - 그리고 음식점의 분위기, 음식의 후기는 지어내지 말고 내가 입력한 리뷰데이터를 기반으로 사실적으로 작성할 수 있도록 해줘
                                - 글의 순서는 소개 -> 음식점 분위기 -> 메뉴 소개 -> 나와 여자친구가 시킨 음식 리뷰 -> 끝맺음 순으로 써줬으면 좋겠어
                                - 글의 마지막에는 이번 포스팅은 여기서 마치겠습니다!!! 먹바! 가 들어가야돼
                                """)
print(response.text,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

# # response = model.generate_content(f"""{response.text}를 이어서 글을 쓸건데 
# #                                 내가 정보를 줄게
# #                                 {text_summary}
# #                                 이게 정보고 이 정보를 바탕으로 글을 이어써줘
                                
# #                                 그리고 이 밑은 예제니깐 이 말투나 글쓰는 방식을 꼭 지켜주고
# #                                 예1)
# #                                 바로 "티 테라피"라는 찻집이에요!
# #                                 차뿐만 아니라 커피, 디저트까지! 
# #                                 맛있고 예쁜 것들이 한가득인 곳이랍니다ㅎㅎ
# #                                 메뉴판을 봤을 때 난생처음 보는 차들이 많았는데 
# #                                 찻집 이름이 테라피인 이유가 있더라구요 !
# #                                 몸 상태에 따라서 어떤 차가 좋을지 
# #                                 메뉴판에 표기되어있었어요😲
                                
# #                                 예2)
# #                                 베이글리스트는 마곡역과 발산역 사이에 위치해있구요! 매일 줄 서있는 것만 보고 포기했었는데 과감히 도전해봤습니다ㅎㅎ
# #                                 다행히 저희가 간 시간에는 대기가 많이 없었어요!
# #                                 웨이팅은 매장 앞 기계?에 웨이팅 등록을 하면 되고, 카카오톡으로 대기상황과 입장 알림을
# #                                 확인해볼 수 있습니다ㅎㅎ
# #                                 운좋게 1번으로 웨이팅 성공~~!!
# #                                 들어가자마자 인테리어가 눈에 띄더라구요 ~
# #                                 새로 생긴지 얼마 안되서 깔끔하기도 하고 인테리어를 굉장히 신경 쓴 모습이였어요ㅎㅎ
                                
# #                                 메뉴판, 그날의 분위기, 가기전에 어떤일을 우리가 겪었는지 등을 니가 위에 내가 준 정보를 바탕으로 창의적이게 글을 이어 써봐
# #                                 메뉴에 대한 이야기를 하기전 까지만 써줘 예제에 메뉴에 대한 소개 전이잖아 그치? 
# #                                 """)

# # print(response.text)