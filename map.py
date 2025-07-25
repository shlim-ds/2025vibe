import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# 북마크 데이터 (도시명: [위도, 경도])
bookmarks = {
    "서울": [37.5665, 126.9780],
    "부산": [35.1796, 129.0756],
    "대구": [35.8714, 128.6014],
    "광주": [35.1595, 126.8526],
    "제주도": [33.4996, 126.5312],
}

# 🌐 Streamlit UI 설정
st.set_page_config(page_title="📌 북마크 지도 + 위치 검색", layout="wide")
st.title("📍 북마크 지도 + 위치 검색")
st.markdown("북마크를 선택하거나 직접 위치를 검색하여 지도에서 확인해보세요.")

# 🔎 위치 검색 기능
search_query = st.text_input("🔍 위치 검색 (예: 강남역, 서울대학교, 남산타워 등)", "")
geolocator = Nominatim(user_agent="streamlit_map_app")

# 🧭 북마크 선택
selected_city = st.sidebar.selectbox("🗺️ 북마크 위치 선택", list(bookmarks.keys()))

# 🗺️ 지도 초기화
default_location = bookmarks[selected_city]
map_location = default_location
zoom_level = 12
search_result = None

# 사용자가 위치 검색한 경우
if search_query:
    try:
        location = geolocator.geocode(search_query)
        if location:
            map_location = [location.latitude, location.longitude]
            zoom_level = 15  # 검색 시 확대
            search_result = {
                "name": location.address,
                "lat": location.latitude,
                "lon": location.longitude
            }
        else:
            st.warning("❌ 위치를 찾을 수 없습니다. 다시 입력해 주세요.")
    except Exception as e:
        st.error(f"위치 검색 중 오류 발생: {e}")

# 🗺️ folium 지도 생성
m = folium.Map(location=map_location, zoom_start=zoom_level)

# 북마크 마커 추가
for city, (lat, lon) in bookmarks.items():
    folium.Marker(
        location=[lat, lon],
        popup=f"{city}",
        tooltip=city,
        icon=folium.Icon(color="blue" if city == selected_city else "gray")
    ).add_to(m)

# 검색 결과 마커 추가
if search_result:
    folium.Marker(
        location=[search_result["lat"], search_result["lon"]],
        popup=f"🔍 {search_result['name']}",
        tooltip="검색 결과",
        icon=folium.Icon(color="red", icon="search")
    ).add_to(m)

# 📌 Streamlit에 지도 표시
st_folium(m, width=900, height=600)
