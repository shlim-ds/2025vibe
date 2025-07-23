import streamlit as st

st.set_page_config(page_title="드론 종합 소개 & 추천 시스템", layout="wide")
st.title("🛩️ 드론 종합 소개 + 관심 분야별 추천 시스템")

st.markdown("📚 드론의 역사, 제조사, 비행 원리부터 🎥 영상, 🛒 구매 추천까지 모두 확인할 수 있습니다.")

# --- 드론 관심 분야별 추천 ---
st.header("🤖 관심 분야에 따른 드론 추천")

# 사용자 선택 입력
selected_use = st.selectbox(
    "관심 있는 드론 활용 분야를 선택하세요:",
    ["촬영", "FPV 비행", "농업 방제", "구조/재난", "물류/배송", "입문/연습용"]
)

# 추천 드론 딕셔너리
drone_recommendations = {
    "촬영": {
        "model": "DJI Air 2S",
        "desc": "1인치 센서 탑재, 5.4K 촬영 지원, 전문가용 촬영 드론",
        "price": "₩891,000",
        "link": "https://store.dji.com/product/dji-air-2s"
    },
    "FPV 비행": {
        "model": "DJI Avata",
        "desc": "FPV 촬영에 특화된 컴팩트 드론, 고글 연동, 초보자도 쉽게 사용 가능",
        "price": "₩1,450,000",
        "link": "https://store.dji.com/product/dji-avata"
    },
    "농업 방제": {
        "model": "DJI Agras T10",
        "desc": "10L 탱크 보유, 자동 방제 루트 지원, 농업 전문 드론",
        "price": "₩7,000,000 이상",
        "link": "https://www.dji.com/kr/t10"
    },
    "구조/재난": {
        "model": "DJI Mavic 3 Thermal",
        "desc": "열화상 카메라 탑재, 구조·감시용 드론, 자동 비행 지원",
        "price": "₩6,000,000 이상",
        "link": "https://www.dji.com/kr/mavic-3-enterprise"
    },
    "물류/배송": {
        "model": "Zipline Fixed-Wing Drone",
        "desc": "아프리카 등에서 의료 배송에 사용되는 고정익 드론 (특수 목적용)",
        "price": "비공개 / 계약 기반",
        "link": "https://flyzipline.com"
    },
    "입문/연습용": {
        "model": "DJI Mini 4K",
        "desc": "249g 이하 초경량, 조종 연습·입문자용으로 적합, 4K 지원",
        "price": "₩365,000",
        "link": "https://store.dji.com/product/dji-mini-2-se"
    },
}

# 결과 출력
selected = drone_recommendations[selected_use]
st.subheader(f"🎯 {selected_use} 추천 드론: {selected['model']}")
st.write(f"**설명**: {selected['desc']}")
st.write(f"**가격**: {selected['price']}")
st.markdown(f"[🔗 구매/상세 보기]({selected['link']})")

# --- 영상 포함 소개 섹션 ---
st.header("📺 드론 영상 가이드")
st.video("https://www.youtube.com/watch?v=y_99afiNYnk")
st.video("https://www.youtube.com/watch?v=SpuXqNakP2A")
st.video("https://www.youtube.com/watch?v=MFO9V11KcI0")
st.video("https://www.youtube.com/watch?v=3r3b-S910jc")

# --- 기타 정보 요약 ---
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
