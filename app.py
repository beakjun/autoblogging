import streamlit as st
from restaurant_crawler import RestaurantInfo
from post_generator import PostGenerator
from streamlit_tags import st_tags
import datetime

st.set_page_config(layout='wide')


st.title("맛집 탐방 블로그 작성 ")

col1, col2 = st.columns([2,4])
# 텍스트 입력 받기


with col1 : 


    with st.form("my_form"):
        user_input_r = st.text_input("매장명")
        user_input_l = st.text_input("지역명" ,placeholder = "ex) 등촌, 등촌역, 신사동")
        
        user_input_d = st.date_input("방문일자", datetime.datetime.now())
        
        user_menues = st_tags(
            label = "메뉴 입력",
            text = "메뉴를 입력해주세요",
            maxtags= 4
        )
        
        # Google API 키 입력 받기
        api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")
        submit_button = st.form_submit_button('**글 작성**')

    
    with col2 :
        
        placeholder = st.empty()
    
    # 초기 상태: 그림과 입력 안내 텍스트 표시
        with placeholder.container():
            #st.image("path/to/your/image.png")  # 그림 경로를 적어주세요
            st.write("입력값을 입력해주세요")
        #st.text_area(label="블로그 작성",placeholder="블로그 작성을 위한 기본 정보를 입력해주세요",height = 500,label_visibility="visible")
        if submit_button :
        # 입력 값 검증
            if not user_input_r:
                st.error("매장명을 입력해 주세요.")
            elif not user_input_l:
                st.error("지역명을 입력해 주세요.")
            elif not user_input_d:
                st.error("방문일자를 선택해 주세요.")
            elif not api_key:
                st.error("방문일자를 선택해 주세요.")
            elif len(user_menues) < 1:
                st.error("메뉴를 최소 1개 이상 입력해 주세요.")
            else:
                # 모든 입력이 유효할 경우 처리 로직
                placeholder = st.empty()
                with st.spinner("로딩 중..."):
                    restaurant=RestaurantInfo(user_input_r,user_input_l)
                    info=restaurant.crawling_restaurant()
                    postgen = PostGenerator(info,user_menues,user_input_d,api_key)
                    title = postgen.generate_title()
                    post = postgen.generate_post()
                    schedule = postgen.generate_schedule()
                st.text_input("블로그 타이틀",values=title)
                st.text_are("포스트",values=f"{post} + \n\n + {schedule}", height= 500)
                
                
                
          
        
