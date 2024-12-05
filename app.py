import streamlit as st
from restaurant_crawler import RestaurantInfo
from post_generator import PostGenerator
from streamlit_tags import st_tags
import datetime
import time

st.set_page_config(layout='wide')


st.title("맛집 탐방 블로그 작성 ")


if "disabled" not in st.session_state:
    st.session_state.disabled = False
if "loading" not in st.session_state:
    st.session_state.loading = False
if "task_completed" not in st.session_state:
    st.session_state.task_completed = False
if "error_message" not in st.session_state:
    st.session_state.error_message = ""
if "task_failed" not in st.session_state:
    st.session_state.task_failed = False   
    
    
    
def handle_submit():
    with col2 :
        if not user_input_r:
            st.session_state.error_message = "매장명을 입력해 주세요."
        elif not user_input_l:
            st.session_state.error_message = "지역명을 입력해 주세요."
        elif not user_input_d:
            st.session_state.error_message = "방문일자를 선택해 주세요."
        elif not api_key:
            st.session_state.error_message = "API KEY를 입력해 주세요."
        elif len(user_menues) < 1:
            st.session_state.error_message = "메뉴를 최소 1개 이상 입력해 주세요."
        else : # 조건 충족
            st.session_state.error_message=""
            st.session_state.disabled = True
            st.session_state.loading = True
            st.session_state.task_completed = False  # 작업 완료 초기화
            st.session_state.task_failed = False
    
import random
def test():
    if random.random() < 0.5:  # 50% 확률
        return True
    else:
        return False

col1, col2 = st.columns([2,4])

## 정보 제출 화면
with col1 : 

    placeholder1 = st.empty()
    placeholder2 = st.empty()
    
    with st.form("my_form"):
        user_input_r = st.text_input("매장명",key='매장명')
        user_input_l = st.text_input("지역명" ,placeholder = "ex) 등촌, 등촌역, 신사동")
        
        user_input_d = st.date_input("방문일자", datetime.datetime.now())
        
        user_menues = st_tags(
            label = "메뉴 입력",
            text = "메뉴를 입력해주세요",
            maxtags= 4
        )
        
        # Google API 키 입력 받기
        api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")
        
        
        
        submit_button = st.form_submit_button('**글 작성**',on_click=handle_submit ,disabled=st.session_state.disabled)
        
if st.session_state.disabled == True & st.session_state.loading == True :
    with col2:
        with st.spinner('로딩중...'):
            dd=test()
            time.sleep(5)
            if dd:
                st.session_state.disabled = False
                st.session_state.loading = False
                st.session_state.task_completed = True
                st.session_state.task_failed = False
                st.rerun()
            else :
                st.session_state.disabled = False
                st.session_state.loading = False
                st.session_state.task_completed = False
                st.session_state.task_failed =True
                failed= True
                st.rerun()
            
            

with col2:
    if st.session_state.error_message :
        st.error(st.session_state.error_message)
    elif st.session_state.task_completed:
        st.success("작업이 완료 되었습니다.")
        st.write('ㅎㅇ')
    elif st.session_state.task_failed:
        st.error("API 에러일듯")
    else :
        st.info("입력값을 작성해주세요")         
        
    
    
                
            
