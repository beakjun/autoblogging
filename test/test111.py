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
response = model.generate_content("""금09:00 - 18:0016:30 라스트오더
토09:00 - 19:0017:30 라스트오더
일09:00 - 19:0017:30 라스트오더
월09:00 - 18:0016:30 라스트오더
화정기휴무 (매주 화요일)
수09:00 - 18:0016:30 라스트오더
목09:00 - 18:0016:30 라스트오더
시간표 줄이지 말고 깔끔하게 표형식으로 정리해줘""")
print(response.text)


