import streamlit as st

st.set_page_config(page_title="브랜드별 드론 추천 프로그램", layout="wide")
st.title("🛩️ 브랜드별 드론 추천 프로그램")

st.markdown("""
이 앱은 다양한 드론 브랜드의 제품을 **가격**, **수준(입문/중급/전문가)**, **용도**에 따라 추천해줍니다.
또한 사용자의 **이해 수준**에 따라 적합한 드론을 자동으로 추천합니다.
""")

# -----------------------------
# 드론 데이터
# -----------------------------
drones = [
    # DJI 제품 추가
    {"brand": "DJI", "model": "Tello", "price": 99, "level": "입문자", "purpose": "연습", "desc": "실내용 미니 드론, 코딩 가능", "link": "https://store.dji.com/product/tello"},
    {"brand": "DJI", "model": "Mini 2 SE", "price": 339, "level": "중급자", "purpose": "촬영", "desc": "2.7K 동영상 촬영, 초경량", "link": "https://store.dji.com/product/dji-mini-2-se"},
    {"brand": "DJI", "model": "Mini 3 Pro", "price": 759, "level": "중급자", "purpose": "촬영", "desc": "4K HDR, 접이식 디자인, 초경량", "link": "https://store.dji.com/product/dji-mini-3-pro"},
    {"brand": "DJI", "model": "Air 2S", "price": 999, "level": "중급자", "purpose": "촬영", "desc": "1인치 센서, 5.4K 동영상, 중급자용 베스트셀러", "link": "https://store.dji.com/product/dji-air-2s"},
    {"brand": "DJI", "model": "Mavic 3 Pro", "price": 2199, "level": "전문가", "purpose": "촬영", "desc": "3개의 카메라, 고급 영상 제작용", "link": "https://store.dji.com/product/mavic-3-pro"},
    {"brand": "DJI", "model": "Mavic 3 Thermal", "price": 6000, "level": "전문가", "purpose": "구조/보안", "desc": "열화상 카메라 탑재, 수색 및 재난 대응용", "link": "https://www.dji.com/kr/mavic-3-enterprise"},
    {"brand": "DJI", "model": "Agras T10", "price": 7000, "level": "전문가", "purpose": "농업", "desc": "10L 탱크, 자동 방제, 농업용 드론", "link": "https://www.dji.com/kr/t10"},

    # 입문자용
    {"brand": "Holy Stone", "model": "HS110D", "price": 70, "level": "입문자", "purpose": "연습", "desc": "실내 연습용 드론, 저가형", "link": "https://www.holystone.com"},
    {"brand": "Hubsan", "model": "X4 H107D+", "price": 80, "level": "입문자", "purpose": "FPV 연습", "desc": "입문용 FPV 드론", "link": "https://www.hubsan.com"},

    # 중급자용
    {"brand": "Holy Stone", "model": "HS720E", "price": 280, "level": "중급자", "purpose": "촬영", "desc": "4K EIS 카메라, GPS", "link": "https://www.holystone.com"},
    {"brand": "Parrot", "model": "Anafi", "price": 699, "level": "중급자", "purpose": "촬영", "desc": "4K HDR, 180도 카메라", "link": "https://www.parrot.com"},
    {"brand": "Autel", "model": "EVO Nano+", "price": 799, "level": "중급자", "purpose": "촬영", "desc": "4K, 저조도 성능 우수", "link": "https://www.autelrobotics.com"},

    # 전문가용
    {"brand": "Autel", "model": "EVO II Pro", "price": 1500, "level": "전문가", "purpose": "촬영", "desc": "6K 카메라, 1인치 센서", "link": "https://www.autelrobotics.com"},
    {"brand": "Skydio", "model": "Skydio 2+", "price": 1500, "level": "전문가", "purpose": "자율비행", "desc": "AI 장애물 회피, 자율 비행", "link": "https://www.skydio.com"},
    {"brand": "Parrot", "model": "Anafi USA", "price": 7000, "level": "전문가", "purpose": "구조/보안", "desc": "열화상 + 줌 카메라", "link": "https://www.parrot.com"},
    {"brand": "Yuneec", "model": "H520", "price": 3000, "level": "전문가", "purpose": "산업", "desc": "측량, 구조용 드론", "link": "https://www.yuneec.com"},
    {"brand": "Yuneec", "model": "Typhoon H Plus", "price": 1800, "level": "전문가", "purpose": "촬영", "desc": "6개 로터, 1인치 센서", "link": "https://www.yuneec.com"},
]

# -----------------------------
# 사용자 입력 (한글 UI + 이해 수준별 추천)
# -----------------------------
st.header("🔍 사용자 조건에 따른 드론 추천")

understanding = st.radio("드론에 대한 이해 수준을 선택하세요:", ["입문자", "중급자", "전문가"])

if understanding == "입문자":
    default_levels = ["입문자"]
    default_budget = (50, 400)
elif understanding == "중급자":
    default_levels = ["중급자"]
    default_budget = (400, 1200)
else:
    default_levels = ["전문가"]
    default_budget = (1200, 10000)

budget = st.slider("예산 범위 (USD)", 50, 10000, default_budget)
levels = st.multiselect("추천 받을 수준 (중복 선택 가능)", ["입문자", "중급자", "전문가"], default=default_levels)
brands = st.multiselect("브랜드 선택", sorted(set(d["brand"] for d in drones)), default=sorted(set(d["brand"] for d in drones)))
purposes = st.multiselect("용도 선택", sorted(set(d["purpose"] for d in drones)), default=sorted(set(d["purpose"] for d in drones)))

# -----------------------------
# 필터링 및 출력
# -----------------------------
st.header("📦 추천 드론 결과")
filtered = [
    d for d in drones
    if budget[0] <= d["price"] <= budget[1]
    and d["level"] in levels
    and d["brand"] in brands
    and d["purpose"] in purposes
]

if filtered:
    for d in filtered:
        st.subheader(f"{d['model']} — ${d['price']}")
        st.write(f"브랜드: {d['brand']} | 수준: {d['level']} | 용도: {d['purpose']}")
        st.write(f"📝 {d['desc']}")
        st.markdown(f"[🔗 공식 링크]({d['link']})")
        st.markdown("---")
else:
    st.warning("조건에 맞는 드론이 없습니다. 예산이나 필터를 조정해보세요.")

# -----------------------------
# 브랜드 링크 요약
# -----------------------------
with st.expander("🔗 브랜드 공식 사이트 모음"):
    st.markdown("""
    - [Parrot](https://www.parrot.com)  
    - [Autel Robotics](https://www.autelrobotics.com)  
    - [Skydio](https://www.skydio.com)  
    - [Holy Stone](https://www.holystone.com)  
    - [Hubsan](https://www.hubsan.com)  
    - [Yuneec](https://www.yuneec.com)  
    - [DJI](https://www.dji.com)
    """)
