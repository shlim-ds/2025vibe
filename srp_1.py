import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", page_icon="🎮")

st.title("🎮 가위바위보 게임 (이모지 버전)")
st.write("총 3판 진행! 이기면 +1점, 지면 -1점이에요.")

# 초기값 설정
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.round = 1

# 선택지 및 이모지 매핑
choices = ["가위", "바위", "보"]
emoji_map = {
    "가위": "✌️",
    "바위": "✊",
    "보": "✋"
}

def get_result(user, comp):
    if user == comp:
        return 0, "🤝 무승부!"
    elif (user == "가위" and comp == "보") or \
         (user == "바위" and comp == "가위") or \
         (user == "보" and comp == "바위"):
        return 1, "🎉 승리!"
    else:
        return -1, "😢 패배..."

# 게임 화면
if st.session_state.round <= 3:
    st.subheader(f"🕹️ {st.session_state.round}번째 판")
    user_choice = st.radio("선택하세요:", choices, index=0, format_func=lambda x: f"{emoji_map[x]} {x}")

    if st.button("결정!"):
        comp_choice = random.choice(choices)

        st.markdown(f"#### 🙋‍♂️ 당신의 선택: {emoji_map[user_choice]} **{user_choice}**")
        st.markdown(f"#### 🤖 컴퓨터의 선택: {emoji_map[comp_choice]} **{comp_choice}**")

        point, message = get_result(user_choice, comp_choice)
        st.session_state.score += point
        st.session_state.round += 1

        st.success(message)
        st.write(f"현재 점수: **{st.session_state.score}점**")
else:
    st.subheader("📊 게임 종료")
    st.write(f"💯 최종 점수: **{st.session_state.score}점**")

    if st.session_state.score > 0:
        st.balloons()
        st.success("🎉 당신이 이겼습니다!")
    elif st.session_state.score < 0:
        st.error("😓 컴퓨터가 이겼습니다.")
    else:
        st.info("😐 무승부입니다.")

    if st.button("🔄 다시 시작하기"):
        st.session_state.score = 0
        st.session_state.round = 1
