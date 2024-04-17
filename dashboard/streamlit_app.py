# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import json

#######################
# 페이지 정의
st.set_page_config(
    page_title="청소년 건강지표",
    page_icon="👦🏻🧒🏻",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# 데이터 불러오기
df = pd.read_csv('./dashboard/data/health_scores_by_region.csv', encoding='utf-8')

# 한국 지도 데이터
with open('./dashboard/data/korea_geojson2.geojson', encoding='UTF-8') as f:
    data_geojson = json.load(f)
    
# 각 지역의 이름 변경
for feature in data_geojson['features']:
    if feature['properties']['CTP_KOR_NM'] == '제주특별자치도':
        feature['properties']['CTP_KOR_NM'] = '제주'
    elif feature['properties']['CTP_KOR_NM'] == '경상남도':
        feature['properties']['CTP_KOR_NM'] = '경남'
    elif feature['properties']['CTP_KOR_NM'] == '경상북도':
        feature['properties']['CTP_KOR_NM'] = '경북'
    elif feature['properties']['CTP_KOR_NM'] == '전라남도':
        feature['properties']['CTP_KOR_NM'] = '전남'
    elif feature['properties']['CTP_KOR_NM'] == '전라북도':
        feature['properties']['CTP_KOR_NM'] = '전북'
    elif feature['properties']['CTP_KOR_NM'] == '충청남도':
        feature['properties']['CTP_KOR_NM'] = '충남'
    elif feature['properties']['CTP_KOR_NM'] == '충청북도':
        feature['properties']['CTP_KOR_NM'] = '충북'
    elif feature['properties']['CTP_KOR_NM'] == '강원도':
        feature['properties']['CTP_KOR_NM'] = '강원'
    elif feature['properties']['CTP_KOR_NM'] == '경기도':
        feature['properties']['CTP_KOR_NM'] = '경기'
    elif feature['properties']['CTP_KOR_NM'] == '세종특별자치시':
        feature['properties']['CTP_KOR_NM'] = '세종'
    elif feature['properties']['CTP_KOR_NM'] == '울산광역시':
        feature['properties']['CTP_KOR_NM'] = '울산'
    elif feature['properties']['CTP_KOR_NM'] == '대전광역시':
        feature['properties']['CTP_KOR_NM'] = '대전'
    elif feature['properties']['CTP_KOR_NM'] == '광주광역시':
        feature['properties']['CTP_KOR_NM'] = '광주'
    elif feature['properties']['CTP_KOR_NM'] == '인천광역시':
        feature['properties']['CTP_KOR_NM'] = '인천'
    elif feature['properties']['CTP_KOR_NM'] == '대구광역시':
        feature['properties']['CTP_KOR_NM'] = '대구'
    elif feature['properties']['CTP_KOR_NM'] == '부산광역시':
        feature['properties']['CTP_KOR_NM'] = '부산'
    elif feature['properties']['CTP_KOR_NM'] == '서울특별시':
        feature['properties']['CTP_KOR_NM'] = '서울'

for x in data_geojson['features']:
    x['id'] = x['properties']['CTP_KOR_NM']

#######################
# 사이드바
with st.sidebar:
    st.title('👦🏻 청소년 건강 지표 🧒🏻')
    
    category_list = ['총점', '개인건강 점수', '외부환경요인 점수']
    selected_category = st.selectbox('지도에 보여줄 점수를 선택하세요', category_list)
    
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

#######################
# 플롯

# Choropleth map (단계구분도)
def make_choropleth(input_df, input_geojson, input_category, input_color_theme):
    fig = px.choropleth_mapbox(
        input_df,
        geojson=input_geojson,
        locations='지역',
        color=input_category,
        color_continuous_scale=input_color_theme,
        mapbox_style="carto-positron",
        zoom=5.5,
        center={"lat": 35.757981, "lon": 127.661132},
        opacity=0.6,
        labels={input_category: f'{input_category}'}
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

#######################
# 대시보드 메인 패널
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### 전국 청소년 건강 점수')
    mean_ALL = round(df['총점'].mean(), 2)  # 소수점 두 자리까지 반올림
    pers_ALL = round(df['개인건강 점수'].mean(), 2)  # 소수점 두 자리까지 반올림
    ext_ALL = round(df['외부환경요인 점수'].mean(), 2)  # 소수점 두 자리까지 반올림
    st.metric(label='평균 총점', value=mean_ALL)
    st.metric(label='평균 개인건강 점수', value=pers_ALL)
    st.metric(label='평균 외부환경요인 점수', value=ext_ALL)
    

with col[1]:
    st.markdown(f'#### 지역 별 {selected_category} 지도')
    choropleth = make_choropleth(df, data_geojson, selected_category, selected_color_theme)
    st.plotly_chart(choropleth, use_container_width=True)
    st.write('지도 위에 마우스를 올리면 지역 별 점수를 확인하실 수 있습니다.')
    
with col[2]:
    st.markdown('#### 지역 별 점수')

    st.dataframe(df,
                 height=500,
                 column_order=("지역", "총점"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "지역": st.column_config.TextColumn(
                        "지역",
                    ),
                    "총점": st.column_config.ProgressColumn(
                        "총점",
                        format="%f",
                        min_value=0,
                        max_value=max(df.총점),
                     )}
                 )


st.expander('About', expanded=True)

st.subheader('About')

st.write('''
         - :orange[**청소년 건강지표**]란: 청소년 정책자료 및 전문가 자문을 통해 청소년 건강에 주요한 영향을 미치는 지표를 설정하고, 지역 간 현황을 점수로 비교함
         - 활용 데이터: [여성가족부 「청소년매체이용및유해환경실태조사」](https://www.mogef.go.kr/io/ind/io_ind_f016.do) , [교육부+질병관리청 「청소년건강행태조사」](http://www.kdca.go.kr/yhs/) 
         - 상세 지표 : [팀 청록 - 청소년 건강 지표 전문](https://docs.google.com/spreadsheets/d/1iotx4Pg6U96wctuZgBsaT0DxnhEYDtJAKGSHxdt-nl8/edit?usp=sharing)
         - 지표 선정 기준: 유관기관 연구 및 정책자료 내 추적 지표 반영 (여성가족부, 교육부, 질병관리청)
         - 점수 계산법: 전문가 자문을 통한 상세 지표 간 순위 선정 후 정책자료 언급 빈도 분석을 통한 분류 간 가중치 종합 설정 - [상세보기](https://drive.google.com/file/d/1TTI8lkIMmBB03J81d7OD6X4MBEQ8f_TV/view?usp=sharing) 
         - 자문 위원: 서울대학교 보건대학원 교수 조성일, 한국방송통신대학교 청소년교육과 교수 김진호, 교사 정준화, 교사 안정훈, 전문상담교사 김경채, 영양사 최문희
        ''')

st.write()
st.write('_Copyright ⓒ 2024 by 청록(김창엽,박시현,우상덕,인다정,조은비) All Contents cannot be copied without permission._')