import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# 페이지 설정
st.set_page_config(page_title="드론 추천 + 단계별 비행 원리 안내", layout="wide")
st.title("🛩️ 드론 추천 + 한국 규제 + 단계별 비행 원리 프로그램")

st.markdown("사용자의 이해 수준에 맞는 단계별 설명과 함께 시각 자료로 드론 비행 원리를 쉽게 배울 수 있습니다.")

# ---------------------------
# 사용자 수준 선택
# ---------------------------
st.header("👤 사용자 이해 수준 선택")

level = st.radio("드론에 대해 얼마나 알고 계신가요?", ["입문자", "기초 사용자", "전문가"])

# ---------------------------
# 단계별 비행 원리 설명
# ---------------------------
st.header("✈️ 단계별 드론 비행 원리 설명")

if level == "입문자":
    st.subheader("👶 입문자용 설명")
    st.markdown("""
    - 드론은 하늘을 나는 **무인 비행 장치**예요.  
    - 보통 4개의 **프로펠러**를 가지고 있고, 리모컨으로 조종할 수 있어요.  
    - 프로펠러가 공기를 아래로 밀어내면, 드론은 하늘로 **둥! 뜨게 돼요**.  
    - **앞으로 가거나 회전하는 건** 각각의 프로펠러가 **속도를 다르게 내서** 조절해요.
    """)

elif level == "기초 사용자":
    st.subheader("📘 기초 사용자용 설명")
    st.markdown("""
    - 드론의 기본 비행 원리는 다음 용어들로 구성됩니다:

    | 용어 | 설명 |
    |------|------|
    | **Lift (양력)** | 위로 뜨는 힘, 프로펠러가 공기를 아래로 밀어냄 |
    | **Thrust (추력)** | 앞으로 나아가는 힘 |
    | **Pitch (피치)** | 앞뒤로 기울이는 동작 |
    | **Roll (롤)** | 좌우로 기울이는 동작 |
    | **Yaw (요우)** | 제자리에서 회전하는 동작 |
    
    - 이 움직임을 조합해 드론은 모든 방향으로 움직일 수 있어요.
    """)

elif level == "전문가":
    st.subheader("🧠 전문가용 설명")
    st.markdown("""
    - 드론은 **멀티콥터 기반 무인 항공기(UAV)**로, 일반적으로 **PID 제어**, **IMU 센서**, **GPS** 기반 자동 항법 시스템을 탑재하고 있습니다.
    
    - 4개의 프로펠러를 가진 쿼드콥터 기준:

    | 동작 | 설명 | 프로펠러 반응 예시 |
    |------|------|-------------------|
    | **이륙 (Lift)** | 4개 프로펠러 동일하게 가속 | ↑↑↑↑ |
    | **전진 (Pitch)** | 뒤쪽 프로펠러 가속, 앞쪽 감속 | ↑↓↑↓ |
    | **좌우 이동 (Roll)** | 좌우 쌍 속도 조절 | ← / → |
    | **회전 (Yaw)** | 대각선 프로펠러 반대 회전 | ↺ / ↻ |

    - 제어계는 보통 **카르만 필터 기반 센서 퓨전**으로 기울기·속도·위치 정보를 계산합니다.
    """)

# ---------------------------
# 비행 원리 그림 추가
# ---------------------------
st.header("🖼️ 드론 비행 원리 시각화")

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Quadcopter_flight_dynamics.svg/1024px-Quadcopter_flight_dynamics.svg.png"
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
st.image(img, caption="쿼드콥터 비행 원리 도식 (출처: Wikimedia Commons)", use_column_width=True)

st.success("🎯 선택한 수준에 맞춰 비행 원리 설명을 완료했습니다. 추천 시스템과도 통합 가능합니다.")
