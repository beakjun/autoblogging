# key = 'AIzaSyCW9fwk8jBkVQ45fiKvVHFLj1971yI1X-o'

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import sys



def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


GOOGLE_API_KEY = 'AIzaSyCW9fwk8jBkVQ45fiKvVHFLj1971yI1X-o'
genai.configure(api_key=GOOGLE_API_KEY)



# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}


model = genai.GenerativeModel('gemini-1.5-flash',
                              generation_config=generation_config)


##제목 테스트
response = model.generate_content("""강남역 김치찌개 맛집 백제김치찌게를 블로그를 쓸건데 제목을 
                                  예 : [연남] 마포 브런치 맛집 '버우드' / 서이추환영 ,[안국역/북촌] 힐링되는 찻집 카페 '티테라피' / 서이추환영
                                  이런식으로 똑같이 만들어봐""")
print(response.text)


##소개글 테스트
response = model.generate_content("""내 블로그 id가 muczzin커플이거든 맛집블로그를 쓰는데 강남역 백제김치찌게에 대한 맛집 소개글을 쓸거야
                                  앞에 개요를
                                  예) 안녕하세요 !! muczzin커플입니다ㅎㅎ


1주일 만에 글을 쓰네요..😭😭

더 부지런히 쓰려고 했는데 작심삼일이랄까...

아무튼!! 오늘은 안국역에 위치한 힐링 카페(?) 

찻집을 소개해 드릴께요!!
이런식으로 쓰려고 해 똑같이 쓰지말고 비슷하게 써주고 날씨라던지 그날은 어떤 분위기어서 방문했다던지 이런걸 자유롭게 소개글 써줘봐 개요만""")
print(response.text)




