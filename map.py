import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# ✅ 북마크 목록 (광주역 포함)
bookmarks = {
    "서울": [37.5665, 126.9780],
    "부산": [35.1796, 129.0756],
    "대구": [35.8714, 128.6014],
    "광주": [35.1595, 126.8526],
    "제주도": [33.4996, 126.5312],
    "광주역": [35.16535065, 126.9092577],  # 정확한 광주역 좌표 추가
}

# 📄 Streamlit UI 설정
st.set_page_config(page_title="📍 북마크 + 위치 검색 지도", layout="wide")
st.title("🗺️ 북마크 지도 + 위치 검색")
st.markdown("북마크에서 선택하거나 검색어로 정확한 위치를 지도에 표시합니다.")

# 📌 북마크 선택
selected_city = st.sidebar.selectbox("📍 북마크 선택", list(bookmarks.keys()))
default_location = bookmarks[selected_city]

# 🔎 사용자 검색어 입력
search_query = st.text_input("🔍 위치 검색 (예: 강남역, 광주역, 서울시청 등)", "")
search_result = None
map_location = default_location
zoom_level = 12

# 🔍 위치 검색 처리
if search_query:
    geolocator = Nominatim(user_agent="streamlit_map_app")
    try:
        location = geolocator.geocode(search_query, timeout=5)
        if location:
            search_result = {
                "name": location.address,
                "lat": location.latitude,
                "lon": location.longitude
            }
            map_location = [location.latitude, location.longitude]
            zoom_level = 15  # 검색 시 확대
            st.success("✅ 위치 검색 성공!")
            st.markdown(f"""
                **📌 주소:** {search_result['name']}  
                **🌐 위도:** {search_result['lat']:.6f}  
                **🌐 경도:** {search_result['lon']:.6f}
            """)
        else:
            st.warning("❗ 위치를 찾을 수 없습니다. 더 구체적으로 입력해 주세요.")
    except (GeocoderTimedOut, GeocoderServiceError):
        st.error("🚨 위치 검색 중 오류 발생. 잠시 후 다시 시도해 주세요.")

# 🗺️ 지도 생성
m = folium.Map(location=map_location, zoom_start=zoom_level)

# 📍 북마크 마커 추가
for city, (lat, lon) in bookmarks.items():
    folium.Marker(
        location=[lat, lon],
        popup=city,
        tooltip=city,
        icon=folium.Icon(color="blue" if city == selected_city else "gray")
    ).add_to(m)

# 🔴 검색 위치 마커 추가
if search_result:
    folium.Marker(
        location=[search_result["lat"], search_result["lon"]],
        popup=f"🔍 {search_result['name']}",
        tooltip="검색된 위치",
        icon=folium.Icon(color="red", icon="search")
    ).add_to(m)

# 🌍 지도 출력
st_folium(m, width=900, height=600)
