import streamlit as st
import tempfile
import os

try:
    import cv2
except ImportError:
    st.error("❌ OpenCV(cv2)를 불러올 수 없습니다. Python 3.13은 지원되지 않습니다.\nPython 3.12 이하 환경에서 실행해주세요.")
    st.stop()

import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from fpdf import FPDF

# Poppler 경로 (Windows 사용자만 해당, macOS/Linux는 필요 없음)
POPLER_PATH = r"D:/poppler-23.11.0/Library/bin"  # 본인의 경로에 맞게 수정

# 파란색 제거 함수
def remove_blue_text(image: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    image[mask > 0] = [255, 255, 255]  # 흰색으로 덮기
    return image

# PDF 처리 함수
def process_pdf(pdf_file_path: str, poppler_path: str) -> str:
    images = convert_from_path(pdf_file_path, poppler_path=poppler_path)
    temp_dir = tempfile.mkdtemp()
    image_paths = []

    for i, image in enumerate(images):
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cleaned_img = remove_blue_text(img_cv)
        cleaned_pil = Image.fromarray(cv2.cvtColor(cleaned_img, cv2.COLOR_BGR2RGB))
        img_path = os.path.join(temp_dir, f"page_{i}.jpg")
        cleaned_pil.save(img_path, "JPEG")
        image_paths.append(img_path)

    pdf = FPDF(unit='pt', format=[images[0].width, images[0].height])
    for img_path in image_paths:
        pdf.add_page()
        pdf.image(img_path, 0, 0)

    output_pdf_path = os.path.join(temp_dir, "정답제거_결과.pdf")
    pdf.output(output_pdf_path)
    return output_pdf_path

# ─────────────────────────────────────
# Streamlit UI
st.set_page_config(page_title="정답 제거기", layout="centered")
st.title("🧹 정답 제거기 (파란색 텍스트 제거)")
st.markdown("PDF에서 **파란색으로 된 정답이나 풀이**를 자동으로 감지하여 제거하고 새 PDF로 저장합니다.")

uploaded_file = st.file_uploader("📤 PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file:
    st.success("✅ 파일 업로드 완료. 변환을 시작합니다.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_pdf_path = tmp_input.name

    with st.spinner("🔍 파란색 정답 제거 중..."):
        try:
            output_pdf_path = process_pdf(input_pdf_path, poppler_path=POPLER_PATH)
        except Exception as e:
            st.error(f"🚨 처리 중 오류 발생: {e}")
            st.stop()

    with open(output_pdf_path, "rb") as f:
        st.success("🎉 정답 제거 완료! 아래 버튼으로 다운로드하세요.")
        st.download_button(
            label="📥 정답 제거된 PDF 다운로드",
            data=f,
            file_name="정답제거_결과.pdf",
            mime="application/pdf"
        )
