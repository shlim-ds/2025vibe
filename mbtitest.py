import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MBTI 테스트", layout="centered")
st.title("🧠 정밀 MBTI 테스트 (랜덤 출제 + 저장 기능)")

# 질문 데이터 정의
questions = {
    "EI": [
        ("새로운 사람을 만나는 것이 즐겁다", "E", "I"),
        ("여럿이 어울리는 모임에서 에너지를 얻는다", "E", "I"),
        ("혼자 있는 시간이 필요하다", "I", "E"),
        ("사람들과 함께 있으면 기분이 좋아진다", "E", "I"),
        ("파티보다는 조용한 시간을 선호한다", "I", "E")
    ],
    "SN": [
        ("사실과 데이터를 중요하게 여긴다", "S", "N"),
        ("추상적인 아이디어보다 실용적인 것이 좋다", "S", "N"),
        ("상상과 영감이 중요하다고 생각한다", "N", "S"),
        ("직관보다는 경험을 신뢰한다", "S", "N"),
        ("세부사항보다는 전체 흐름에 집중한다", "N", "S")
    ],
    "TF": [
        ("의사결정 시 논리를 우선시한다", "T", "F"),
        ("사람들의 감정을 고려해 결정을 내린다", "F", "T"),
        ("비판적 사고를 중시한다", "T", "F"),
        ("공감 능력이 뛰어나다는 말을 듣는다", "F", "T"),
        ("객관적인 기준으로 판단한다", "T", "F")
    ],
    "JP": [
        ("계획적으로 일정을 관리한다", "J", "P"),
        ("유연한 일정과 즉흥적인 계획을 선호한다", "P", "J"),
        ("체계적으로 일 처리를 한다", "J", "P"),
        ("즉흥적인 상황에서 잘 대처한다", "P", "J"),
        ("일을 하기 전 미리 정리한다", "J", "P")
    ]
}

# 랜덤하게 각 차원에서 3문항 선택
selected_questions = {}
for key, qlist in questions.items():
    selected_questions[key] = random.sample(qlist, 3)

# 점수 기록
scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

# 질문 표시
st.markdown("---")
st.subheader("📝 질문에 답해주세요:")
for dim, qlist in selected_questions.items():
    for idx, (q, a1, a2) in enumerate(qlist):
        choice = st.radio(f"{q}", [a1, a2], key=f"{dim}-{idx}")
        scores[choice] += 1

# MBTI 유형 결정
def determine_mbti(scores):
    result = ""
    result += "E" if scores["E"] >= scores["I"] else "I"
    result += "S" if scores["S"] >= scores["N"] else "N"
    result += "T" if scores["T"] >= scores["F"] else "F"
    result += "J" if scores["J"] >= scores["P"] else "P"
    return result

# 설명 사전
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

# 결과 버튼
if st.button("🔍 MBTI 결과 확인"):
    mbti_type = determine_mbti(scores)
    st.success(f"당신의 MBTI는 **{mbti_type}** 입니다!")
    st.markdown(f"**{mbti_desc.get(mbti_type, '설명이 준비 중입니다.')}**")

    # 결과 저장
    result = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "MBTI": mbti_type,
        **scores
    }
    df = pd.DataFrame([result])
    try:
        df.to_csv("mbti_results.csv", mode='a', index=False, header=False)
        st.info("✅ 결과가 `mbti_results.csv` 파일에 저장되었습니다.")
    except:
        st.warning("⚠️ 결과 저장에 실패했습니다. 로컬 권한을 확인하세요.")

    # 다시하기
    st.markdown("---")
    st.markdown("🔁 테스트를 다시 하고 싶다면 앱을 새로고침 해주세요 (F5 또는 ⟳ 버튼).")

