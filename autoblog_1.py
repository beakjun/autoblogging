import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

class restaurant_post_generator: # gemini_api 활용
    def __init__(self,restaurant_info::dict, menu::list ,api_key):
        self.restaurant_loc = restaurant_info['loc']
        self.restaurant_nm = restaurant_info['name']
        self.reviews = restaurant_info['reviews']
        self.schedule = restaurant_info['schedule']
        self.menu = menu
        self.api_key = api_key
        self.model = self._configure_model(api_key)

   # 메뉴 추가 메서드
    def add_menu_item(self, item):
        self.menu.append(item)  # 새로운 메뉴 항목 추가

    # 메뉴 제거 메서드
    def remove_menu_item(self):
        if item in self.menu:
            self.menu.pop()      
    
        
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
        
        return model
    
    