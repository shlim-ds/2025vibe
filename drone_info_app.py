import streamlit as st

st.set_page_config(page_title="드론 예산별 구매 가이드", layout="wide")
st.title("🛩️ 드론 예산별 구매 추천 프로그램")

st.markdown("""
이 앱은 사용자의 **관심 분야**와 **예산**을 기반으로 적합한 드론을 추천해줍니다.
""")

# 드론 데이터셋
drone_db = [
    {
        "model": "DJI Mini 4K",
        "category": "입문/연습용",
        "desc": "초경량, 입문자용, 4K 촬영 지원",
        "price": 365000,
        "link": "https://store.dji.com/product/dji-mini-2-se"
    },
    {
        "model": "DJI Air 2S",
        "category": "촬영",
        "desc": "1인치 센서, 5.4K 촬영, 중급 이상",
        "price": 891000,
        "link": "https://store.dji.com/product/dji-air-2s"
    },
    {
        "model": "DJI Avata",
        "category": "FPV 비행",
        "desc": "FPV 전용 드론, 고글 연동, 입문자도 사용 가능",
        "price": 1450000,
        "link": "https://store.dji.com/product/dji-avata"
    },
    {
        "model": "DJI Agras T10",
        "category": "농업 방제",
        "desc": "10L 방제 드론, 농업 자동화에 적합",
        "price": 7000000,
        "link": "https://www.dji.com/kr/t10"
    },
    {
        "model": "DJI Mavic 3 Thermal",
        "category": "구조/재난",
        "desc": "열화상 감지 가능, 구조 및 감시용",
        "price": 6000000,
        "link": "https://www.dji.com/kr/mavic-3-enterprise"
    },
    {
        "model": "Xiaomi Mijia E88 Pro",
        "category": "입문/연습용",
        "desc": "가성비 FPV 입문 드론, HD 영상 가능",
        "price": 15000,
        "link": "https://www.aliexpress.com/item/1005005046354100.html"
    },
    {
        "model": "Zipline Drone",
        "category": "물류/배송",
        "desc": "고정익 기반 장거리 배송 드론, 계약 기반 운영",
        "price": 99999999,
        "link": "https://flyzipline.com"
    }
]

# 사용자 입력
st.header("🔍 구매 조건 입력")
budget = st.number_input("예산을 입력하세요 (₩ 단위)", min_value=10000, max_value=100000000, value=1000000, step=50000)
category = st.selectbox(
    "관심 있는 드론 활용 분야를 선택하세요:",
    sorted(set([d["category"] for d in drone_db]))
)

# 조건 필터링
filtered = [d for d in drone_db if d["category"] == category and d["price"] <= budget]

# 결과 출력
st.header("📦 추천 드론 결과")
if filtered:
    for drone in filtered:
        st.subheader(f"{drone['model']} — ₩{drone['price']:,}")
        st.write(drone["desc"])
        st.markdown(f"[🔗 구매 링크]({drone['link']})")
else:
    st.warning(f"❌ 예산 ₩{budget:,} 내에 '{category}' 분야에 적합한 드론이 없습니다. 예산을 높여보세요.")

# 부가 정보
with st.expander("💡 드론 구매 시 팁"):
    st.markdown("""
    - **항공법 확인 필수**: 250g 초과 시 등록 의무  
    - **비행시간, 영상화질, 조종 난이도**를 반드시 고려  
    - **자격증 필요 여부**도 확인하세요 (2kg 이상 대부분 필요)
    """)

st.success("🎉 예산 기반 드론 추천이 완료되었습니다!")

st.header("📚 기타 드론 정보 요약")

with st.expander("📜 드론의 역사"):
    st.markdown("""
    - 1900년대 초: 군용 무선조종 비행체 개발  
    - 1990년대: GPS 기반 군정찰기  
    - 2000년대 이후: 민간 촬영용 드론 대중화
    """)

with st.expander("🏭 제조사 비교"):
    st.markdown("""
    - DJI (중국): 전 세계 점유율 70% 이상  
    - Parrot, Autel, Skydio 등 다양한 기업 존재
    """)

with st.expander("✈️ 비행 원리"):
    st.markdown("""
    - 프로펠러 양력, 추력, 피치/롤/요 조절  
    - 센서 & GPS로 비행 안정성 유지
    """)

with st.expander("🚀 활용 분야"):
    st.markdown("""
    - 촬영, 농업, 배송, 구조, 건설, 군사용 등 다양한 분야
    """)

with st.expander("🕹️ 조종법 & 자격증"):
    st.markdown("""
    - 조종기: 왼쪽 스틱 (고도, 회전), 오른쪽 스틱 (이동)  
    - 한국 자격증: 1종~4종, 기체 중량에 따라 다름
    """)

st.success("💡 관심 분야 기반 추천이 완료되었습니다! 더 많은 기능이 필요하시면 말씀해 주세요.")
