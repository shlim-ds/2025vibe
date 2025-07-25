import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from haversine import haversine, Unit

# Streamlit 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = {
        "서울": [37.5665, 126.9780],
        "부산": [35.1796, 129.0756],
        "광주역": [35.16535065, 126.9092577],
        "제주도": [33.4996, 126.5312],
    }

# 페이지 설정
st.set_page_config(page_title="🗺️ 위치 지도 + 북마크 + 거리 계산", layout="wide")
st.title("📍 위치 기반 지도 탐색")
st.markdown("북마크를 추가하고, 현재 위치 기준으로 거리 및 예상 시간을 확인할 수 있어요.")

# 현재 위치 입력 (사용자가 직접 입력)
st.sidebar.subheader("📍 현재 위치 입력")
current_lat = st.sidebar.number_input("위도", format="%.6f", value=37.5665)
current_lon = st.sidebar.number_input("경도", format="%.6f", value=126.9780)
current_location = (current_lat, current_lon)

# 북마크 선택
st.sidebar.subheader("📌 북마크 선택")
selected_place = st.sidebar.selectbox("북마크에서 선택", list(st.session_state.bookmarks.keys()))
selected_coords = st.session_state.bookmarks[selected_place]

# ➕ 북마크 추가
with st.sidebar.expander("➕ 북마크 추가"):
    new_place = st.text_input("추가할 장소명", "")
    if st.button("🔍 위치 검색하여 추가"):
        if new_place:
            geolocator = Nominatim(user_agent="streamlit_map_app")
            try:
                location = geolocator.geocode(new_place, timeout=5)
                if location:
                    lat, lon = location.latitude, location.longitude
                    st.session_state.bookmarks[new_place] = [lat, lon]
                    st.success(f"✅ 북마크 추가 완료: {new_place} ({lat:.5f}, {lon:.5f})")
                else:
                    st.warning("❗ 위치를 찾을 수 없습니다. 정확히 입력해 주세요.")
            except Exception:
                st.error("🚨 위치 검색 실패. 잠시 후 다시 시도해 주세요.")

# 🔍 검색어로 위치 검색
search_query = st.text_input("🔎 위치 검색 (예: 강남역, 남산타워 등)", "")
search_result = None
map_center = selected_coords
zoom_level = 13

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
            map_center = [location.latitude, location.longitude]
            zoom_level = 15
            st.success("✅ 위치 검색 성공!")
            st.markdown(f"""
                **📌 주소:** {search_result['name']}  
                **🌐 위도:** {search_result['lat']:.6f}  
                **🌐 경도:** {search_result['lon']:.6f}
            """)
        else:
            st.warning("❗ 위치를 찾을 수 없습니다.")
    except Exception:
        st.error("🚨 위치 검색 실패. 인터넷 상태를 확인해 주세요.")

# 거리 및 시간 계산
def calculate_distance_and_time(loc1, loc2):
    try:
        distance_km = haversine(loc1, loc2, unit=Unit.KILOMETERS)
        walking_time = distance_km / 5 * 60  # 평균 도보 속도 5km/h
        driving_time = distance_km / 50 * 60  # 평균 차량 속도 50km/h
        return round(distance_km, 2), round(walking_time), round(driving_time)
    except:
        return None, None, None

# 지도 생성
m = folium.Map(location=map_center, zoom_start=zoom_level)

# 현재 위치 마커
folium.Marker(
    location=current_location,
    tooltip="📍 현재 위치",
    popup="현재 위치",
    icon=folium.Icon(color="green", icon="user")
).add_to(m)

# 북마크 마커 추가
for name, (lat, lon) in st.session_state.bookmarks.items():
    folium.Marker(
        location=[lat, lon],
        popup=name,
        tooltip=name,
        icon=folium.Icon(color="blue" if name == selected_place else "gray")
    ).add_to(m)

# 검색 위치 마커 추가
if search_result:
    folium.Marker(
        location=[search_result["lat"], search_result["lon"]],
        popup=f"🔍 {search_result['name']}",
        tooltip="검색 결과",
        icon=folium.Icon(color="red", icon="search")
    ).add_to(m)

    # 거리 계산
    dist_km, walk_min, drive_min = calculate_distance_and_time(current_location, (search_result["lat"], search_result["lon"]))
    if dist_km:
        st.info(f"📏 현재 위치 → 검색 위치 거리: **{dist_km}km**\n🚶 도보 약 {walk_min}분 / 🚗 차량 약 {drive_min}분 소요")

# 지도 표시
st_folium(m, width=900, height=600)
