import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="정밀 MBTI 테스트", layout="centered")
st.title("🧠 정밀 MBTI 테스트 (28문항)")
st.markdown("당신의 성격을 28개의 세밀한 질문으로 분석해드립니다.")

# 질문 데이터 정의 (각 차원 7개씩)
questions = {
    "EI": [
        ("사람들과 이야기할 때 에너지가 생긴다", "E", "I"),
        ("파티나 모임을 자주 참석하는 편이다", "E", "I"),
        ("말하기보다는 듣는 것이 편하다", "I", "E"),
        ("혼자 있는 시간이 꼭 필요하다", "I", "E"),
        ("즉흥적인 대화에 능숙하다", "E", "I"),
        ("많은 사람보다 소수의 깊은 관계를 선호한다", "I", "E"),
        ("모르는 사람과도 금방 친해질 수 있다", "E", "I")
    ],
    "SN": [
        ("구체적인 설명을 더 선호한다", "S", "N"),
        ("세부적인 정보를 놓치지 않으려 노력한다", "S", "N"),
        ("미래의 가능성을 자주 상상한다", "N", "S"),
        ("지금 현실보다 '무엇이 될 수 있는가'를 생각한다", "N", "S"),
        ("새로운 개념을 배우는 것이 즐겁다", "N", "S"),
        ("감각적으로 체험한 것을 더 신뢰한다", "S", "N"),
        ("사실보다 해석에 더 집중한다", "N", "S")
    ],
    "TF": [
        ("의사결정은 감정보다 논리가 우선이다", "T", "F"),
        ("사람의 입장을 먼저 생각하는 편이다", "F", "T"),
        ("비판적 사고가 중요하다고 생각한다", "T", "F"),
        ("다른 사람의 감정을 쉽게 공감한다", "F", "T"),
        ("정의보다는 배려가 더 중요하다", "F", "T"),
        ("갈등 상황에서도 감정보다는 원칙을 중시한다", "T", "F"),
        ("사람을 실망시키는 것이 싫다", "F", "T")
    ],
    "JP": [
        ("계획표를 짜는 것을 좋아한다", "J", "P"),
        ("마감 전에 일을 끝내는 편이다", "J", "P"),
        ("갑작스러운 변화를 즐기는 편이다", "P", "J"),
        ("계획이 틀어지면 스트레스를 받는다", "J", "P"),
        ("일정을 유동적으로 움직이는 게 편하다", "P", "J"),
        ("해야 할 일을 미리 준비한다", "J", "P"),
        ("계획보다 즉흥적인 선택이 더 잘 맞는다", "P", "J")
    ]
}

# 초기 점수 세팅
scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

st.markdown("---")
st.subheader("📝 28문항에 답해주세요:")

# 질문 순서대로 출력
for dimension, q_list in questions.items():
    st.markdown(f"### {dimension} 유형 질문")
    for idx, (q, opt1, opt2) in enumerate(q_list):
        choice = st.radio(f"{q}", [opt1, opt2], key=f"{dimension}-{idx}")
        scores[choice] += 1

# MBTI 결정 함수
def get_mbti(scores):
    return (
        "E" if scores["E"] >= scores["I"] else "I"
    ) + (
        "S" if scores["S"] >= scores["N"] else "N"
    ) + (
        "T" if scores["T"] >= scores["F"] else "F"
    ) + (
        "J" if scores["J"] >= scores["P"] else "P"
    )

# MBTI 설명
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

# 결과 출력
if st.button("🔍 결과 보기"):
    mbti_result = get_mbti(scores)
    st.success(f"✅ 당신의 MBTI는 **{mbti_result}** 입니다!")
    st.write(f"**{mbti_desc.get(mbti_result, '설명이 준비 중입니다.')}**")

    # 결과 저장
    result = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "MBTI": mbti_result,
        **scores
    }
    df = pd.DataFrame([result])
    try:
        df.to_csv("mbti_results_full.csv", mode='a', index=False, header=not pd.io.common.file_exists("mbti_results_full.csv"))
        st.info("📝 결과가 'mbti_results_full.csv' 파일에 저장되었습니다.")
    except:
        st.warning("⚠️ 결과 저장 실패 - 로컬 파일 권한을 확인해주세요.")

    st.markdown("---")
    st.markdown("🔁 **테스트를 다시 하고 싶다면 페이지를 새로고침해주세요.**")

