import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io
import os

# ✅ Poppler 설치 경로 (사용자 환경에 맞게 수정 완료됨)
POPLER_PATH = r"D:\poppler-23.11.0\Library\bin"  # 역슬래시(\) 대신 r-string 또는 슬래시(/) 사용 권장

st.set_page_config(page_title="PDF → 이미지 변환기", layout="centered")
st.title("📄 PDF 파일을 이미지로 변환")

# 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file:
    try:
        st.info("PDF를 이미지로 변환 중입니다...")

        # PDF → 이미지 (첫 페이지만 변환)
        images = convert_from_bytes(
            uploaded_file.read(),
            dpi=200,
            poppler_path=POPLER_PATH,
            first_page=1,
            last_page=1
        )

        # 첫 번째 페이지만 표시
        image = images[0]
        st.image(image, caption="PDF 첫 페이지 이미지", use_column_width=True)

        # 다운로드 링크 생성
        img_io = io.BytesIO()
        image.save(img_io, format="PNG")
        img_io.seek(0)

        st.download_button(
            label="📥 이미지 다운로드",
            data=img_io,
            file_name="converted_page.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"🚨 PDF 변환 중 오류 발생:\n\n{e}")
