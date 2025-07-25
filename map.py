import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from haversine import haversine, Unit

# ✅ 초기 북마크 (아이콘 포함)
default_bookmarks = {
    "서울": {"coords": [37.5665, 126.9780], "icon": "home"},
    "광주역": {"coords": [35.16535065, 126.9092577], "icon": "train"},
    "부산": {"coords": [35.1796, 129.0756], "icon": "flag"},
    "제주도": {"coords": [33.4996, 126.5312], "icon": "star"},
}

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = default_bookmarks

st.set_page_config(page_title="📍 위치 기반 지도 서비스", layout="wide")
st.title("🗺️ 현재 위치 + 북마크 + 아이콘 표시 + 경로 시각화")

# 📍 현재 위치 주소 입력
st.sidebar.subheader("📍 현재 위치 (주소 입력)")
geolocator = Nominatim(user_agent="streamlit_map_app")
current_address = st.sidebar.text_input("현재 위치 주소", "서울특별시 종로구 세종대로 209")

try:
    location = geolocator.geocode(current_address, timeout=5)
    if location:
        current_latlon = (location.latitude, location.longitude)
        st.sidebar.success(f"위도: {location.latitude:.6f}, 경도: {location.longitude:.6f}")
    else:
        current_latlon = (37.5665, 126.9780)
        st.sidebar.warning("❗ 위치를 찾을 수 없습니다. 기본값(서울) 사용.")
except Exception:
    current_latlon = (37.5665, 126.9780)
    st.sidebar.error("🚨 현재 위치 조회 실패. 기본값 사용")

# 📌 북마크 선택
st.sidebar.subheader("📌 북마크 선택")
selected_place = st.sidebar.selectbox("북마크", list(st.session_state.bookmarks.keys()))
selected_coords = st.session_state.bookmarks[selected_place]["coords"]

# ➕ 북마크 추가
with st.sidebar.expander("➕ 북마크 추가"):
    new_place = st.text_input("장소명 입력")
    new_icon = st.selectbox("아이콘 선택", ["star", "flag", "home", "train", "info-sign"])
    if st.button("🔍 장소 추가"):
        try:
            loc = geolocator.geocode(new_place, timeout=5)
            if loc:
                st.session_state.bookmarks[new_place] = {
                    "coords": [loc.latitude, loc.longitude],
                    "icon": new_icon
                }
                st.success(f"✅ 북마크 '{new_place}' 추가 완료")
            else:
                st.warning("❗ 장소를 찾을 수 없습니다.")
        except Exception:
            st.error("🚨 장소 추가 실패")

# 🔍 위치 검색
search_query = st.text_input("🔎 위치 검색", "")
search_result = None
map_center = selected_coords
zoom_level = 13

if search_query:
    try:
        loc = geolocator.geocode(search_query, timeout=5)
        if loc:
            search_result = {
                "name": loc.address,
                "lat": loc.latitude,
                "lon": loc.longitude
            }
            map_center = [loc.latitude, loc.longitude]
            zoom_level = 15
            st.success("✅ 검색 위치 확인됨")
            st.markdown(f"""
                **📌 주소:** {search_result['name']}  
                **🌐 위도:** {search_result['lat']:.6f}  
                **🌐 경도:** {search_result['lon']:.6f}
            """)
        else:
            st.warning("❗ 검색 결과를 찾을 수 없습니다.")
    except Exception:
        st.error("🚨 검색 실패")

# 거리/시간 계산 함수
def calculate_distance_and_time(loc1, loc2):
    distance_km = haversine(loc1, loc2, unit=Unit.KILOMETERS)
    walk_min = round((distance_km / 5) * 60)
    drive_min = round((distance_km / 50) * 60)
    return round(distance_km, 2), walk_min, drive_min

# 지도 생성
m = folium.Map(location=map_center, zoom_start=zoom_level)

# 현재 위치 마커
folium.Marker(
    location=current_latlon,
    tooltip="📍 현재 위치",
    popup=current_address,
    icon=folium.Icon(color="green", icon="user")
).add_to(m)

# 북마크 마커 + 아이콘 적용
for name, data in st.session_state.bookmarks.items():
    lat, lon = data["coords"]
    icon_type = data.get("icon", "info-sign")
    folium.Marker(
        location=[lat, lon],
        popup=name,
        tooltip=name,
        icon=folium.Icon(color="blue", icon=icon_type)
    ).add_to(m)

# 검색 위치 마커
if search_result:
    target_latlon = (search_result["lat"], search_result["lon"])
    folium.Marker(
        location=target_latlon,
        popup=search_result["name"],
        tooltip="🔍 검색 위치",
        icon=folium.Icon(color="red", icon="search")
    ).add_to(m)

    # 경로 시각화
    folium.PolyLine(locations=[current_latlon, target_latlon], color="purple", weight=3).add_to(m)

    # 거리 및 시간 출력
    dist_km, walk_min, drive_min = calculate_distance_and_time(current_latlon, target_latlon)
    st.info(f"""
        📏 거리: **{dist_km} km**  
        🚶 도보 시간: 약 {walk_min}분  
        🚗 차량 시간: 약 {drive_min}분
    """)

# 지도 출력
st_folium(m, width=900, height=600)
