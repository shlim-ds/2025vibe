import streamlit as st

st.title("🌟 MBTI 성격 유형 테스트")
st.markdown("당신의 성격 유형을 간단한 질문 4개로 알아봅시다!")

# 질문 1: E / I
ei = st.radio(
    "Q1. 사람들과 어울릴 때 에너지가 생기시나요?",
    ("E - 네, 사람들과 있을 때 더 에너지가 생겨요",
     "I - 아니요, 혼자 있을 때 더 편하고 에너지가 생겨요")
)

# 질문 2: S / N
sn = st.radio(
    "Q2. 정보를 받아들일 때 어떤 것을 더 신뢰하시나요?",
    ("S - 구체적이고 현실적인 사실",
     "N - 직관과 가능성, 아이디어")
)

# 질문 3: T / F
tf = st.radio(
    "Q3. 결정을 내릴 때 어떤 것이 더 중요하다고 느끼시나요?",
    ("T - 논리와 객관적인 분석",
     "F - 감정과 사람에 대한 공감")
)

# 질문 4: J / P
jp = st.radio(
    "Q4. 일정을 계획할 때 어떤 스타일이신가요?",
    ("J - 계획적으로 체계적으로 정리하는 편이에요",
     "P - 즉흥적으로 유연하게 처리하는 편이에요")
)

# 결과 버튼
if st.button("🔍 내 MBTI 유형 확인하기"):
    mbti = ""
    mbti += "E" if ei.startswith("E") else "I"
    mbti += "S" if sn.startswith("S") else "N"
    mbti += "T" if tf.startswith("T") else "F"
    mbti += "J" if jp.startswith("J") else "P"

    st.subheader(f"🎯 당신의 MBTI는: **{mbti}**")

    mbti_desc = {
        "ISTJ": "신중하고 책임감 있는 관리자",
        "ISFJ": "조용하고 성실한 보호자",
        "INFJ": "통찰력 있는 조용한 이상주의자",
        "INTJ": "독립적이고 전략적인 사색가",
        "ISTP": "논리적이고 실용적인 탐험가",
        "ISFP": "조용하고 친절한 예술가",
        "INFP": "이상적이고 충성스러운 중재자",
        "INTP": "지적이고 창의적인 사색가",
        "ESTP": "활동적이고 에너지 넘치는 해결사",
        "ESFP": "사교적이고 자유로운 연예인",
        "ENFP": "열정적이고 창의적인 활동가",
        "ENTP": "논쟁을 즐기는 발명가",
        "ESTJ": "체계적이고 실용적인 관리자",
        "ESFJ": "다정하고 헌신적인 조력자",
        "ENFJ": "이타적이고 카리스마 있는 리더",
        "ENTJ": "단호하고 목표지향적인 지휘관"
    }

    description = mbti_desc.get(mbti, "설명을 준비 중입니다.")
    st.write(description)
