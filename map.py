import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# 🌍 기본 북마크 정의
bookmarks = {
    "서울": [37.5665, 126.9780],
    "부산": [35.1796, 129.0756],
    "대구": [35.8714, 128.6014],
    "광주": [35.1595, 126.8526],
    "제주도": [33.4996, 126.5312],
}

# 📄 페이지 설정
st.set_page_config(page_title="정확한 위치 검색 지도", layout="wide")
st.title("📍 위치 검색 및 북마크 지도")
st.markdown("북마크 또는 검색어로 지도를 탐색할 수 있습니다. 검색된 위치의 정확한 주소와 좌표도 함께 확인하세요.")

# 📌 북마크 선택
selected_city = st.sidebar.selectbox("📍 북마크에서 위치 선택", list(bookmarks.keys()))
default_location = bookmarks[selected_city]

# 🔍 위치 검색
search_query = st.text_input("🔍 위치 검색 (예: 서울시청, 강남역, 제주 공항 등)", "")
search_result = None
map_location = default_location
zoom_level = 12

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

            # ✅ 검색된 위치 정보 출력
            st.success("✅ 정확한 위치를 찾았습니다!")
            st.markdown(f"""
                **📌 주소:** {search_result['name']}  
                **🌐 위도:** {search_result['lat']:.6f}  
                **🌐 경도:** {search_result['lon']:.6f}
            """)
        else:
            st.warning("❗ 위치를 찾을 수 없습니다. 정확한 지명을 입력해 주세요.")
    except (GeocoderTimedOut, GeocoderServiceError):
        st.error("🚨 위치 검색 중 오류가 발생했습니다. 인터넷 상태를 확인하거나 잠시 후 다시 시도해 주세요.")

# 🗺️ 지도 객체 생성
m = folium.Map(location=map_location, zoom_start=zoom_level)

# 📍 북마크 마커 추가
for city, (lat, lon) in bookmarks.items():
    folium.Marker(
        location=[lat, lon],
        popup=city,
        tooltip=city,
        icon=folium.Icon(color="blue" if city == selected_city else "gray")
    ).add_to(m)

# 🔴 검색 결과 마커 추가
if search_result:
    folium.Marker(
        location=[search_result["lat"], search_result["lon"]],
        popup=f"🔍 {search_result['name']}",
        tooltip="검색된 위치",
        icon=folium.Icon(color="red", icon="search")
    ).add_to(m)

# 🌐 지도 출력
st_folium(m, width=900, height=600)
