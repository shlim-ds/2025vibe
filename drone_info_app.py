import streamlit as st

st.set_page_config(page_title="드론 추천 통합 프로그램", layout="wide")
st.title("🛩️ 드론 예산/수준 기반 추천 + 비행 원리 안내")

# -----------------------------
# 사용자 수준 선택
# -----------------------------
st.header("👤 사용자 이해 수준을 선택하세요")

level = st.radio("드론에 대해 어느 정도 알고 계신가요?", ["입문자", "중급자", "전문가"])

# -----------------------------
# 예산 & 분야 입력
# -----------------------------
st.header("🔍 구매 조건 입력")

budget = st.number_input("💰 예산 입력 (₩)", min_value=10000, max_value=100000000, value=1000000, step=50000)
category = st.selectbox("📌 드론 활용 분야 선택", ["입문/연습용", "촬영", "FPV 비행", "농업 방제", "구조/재난", "물류/배송"])

# -----------------------------
# 드론 데이터셋
# -----------------------------
drone_db = [
    {"model": "DJI Mini 4K", "category": "입문/연습용", "desc": "초경량, 입문자용, 4K 촬영", "price": 365000, "level": "입문자", "link": "https://store.dji.com/product/dji-mini-2-se"},
    {"model": "Xiaomi E88 Pro", "category": "입문/연습용", "desc": "가성비 연습용, HD 영상", "price": 15000, "level": "입문자", "link": "https://www.aliexpress.com/item/1005005046354100.html"},
    {"model": "DJI Air 2S", "category": "촬영", "desc": "1인치 센서, 중급 이상 영상 촬영", "price": 891000, "level": "중급자", "link": "https://store.dji.com/product/dji-air-2s"},
    {"model": "DJI Avata", "category": "FPV 비행", "desc": "FPV 전용, 고속 비행, 고글 연동", "price": 1450000, "level": "중급자", "link": "https://store.dji.com/product/dji-avata"},
    {"model": "DJI Agras T10", "category": "농업 방제", "desc": "10L 방제, 산업용 농업 드론", "price": 7000000, "level": "전문가", "link": "https://www.dji.com/kr/t10"},
    {"model": "DJI Mavic 3 Thermal", "category": "구조/재난", "desc": "열화상 센서, 구조 감시용", "price": 6000000, "level": "전문가", "link": "https://www.dji.com/kr/mavic-3-enterprise"},
    {"model": "Zipline Drone", "category": "물류/배송", "desc": "고정익 기반 장거리 배송 드론", "price": 99999999, "level": "전문가", "link": "https://flyzipline.com"},
]

# -----------------------------
# 필터링 로직
# -----------------------------
filtered = [
    d for d in drone_db
    if d["category"] == category and d["price"] <= budget and (
        level == "입문자" and d["level"] in ["입문자"] or
        level == "중급자" and d["level"] in ["입문자", "중급자"] or
        level == "전문가"
    )
]

# -----------------------------
# 추천 결과
# -----------------------------
st.header("📦 추천 드론 결과")
if filtered:
    for d in filtered:
        st.subheader(f"{d['model']} — ₩{d['price']:,}")
        st.write(d["desc"])
        st.markdown(f"[🔗 구매 링크]({d['link']})")
        st.markdown("---")
else:
    st.warning("조건에 맞는 드론이 없습니다. 예산을 늘리거나 다른 수준 또는 분야를 선택해보세요.")

# -----------------------------
# 드론 종류 소개
# -----------------------------
st.header("📚 드론의 종류")

with st.expander("🌀 쿼드콥터 (Quadcopter)"):
    st.markdown("""
    - 4개의 수직 프로펠러 사용  
    - 정지비행 가능, 조종 쉬움  
    - 촬영·입문·연습용에 많이 사용
    """)

with st.expander("🛫 고정익 드론"):
    st.markdown("""
    - 날개 형태, 비행기와 유사  
    - 장거리 고속비행에 적합  
    - 배송, 측량 등에 사용
    """)

with st.expander("🧬 하이브리드 드론"):
    st.markdown("""
    - 수직 이착륙 + 장거리 비행  
    - 고정익 + 회전익 혼합형  
    - 고급 산업용에서 사용
    """)

# -----------------------------
# 비행 원리 설명
# -----------------------------
st.header("✈️ 드론 비행 원리")

if level == "입문자":
    st.markdown("""
    드론은 공중에서 **떠오르고**, **앞으로 가고**, **회전**합니다.  
    이건 모두 **프로펠러의 속도 조절**로 이루어져요.
    """)
elif level == "중급자":
    st.markdown("""
    드론은 다음과 같은 힘과 회전 조합으로 비행합니다:

    - **Lift** (양력): 위로 뜨는 힘  
    - **Thrust** (추력): 앞으로 나아가는 힘  
    - **Pitch**: 앞뒤 기울기 조절  
    - **Roll**: 좌우 기울기 조절  
    - **Yaw**: 좌우 회전 조절
    """)
else:
    st.markdown("""
    전문가용 설명:

    - 드론은 **쿼드콥터 구조**로 PID 기반 실시간 자세 제어  
    - **Pitch/Roll/Yaw**는 각 축 회전에 따른 운동  
    - IMU + GPS 센서를 기반으로 한 비행 컨트롤러가 중심
    """)

# -----------------------------
# 시각 자료
# -----------------------------
st.header("🖼️ 드론 비행 동작 이미지")
st.markdown("""
<img src="https://upload.wikimedia.org/wikipedia/commons/1/1e/Quadcopter_flight_dynamics.svg" width="700">
<p style="text-align:center;"><i>쿼드콥터의 Pitch / Roll / Yaw 개념도</i></p>
""", unsafe_allow_html=True)

# -----------------------------
# 부가 정보
# -----------------------------
with st.expander("📋 드론 구매/비행 시 유의사항"):
    st.markdown("""
    - 250g 초과 → **기체 등록 필수**  
    - 2kg 초과 → **조종자 자격증 필요**  
    - 야간·도심·비가시권 비행 시 허가 필요
    """)

st.success("✅ 추천 및 안내가 완료되었습니다! 더 알고 싶으신 기능이 있다면 요청해주세요.")
