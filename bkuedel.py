import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io
import os

# Poppler가 설치된 로컬 경로를 지정하세요
POPLER_PATH = "C:/poppler-23.11.0/Library/bin"  # 또는 리눅스/mac은 None

st.title("📄 PDF → 이미지 변환기")

uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file:
    try:
        st.info("PDF를 이미지로 변환 중입니다...")
        images = convert_from_bytes(
            uploaded_file.read(), 
            dpi=200, 
            first_page=1, 
            last_page=1,
            poppler_path=POPLER_PATH if os.name == "nt" else None
        )
        
        image = images[0]
        st.image(image, caption="PDF 첫 페이지", use_column_width=True)

        # 다운로드 버튼
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        st.download_button(
            label="📥 이미지 다운로드",
            data=img_io.getvalue(),
            file_name="converted_page.png",
            mime="image/png"
        )
    
    except Exception as e:
        st.error(f"PDF 변환 중 오류 발생: {e}")
