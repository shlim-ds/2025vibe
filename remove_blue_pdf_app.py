import streamlit as st
import tempfile
import os
from pdf2image import convert_from_path
from PIL import Image
from fpdf import FPDF

import numpy as np

# Windows 사용자: Poppler 경로 설정
POPLER_PATH = r"D:/poppler-23.11.0/Library/bin"  # 본인의 경로로 수정하세요

# 🔧 OpenCV 없이 파란색 제거 함수 (Pillow + NumPy만 사용)
def remove_blue_with_pillow(pil_image: Image.Image) -> Image.Image:
    img = pil_image.convert("RGB")
    data = np.array(img)

    # RGB → 파란색 영역 조건 정의
    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]

    # 파란색 조건: 파란색이 많이 강하고 R,G보다 높으면 제거
    mask = (blue > 130) & (blue > red + 30) & (blue > green + 30)

    # 파란색 부분을 흰색으로 변경
    data[mask] = [255, 255, 255]

    return Image.fromarray(data)

# 🔁 PDF 처리 함수 (OpenCV 없이 동작)
def process_pdf(file_bytes: bytes, poppler_path: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(file_bytes)
        pdf_path = tmp_pdf.name

    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    temp_dir = tempfile.mkdtemp()
    image_paths = []

    for i, image in enumerate(images):
        cleaned = remove_blue_with_pillow(image)
        img_path = os.path.join(temp_dir, f"page_{i}.jpg")
        cleaned.save(img_path, "JPEG")
        image_paths.append(img_path)

    # 이미지들을 PDF로 저장
    pdf = FPDF(unit='pt', format=[images[0].width, images[0].height])
    for img_path in image_paths:
        pdf.add_page()
        pdf.image(img_path, 0, 0)

    output_pdf_path = os.path.join(temp_dir, "정답제거_결과.pdf")
    pdf.output(output_pdf_path)
    return output_pdf_path

# ────────────────────────────────────────────
# 🎨 Streamlit 인터페이스
st.set_page_config(page_title="정답 제거기 - PDF (OpenCV 없이)", layout="centered")
st.title("🧹 정답 제거기 - 파란색 풀이 자동 삭제 (OpenCV 미사용)")
st.markdown("Python 3.13 환경에서도 작동합니다. PDF에서 **파란색 텍스트**를 제거해 새 PDF로 저장합니다.")

uploaded_file = st.file_uploader("📤 PDF 파일 업로드", type=["pdf"])

if uploaded_file:
    st.success(f"✅ 파일 '{uploaded_file.name}' 업로드 완료!")

    with st.spinner("🔍 파란색 텍스트 제거 중..."):
        try:
            result_pdf_path = process_pdf(uploaded_file.read(), poppler_path=POPLER_PATH)
        except Exception as e:
            st.error(f"🚨 처리 실패: {e}")
            st.stop()

    with open(result_pdf_path, "rb") as result_file:
        st.success("🎉 정답 제거 완료! 아래 버튼으로 다운로드하세요.")
        st.download_button(
            label="📥 정답 제거된 PDF 다운로드",
            data=result_file,
            file_name="정답제거_결과.pdf",
            mime="application/pdf"
        )
