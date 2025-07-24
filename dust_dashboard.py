import requests
import streamlit as st
import pandas as pd

# ✅ 사용자 API 키 입력
API_KEY = "여기에_당신의_API_KEY를_입력하세요"  # data.go.kr에서 발급받은 키

# ✅ 전국 시도 리스트
sido_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
             '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']

# ✅ 등급 계산 함수 + 이모지
def get_grade_emoji(pm_value, is_pm25=False):
    try:
        pm_value = int(pm_value)
    except:
        return "❓ 정보 없음"

    if is_pm25:
        if pm_value <= 15:
            return "🟢 좋음"
        elif pm_value <= 35:
            return "🟡 보통"
        elif pm_value <= 75:
            return "🟠 나쁨"
        else:
            return "🔴 매우나쁨"
    else:
        if pm_value <= 30:
            return "🟢 좋음"
        elif pm_value <= 80:
            return "🟡 보통"
        elif pm_value <= 150:
            return "🟠 나쁨"
        else:
            return "🔴 매우나쁨"

# ✅ 미세먼지 정보 조회 함수
@st.cache_data(ttl=600)
def get_air_quality_data(sido_name):
    url = f"http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/" \
          f"getCtprvnRltmMesureDnsty?serviceKey={API_KEY}" \
          f"&returnType=json&numOfRows=100&pageNo=1&sidoName={sido_name}&ver=1.0"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json().get("response", {}).get("body", {}).get("items", [])
        return pd.DataFrame(items)
    else:
        return pd.DataFrame()

# ✅ Streamlit UI 구성
st.set_page_config(page_title="🌫 미세먼지 대시보드", layout="wide")
st.title("🌏 대한민국 미세먼지 대시보드")
st.markdown("🧭 시/도를 선택하면 지역 내 측정소별 미세먼지 현황을 보여줍니다.")
st.markdown("📊 실시간 자료 기반 - 환경부 에어코리아 (10분 간격 갱신)")

# ✅ 시/도 선택
sido = st.selectbox("📍 시/도 선택", sido_list)

# ✅ 데이터 로딩
data = get_air_quality_data(sido)

if not data.empty:
    # 숫자형 변환
    data["pm10Value"] = pd.to_numeric(data["pm10Value"], errors='coerce')
    data["pm25Value"] = pd.to_numeric(data["pm25Value"], errors='coerce')

    # 등급 이모지 계산
    data["미세먼지등급"] = data["pm10Value"].apply(lambda x: get_grade_emoji(x, is_pm25=False))
    data["초미세먼지등급"] = data["pm25Value"].apply(lambda x: get_grade_emoji(x, is_pm25=True))

    # 시각 표시
    st.markdown(f"🕒 데이터 기준 시간: `{data.iloc[0]['dataTime']}`")

    # ✅ 테이블 표시
    st.subheader("📋 측정소별 미세먼지 현황")
    st.dataframe(
        data[["stationName", "pm10Value", "미세먼지등급", "pm25Value", "초미세먼지등급"]]
        .rename(columns={
            "stationName": "측정소",
            "pm10Value": "미세먼지(㎍/㎥)",
            "pm25Value": "초미세먼지(㎍/㎥)"
        }),
        use_container_width=True
    )

    # ✅ 차트 시각화
    st.subheader("📊 미세먼지(PM10) 수치 비교")
    st.bar_chart(data.set_index("stationName")["pm10Value"])

    st.subheader("📊 초미세먼지(PM2.5) 수치 비교")
    st.bar_chart(data.set_index("stationName")["pm25Value"])

else:
    st.error("🚨 데이터를 불러오지 못했습니다. API 키 또는 지역명을 확인해주세요.")
