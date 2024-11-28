import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from logger_config import get_logger
 
class PostGenerator: # gemini_api 활용
    def __init__(self,restaurant_info:dict, menu:list, visit_date: str,api_key:str):
        self.logger = get_logger(self.__class__.__name__)
        self.restaurant_info = restaurant_info
        self.restaurant_info.update({
            "menu": menu,
            "visit_date": visit_date
        })
        self.api_key = api_key
        self.model = self.genai_model()
        
        
    

   # 메뉴 추가 메서드
    def add_menu_item(self, item):
        self.menu.append(item)  # 새로운 메뉴 항목 추가
        self.logger.info(f"{item} 메뉴가 추가 되었습니다.")
    # 메뉴 제거 메서드
    def remove_menu_item(self):
        if item in self.menu:
            removed_menu=self.menu.pop()
            self.logger.info(f"{removed_menu} 메뉴가 제거 되었습니다.")      
    
        
    def genai_model(self):
        genai.configure(api_key=self.api_key)

        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        model = genai.GenerativeModel('gemini-1.5-flash',
                                    generation_config=generation_config)
        self.logger.info("모델 api 로드 완료") 
        return model
    
    def generate_title(self):
    
        response = self.model.generate_content(f"""{self.restaurant_info} 이와같은 음식점 정보를 
                                    바탕으로 블로그 포스팅을 할껀데 제목을 아래의 예제와 같이 지을꺼야
                                    예제) [연남] 마포 브런치 맛집 '버우드' / 서이추환영 ,[안국역/북촌] 힐링되는 찻집 카페 '티테라피' / 서이추환영
                                    - 첫번째로 들어가는 것은 []안에 지역을 넣어줘 역을 기준으로 넣어주는게 제일 좋고 아니라면 그 음식점이 있는 유명한 지명을 넣어줘도 돼
                                    - 두번째 이 음식점의 대표메뉴나 대표표현을 이용해서 이 음식점의 특징을 넣어줘 예를 들어 힐링되는 찻집 카페 처럼 말이야
                                    - 그리고 세번째는 ''안에 음식점 이름을 넣어줘
                                    - 마지막으로는 / 서이추환영을 꼭 넣어주길 바라
                                    - 다른 옵션이나 부가 설명은 답변안에 넣지말고 제목만 추출해서 쓸 수 있게 짧게 답변 줬으면 좋겠어
                                    """)    
        self.logger.info("블로그 제목 완성")               
        return response.text
    
    def generate_post(self):
        response = self.model.generate_content(f"""{self.restaurant_info} 이와 같은 음식점 정보를 바탕으로 블로그 포스팅을 할꺼야 아래는 내가 예전에 쓴 글이니
                                이와 같이 써줘.
                                
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

                                - 내 블로그 닉네임이 "먹찐 커플"이야 그러니깐 첫 문장은 "먹찐 커플"임을 밝히고 시작했으면 좋겠어
                                - 여자친구와 함께 간 음식점에 대한 블로그글이어서 이 점 꼭 참고해서 작성해줘
                                - 내가 쓴글의 말투와 문장의 수와 비슷하게 참고해서 작성해줬으면 좋겠어
                                - 니가 거리에 대한 정보는 알아서 몇 분정도 걸어가면 있다던지로 대체해줘
                                - 중간중간 글 아래 해당하는 글에 대한 '[사진]' 한개를 넣어줘
                                - 내가 준 정보의 menu가 내가 시킨 음식이니깐 이것에 대해서만 글을 써야해
                                - 글의 첫 부분에는 어떻게 가게 됐는지 설명이 들어가야해 젊은 커플이 왜 그 음식점을 갔는지 잘 지어내서 써줘
                                - 그리고 음식점의 분위기, 음식의 후기는 지어내지 말고 내가 입력한 리뷰 정보를 기반으로 사실적으로 작성할 수 있도록 해
                                - 가격은 시간에 따라서 변할 수 있으니 언급해주지 않았으면 좋겠어
                                - 글의 순서는 소개 -> 음식점 분위기 -> 메뉴 소개 -> 나와 여자친구가 시킨 음식 리뷰 -> 추천글 ->끝맺음 순으로 써줬으면 좋겠어
                                - 사진은 가게내부사진, 메뉴판사진, 시킨 메뉴의 전체사진, 각 메뉴의 사진만으로 구성해줘
                                - 가게에서 다루는 메뉴에 대해서 소개할 때 내가 준 리뷰 정보에 나와있는 음식이거나 내가 시킨 음식들 정도만 언급하고 다양한 음식들이 있다 이정도 수준만 언급해봐
                                - 각 메뉴리뷰는 한개씩 사진과 함께 글을 작성해줘 또한 메뉴에 대해서 설명할 때 리뷰정보에 있는 재료들만 사실적으로 언급해줘
                                - 리뷰에서 봤다 이런 표현은 자제해줘
                                - 글의 마지막에는 이번 포스팅은 여기서 마치겠습니다!!! 먹바! 가 들어가야돼
                                """)
        self.logger.info("블로그 포스트 글 완성")  
        return response.text
    
    
    def generate_schedule(self):
        response = self.model.generate_content(f"""{self.restaurant_info['schedule']}은 음식점의 영업시간 정보야 이를 블로그에 정보로 넣을 건데 다음과 같이 적어줘
                                    - 영업시간 이라는 단어로 시작해줘 이부분에만 '*'는 빼줘
                                    - 영업시간이 같은 요일끼리 묶어줘 예) 월요일 - 금요일, 토요일 - 일요일
                                    - 요일 뒤, 라스트 오더, 브레이크 타임뒤에는 한줄 띄고 시간을 적어줘
                                    - 영업시간을 두개로 쪼개지말고 브레이크 타임 고려하지 말고 꼭 한줄에 적어줘
                                    - 브레이크 타임이나 라스트 오더 시간이 있다면 적어줘
                                    - 정기 휴무가 있다면 제일 마지막에 적어줘 없으면 적지마
                                    - 마지막으로 네이버에 등록된 업체 등록 영업 시간입니다* 를 이대로 똑같이 맨 아래에 꼭 넣어줘, 영업 시간입니다 뒤에 * 잊지말고 넣어주고
                                    """)
        self.logger.info("영업시간 작성 완료")  
        return response.text



def main():
    
    # 테스트용 데이터
    import json    
    file_path = '/home/wjsqorwns93/bj/autoblogging/restaurant_data.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    GOOGLE_API_KEY = 'AIzaSyBiKq7ZZp_Rndr7IA6K0_2ZeGrwJeWUqxI'
    postgenerator = PostGenerator(data,['아지텐동','에비텐카레'],'2024-08-02',GOOGLE_API_KEY)

    aa=postgenerator.generate_schedule()
    
    #bb=postgenerator.generate_post()
    #cc=postgenerator.generate_title()
    print(aa)

if __name__ == "__main__":
    main()