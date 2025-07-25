import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 데이터 로딩
@st.cache_data
def load_data():
    return pd.read_csv("202506_202506_연령별인구현황_월간_남여구분.csv", encoding="cp949")

df = load_data()

# 지역 목록 선택
st.title("👥 2025년 6월 연령별 인구 피라미드")
region_list = df["행정구역"].unique()
selected_region = st.selectbox("📍 행정구역 선택", region_list)

# 선택 지역 데이터 추출
region_df = df[df["행정구역"] == selected_region].iloc[0]

# 연령별 컬럼 분리
male_cols = [col for col in df.columns if "남_" in col and "세" in col]
female_cols = [col for col in df.columns if "여_" in col and "세" in col]
ages = [col.split("_")[-1] for col in male_cols]

# 숫자 처리 함수
def clean_number(val):
    if pd.isna(val):
        return 0
    return int(str(val).replace(",", ""))

# 인구값 정리
male_values = region_df[male_cols].apply(clean_number).values * -1
female_values = region_df[female_cols].apply(clean_number).values

# 그래프 생성
fig = go.Figure()
fig.add_trace(go.Bar(y=ages, x=male_values, name="남성", orientation='h', marker=dict(color='steelblue')))
fig.add_trace(go.Bar(y=ages, x=female_values, name="여성", orientation='h', marker=dict(color='lightcoral')))

fig.update_layout(
    title=f"{selected_region} 연령별 인구 피라미드 (2025년 6월)",
    barmode='relative',
    xaxis=dict(title='인구 수', tickvals=[-50000, -25000, 0, 25000, 50000],
               ticktext=['50,000', '25,000', '0', '25,000', '50,000']),
    yaxis=dict(title='연령'),
    height=800
)

st.plotly_chart(fig, use_container_width=True)
