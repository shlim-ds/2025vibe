import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io
import os

# ✅ Poppler 경로 수정됨 (백슬래시 끝에 문제 없도록)
POPLER_PATH = "D:/poppler-24.08.0/Library/bin"

# Poppler 실행 파일 존재 여부 확인
if not os.path.exists(os.path.join(POPLER_PATH, "pdftoppm.exe")):
    st.error("❌ Poppler 실행 파일이 존재하지 않습니다. 경로를 다시 확인하세요.")
    st.stop()

st.set_page_config(page_title="PDF → 이미지 변환기", layout="centered")
st.title("📄 PDF 파일을 이미지로 변환")

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

        image = images[0]
        st.image(image, caption="PDF 첫 페이지", use_column_width=True)

        # 다운로드 버튼
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
