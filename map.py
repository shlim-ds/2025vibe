import streamlit as st
import folium
from streamlit_folium import st_folium

# 샘플 북마크 지점 (이름, 위도, 경도)
bookmarks = {
    "서울 시청": (37.5665, 126.9780),
    "부산 해운대": (35.1587, 129.1604),
    "제주 공항": (33.5113, 126.4983),
    "대전역": (36.3327, 127.4342),
    "광주광역시청": (35.1595, 126.8526)
}

st.set_page_config(page_title="북마크 지도", layout="wide")
st.title("📍 북마크를 이용한 지도 보기")

# 북마크 선택
selected_places = st.multiselect("📌 지도에 표시할 북마크를 선택하세요:", list(bookmarks.keys()))

# 지도 초기화 (기본 위치는 대한민국 중심)
m = folium.Map(location=[36.5, 127.8], zoom_start=6)

# 선택한 북마크 마커 추가
for place in selected_places:
    lat, lon = bookmarks[place]
    folium.Marker([lat, lon], tooltip=place, popup=place).add_to(m)

# Streamlit에 지도 출력
st_folium(m, width=900, height=600)
