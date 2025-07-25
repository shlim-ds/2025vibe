import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io

st.title("📘 정답 제거 PDF 변환기")
st.write("파란색 글씨로 된 정답을 제거한 학생용 PDF를 생성합니다.")

uploaded_file = st.file_uploader("📤 교사용 PDF 업로드", type=["pdf"])

def remove_blue_text(image):
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            # 파란색 계열 제거 조건
            if (r < 160 and g > 120 and b > 180) or (b - r > 50 and b - g > 40):
                pixels[x, y] = (255, 255, 255)
    return image

if uploaded_file:
    st.success("✅ 파일이 업로드되었습니다. 처리 중...")

    # PDF를 이미지로 변환
    images = convert_from_bytes(uploaded_file.read(), dpi=200)
    processed_images = []

    for img in images:
        cleaned = remove_blue_text(img.convert("RGB"))
        processed_images.append(cleaned)

    # 결과 PDF로 저장
    pdf_bytes = io.BytesIO()
    processed_images[0].save(
        pdf_bytes,
        format="PDF",
        save_all=True,
        append_images=processed_images[1:]
    )

    st.success("🎉 정답 제거가 완료되었습니다!")
    st.download_button(
        label="📥 정답 제거된 PDF 다운로드",
        data=pdf_bytes.getvalue(),
        file_name="정답제거_학생용.pdf",
        mime="application/pdf"
    )
