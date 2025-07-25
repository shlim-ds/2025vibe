import streamlit as st
import tempfile
import os
from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image
from fpdf import FPDF

# Poppler 설치 경로 (윈도우 전용)
POPLER_PATH = r"D:/poppler-24.08.0/Library/bin"  # 사용자의 설치 경로로 변경

def remove_blue_text(image: np.ndarray) -> np.ndarray:
    """파란색 계열 텍스트를 제거 (흰색 덮기)"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 파란색 범위 (필요시 조절 가능)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    image[mask > 0] = [255, 255, 255]  # 흰색으로 덮기

    return image

def process_pdf(pdf_file_path: str, poppler_path: str) -> str:
    # PDF → 이미지 변환
    images = convert_from_path(pdf_file_path, poppler_path=poppler_path)

    # 임시 저장 디렉토리
    temp_dir = tempfile.mkdtemp()
    image_paths = []

    for i, image in enumerate(images):
        # OpenCV 변환
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 파란색 제거
        cleaned_img = remove_blue_text(img_cv)

        # 다시 PIL 이미지로
        cleaned_pil = Image.fromarray(cv2.cvtColor(cleaned_img, cv2.COLOR_BGR2RGB))

        # 이미지 저장
        img_path = os.path.join(temp_dir, f"page_{i}.jpg")
        cleaned_pil.save(img_path, "JPEG")
        image_paths.append(img_path)

    # PDF 파일 재구성
    pdf = FPDF(unit='pt', format=[images[0].width, images[0].height])
    for img_path in image_paths:
        pdf.add_page()
        pdf.image(img_path, 0, 0)
    
    output_pdf_path = os.path.join(temp_dir, "정답제거_결과.pdf")
    pdf.output(output_pdf_path)

    return output_pdf_path

# ───────────────────────────────
# 📘 Streamlit UI

st.set_page_config(page_title="정답 제거 PDF 앱", layout="centered")
st.title("🧹 정답 제거기 - 파란색 풀이 지우기")
st.write("업로드된 PDF에서 파란색으로 표시된 **정답 또는 풀이**를 자동으로 제거합니다.")

uploaded_file = st.file_uploader("📤 PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file:
    st.success("✅ 파일이 업로드되었습니다. 처리 중입니다...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_pdf_path = tmp_input.name

    with st.spinner("🛠️ 정답(파란색) 제거 중..."):
        try:
            output_pdf_path = process_pdf(input_pdf_path, poppler_path=POPLER_PATH)
        except Exception as e:
            st.error(f"🚨 오류 발생: {e}")
            st.stop()

    with open(output_pdf_path, "rb") as f:
        st.success("🎉 처리가 완료되었습니다! 아래 버튼을 눌러 결과를 다운로드하세요.")
        st.download_button(
            label="📥 정답 제거된 PDF 다운로드",
            data=f,
            file_name="정답제거_결과.pdf",
            mime="application/pdf"
        )
