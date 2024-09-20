# key = 'AIzaSyCW9fwk8jBkVQ45fiKvVHFLj1971yI1X-o'

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

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



response = model.generate_content("인생의 의미란 무엇일까?")
print(response.text)
