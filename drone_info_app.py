import streamlit as st

st.set_page_config(page_title="드론 추천 + 구조/농업 통합 안내", layout="wide")
st.title("🛩️ 드론 추천 + 구조/농업 활용 통합 프로그램")

st.markdown("사용자의 **예산**, **이해 수준**, **활용 분야**에 따라 적절한 드론을 추천하고, **농업 방제 및 구조 구난 드론 종류**도 안내합니다.")

# -------------------------------
# 사용자 입력
# -------------------------------
st.header("🔍 드론 추천 조건 설정")

level = st.radio("📘 드론 이해 수준", ["입문자", "중급자", "전문가"])
budget = st.number_input("💰 예산 입력 (₩)", min_value=10000, max_value=100000000, value=1000000, step=50000)
category = st.selectbox("📌 관심 분야 선택", ["입문/연습용", "촬영", "FPV 비행", "농업 방제", "구조/재난", "물류/배송"])

# -------------------------------
# 드론 데이터
# -------------------------------
drone_db = [
    {"model": "DJI Mini 4K", "category": "입문/연습용", "desc": "초경량, 입문자용, 4K 촬영", "price": 365000, "level": "입문자", "link": "https://store.dji.com/product/dji-mini-2-se"},
    {"model": "Xiaomi E88 Pro", "category": "입문/연습용", "desc": "가성비 연습용 드론", "price": 15000, "level": "입문자", "link": "https://www.aliexpress.com/item/1005005046354100.html"},
    {"model": "DJI Air 2S", "category": "촬영", "desc": "1인치 센서, 5.4K 영상 촬영", "price": 891000, "level": "중급자", "link": "https://store.dji.com/product/dji-air-2s"},
    {"model": "DJI Avata", "category": "FPV 비행", "desc": "FPV 전용 고속 드론", "price": 1450000, "level": "중급자", "link": "https://store.dji.com/product/dji-avata"},
    {"model": "DJI Agras T10", "category": "농업 방제", "desc": "10L 탱크, 자동 방제 경로", "price": 7000000, "level": "전문가", "link": "https://www.dji.com/kr/t10"},
    {"model": "DJI Agras T40", "category": "농업 방제", "desc": "대면적용 40L 방제 드론", "price": 18000000, "level": "전문가", "link": "https://www.dji.com/kr/t40"},
    {"model": "DJI Mavic 3 Thermal", "category": "구조/재난", "desc": "열화상 + 줌 카메라 탑재", "price": 6000000, "level": "전문가", "link": "https://www.dji.com/kr/mavic-3-enterprise"},
    {"model": "DJI Matrice 30", "category": "구조/재난", "desc": "다중 센서 + RTK + 우천비행 가능", "price": 17000000, "level": "전문가", "link": "https://www.dji.com/kr/matrice-30"},
    {"model": "Zipline Drone", "category": "물류/배송", "desc": "고정익 기반, 장거리 배송", "price": 99999999, "level": "전문가", "link": "https://flyzipline.com"},
]

# -------------------------------
# 필터링
# -------------------------------
filtered = [
    d for d in drone_db
    if d["category"] == category and d["price"] <= budget and (
        level == "입문자" and d["level"] == "입문자" or
        level == "중급자" and d["level"] in ["입문자", "중급자"] or
        level == "전문가"
    )
]

# -------------------------------
# 추천 결과
# -------------------------------
st.header("📦 추천 드론 결과")

if filtered:
    for d in filtered:
        st.subheader(f"{d['model']} — ₩{d['price']:,}")
        st.write(f"**설명:** {d['desc']}")
        st.markdown(f"[🔗 구매 링크]({d['link']})")
        st.markdown("---")
else:
    st.warning("해당 조건에 맞는 드론이 없습니다. 예산이나 수준을 조정해보세요.")

# -------------------------------
# 농업 방제 및 구조 구난 드론 소개
# -------------------------------
st.header("🌾🚨 농업 방제 및 구조 구난 드론 정보")

with st.expander("🌾 농업 방제용 드론 종류"):
    st.markdown("""
    ### ✅ DJI Agras 시리즈
    - **T10 / T20 / T40**: 10~40L 대용량 탱크  
    - 자동 경로 비행, 장애물 감지, RTK GPS 지원  
    - [🔗 Agras T10 상세보기](https://www.dji.com/kr/t10) / [🔗 Agras T40](https://www.dji.com/kr/t40)

    ### ✅ 국내 농업 특화 기종
    - 헬셀 M 시리즈, 퍼스텍, 포유드론 등  
    - 농협 연계, 국산 기술 기반 A/S  
    """)

with st.expander("🚨 구조/구난용 드론 종류"):
    st.markdown("""
    ### ✅ DJI Mavic 3 Thermal
    - 열화상 + 줌 카메라 탑재  
    - 실종자 수색, 화재 감시 등  
    - [🔗 제품 링크](https://www.dji.com/kr/mavic-3-enterprise)

    ### ✅ DJI Matrice 30 / 300 RTK
    - 다중 센서 (열화상 + 거리측정 + RGB)  
    - 우천/야간/도심 비행 가능  
    - [🔗 Matrice 30 링크](https://www.dji.com/kr/matrice-30)

    ### ✅ Zipline 고정익 드론
    - 혈액, 백신 긴급 배송  
    - 고속 장거리 비행  
    - [🔗 Zipline 링크](https://flyzipline.com)
    """)

# -------------------------------
# 비행 원리
# -------------------------------
st.header("✈️ 드론 비행 원리 (Pitch, Roll, Yaw)")

st.markdown("""
**Pitch**, **Roll**, **Yaw**는 드론의 회전 운동을 설명하는 핵심 용어입니다.

| 용어 | 축 | 회전 방향 | 설명 |
|------|----|-------------|------|
| **Pitch (피치)** | Y축 | 앞뒤 기울기 | 앞뒤 방향으로 기울어지는 회전 |
| **Roll (롤)** | X축 | 좌우 기울기 | 좌우로 기울어지는 회전 |
| **Yaw (요우)** | Z축 | 중심축 회전 | 기체 중심축을 기준으로 좌우 회전 |

➡️ 이 회전들을 조합하여 드론은 상하좌우 이동, 회전 비행이 가능합니다.
""")

# -------------------------------
# 유의사항
# -------------------------------
with st.expander("📋 드론 관련 규제 안내"):
    st.markdown("""
    - 250g 초과: **기체 등록 필수**  
    - 2kg 초과: **조종자 자격증 필요**  
    - 야간·도심·비가시권 비행: **사전 허가 필요**
    """)

st.success("✅ 모든 추천과 정보 안내가 완료되었습니다. 더 많은 정보가 필요하면 말씀해주세요.")
