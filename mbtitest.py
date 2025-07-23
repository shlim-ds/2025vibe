import streamlit as st
import matplotlib
matplotlib.use('Agg')  # Streamlit에서 백엔드 설정
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import os

st.set_page_config(page_title="MBTI 진로/진학 추천", layout="wide")
st.title("🧠 MBTI 기반 진로/진학 분석 프로그램")

# MBTI 차원 정의
dimensions = ["E", "I", "S", "N", "T", "F", "J", "P"]
scores = {dim: 0 for dim in dimensions}

# 차원별 질문
questions = {
    "E": [
        "사람들과 어울릴 때 에너지가 생긴다",
        "여럿이 어울리는 활동을 선호한다",
        "새로운 사람을 만나는 것이 즐겁다",
        "즉흥적인 대화를 잘 한다",
        "자기소개를 편하게 한다",
        "모임을 주도하는 편이다",
        "다양한 활동에 자주 참여한다"
    ],
    "I": [
        "혼자 있는 시간이 필요하다",
        "조용한 환경이 더 편하다",
        "생각을 정리한 후 말한다",
        "감정보다 관찰에 집중한다",
        "자신만의 공간이 중요하다",
        "혼자서 문제 해결을 선호한다",
        "사교적인 자리는 피로하다"
    ],
    "S": [
        "현실적이고 실용적인 것을 좋아한다",
        "지금 상황에 집중하는 편이다",
        "사실과 데이터를 중시한다",
        "경험에서 배우는 걸 선호한다",
        "세부사항을 잘 기억한다",
        "명확하고 구체적인 설명이 좋다",
        "신중한 선택을 한다"
    ],
    "N": [
        "상상하고 창조하는 것을 좋아한다",
        "미래의 가능성에 자주 생각이 머문다",
        "은유적 표현을 즐긴다",
        "직관에 따라 결정을 내린다",
        "새로운 이론이나 개념을 즐긴다",
        "전체 흐름을 빠르게 파악한다",
        "변화에 열려있다"
    ],
    "T": [
        "논리와 분석이 중요하다",
        "문제를 해결할 때 감정보다 사실을 본다",
        "비판적으로 사고하는 편이다",
        "객관적으로 판단하려 한다",
        "효율을 우선시한다",
        "감정보다는 원칙이 우선이다",
        "논쟁을 피하지 않는다"
    ],
    "F": [
        "다른 사람의 감정을 잘 이해한다",
        "공감하는 대화가 중요하다",
        "상대의 입장에서 생각한다",
        "사람 사이의 조화를 중시한다",
        "정의보다 배려가 더 중요하다",
        "상대의 기분을 해치지 않으려 노력한다",
        "불편한 말을 피하는 편이다"
    ],
    "J": [
        "계획적으로 행동하는 편이다",
        "마감 기한을 잘 지킨다",
        "할 일을 미리 준비한다",
        "일정표를 만드는 걸 좋아한다",
        "혼란스러운 상황이 싫다",
        "체계적인 환경이 좋다",
        "불확실한 상황에 불편함을 느낀다"
    ],
    "P": [
        "즉흥적인 결정을 잘 한다",
        "상황에 따라 유연하게 대처한다",
        "새로운 일정을 반기는 편이다",
        "기한이 가까워야 집중이 된다",
        "변화에 강하다",
        "계획보다는 흐름에 맡긴다",
        "자유로운 스타일이 좋다"
    ]
}

# 질문 출력
st.subheader("📝 56문항 성격 유형 질문")
for dim in dimensions:
    st.markdown(f"#### {'외향' if dim == 'E' else '내향' if dim == 'I' else dim}")
    for i, q in enumerate(questions[dim]):
        ans = st.radio(q, ["그렇다", "아니다"], key=f"{dim}_{i}")
        if ans == "그렇다":
            scores[dim] += 1

# 결과 분석
if st.button("🔍 결과 분석 및 추천 보기"):
    mbti = (
        "E" if scores["E"] >= scores["I"] else "I"
    ) + (
        "S" if scores["S"] >= scores["N"] else "N"
    ) + (
        "T" if scores["T"] >= scores["F"] else "F"
    ) + (
        "J" if scores["J"] >= scores["P"] else "P"
    )

    st.subheader(f"🎯 당신의 MBTI 유형은: {mbti}")

    # MBTI 결과 정보
    mbti_data = {
        "ENTP": {
            "설명": "도전적이고 창의적인 발명가형",
            "진로": ["창업가", "마케터", "전략가"],
            "전공": ["경영학", "경제학", "창업학"]
        },
        "ISFJ": {
            "설명": "성실하고 온화한 조력자형",
            "진로": ["간호사", "사회복지사", "초등교사"],
            "전공": ["간호학", "사회복지학", "교육학"]
        },
        # 모든 유형 추가 가능...
    }

    info = mbti_data.get(mbti, None)
    if info:
        st.markdown(f"**설명:** {info['설명']}")
        st.markdown("**💼 추천 진로:** " + ", ".join(info["진로"]))
        st.markdown("**🎓 추천 전공:** " + ", ".join(info["전공"]))
    else:
        st.warning("MBTI 데이터가 아직 등록되지 않았습니다.")

    # 성향 그래프 시각화
    dim_pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    labels = ["E-I", "S-N", "T-F", "J-P"]
    values = [scores[p1] - scores[p2] for p1, p2 in dim_pairs]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color='cornflowerblue')
    ax.axhline(0, color='black')
    ax.set_ylabel("성향 점수 차")
    ax.set_title("MBTI 성향 그래프")
    st.pyplot(fig)

    # 저장
    result = {
        "MBTI": mbti,
        **scores
    }
    df = pd.DataFrame([result])
    if not os.path.exists("mbti_results.csv"):
        df.to_csv("mbti_results.csv", index=False)
    else:
        df.to_csv("mbti_results.csv", mode='a', header=False, index=False)
    st.success("✅ 결과가 저장되었습니다 (mbti_results.csv)")
