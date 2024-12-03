import streamlit as st
from restaurant_crawler import RestaurantInfo
from post_generator import PostGenerator
from streamlit_tags import st_tags
import datetime

st.set_page_config(layout='wide')


st.title("맛집 탐방 블로그 작성 ")

col1, col2 = st.columns([2,4])
    # 텍스트 입력 받기


def disable():
    st.session_state.disabled = True
def enable():
    if "disabled" in st.session_state and st.session_state.disabled == True:
        st.session_state.disabled = False    
    
if "disabled" not in st.session_state:
    st.session_state.disabled = False
    
with col1 : 

    placeholder1 = st.empty()
    placeholder2 = st.empty()
    
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
        submit_button = st.form_submit_button('**글 작성**' ,disabled=st.session_state.disabled)
    
    with col2 :
        title=None
        post=None
        schedule=None
        placeholder = st.empty()
        placeholder.write("입력값을 입력해주세요") 
    

        #st.text_area(label="블로그 작성",placeholder="블로그 작성을 위한 기본 정보를 입력해주세요",height = 500,label_visibility="visible")
        if submit_button :
        # 입력 값 검증
            st.session_state.disabled = True
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
                placeholder.empty()
                with st.spinner("로딩 중..."):
                    restaurant=RestaurantInfo(user_input_r,user_input_l)
                    info=restaurant.crawling_restaurant()
                    try :
                        postgen = PostGenerator(info,user_menues,user_input_d,api_key)
                        model = postgen.genai_model()
                        title = postgen.generate_title()
                        post = postgen.generate_post()
                        schedule = postgen.generate_schedule()
                    except ValueError as e:
                        if "API key not valid" in str(e):
                            st.error("API 오류: 유효하지 않은 API 키입니다. API 키를 확인하세요.")
                        else:
                            st.error(f"모델 사용 중 오류 발생: {str(e)}")  # 모델 사용 중 다른 오류 처리
                if title is not None and post is not None:
                    placeholder.empty()
                    st.text_input("블로그 타이틀", value=title)
                    st.text_area("포스트", value=f"{post}\n\n{schedule}", height=500)
                    
                else:
                    st.error("포스트 또는 스케줄 생성에 실패했습니다.")
                  # 초기 상태: 그림과 입력 안내 텍스트 표시

                               
        
