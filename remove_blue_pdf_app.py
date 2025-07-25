import streamlit as st
import tempfile
import os
from pdf2image import convert_from_path
from PIL import Image
from fpdf import FPDF
import numpy as np

# 💡 Poppler 설치 경로 (Windows 전용)
POPLER_PATH = r"D:/poppler-23.11.0/Library/bin"  # 본인의 poppler bin 경로로 바꾸세요

# 🔧 파란색 제거 함수 (OpenCV 없이 Pillow만 사용)
def remove_blue_with_pillow(pil_image: Image.Image) -> Image.Image:
    img = pil_image.convert("RGB")
    data = np.array(img)

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]

    # 파란색 조건: blue > 130 이고 red/green보다 우위
    mask = (blue > 130) & (blue > red + 30) & (blue > green + 30)

    data[mask] = [255, 255, 255]  # 흰색으로 덮기

    return Image.fromarray(data)

# 🔁 PDF 변환 및 처리 함수
def process_pdf_selected_pages(file_bytes: bytes, poppler_path: str, selected_pages: list) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(file_bytes)
        pdf_path = tmp_pdf.name

    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    temp_dir = tempfile.mkdtemp()
    image_paths = []

    total_pages = len(images)

    for i, image in enumerate(images):
        page_num = i + 1
        if page_num in selected_pages:
            st.info(f"🔧 페이지 {page_num} → 파란색 제거 적용")
            processed_image = remove_blue_with_pillow(image)
        else:
            st.info(f"➡️ 페이지 {page_num} → 원본 유지")
            processed_image = image

        img_path = os.path.join(temp_dir, f"page_{i}.jpg")
        processed_image.save(img_path, "JPEG")
        image_paths.append(img_path)

    pdf = FPDF(unit='pt', format=[images[0].width, images[0].height])
    for img_path in image_paths:
        pdf.add_page()
        pdf.image(img_path, 0, 0)

    output_pdf_path = os.path.join(temp_dir, "선택페이지_정답제거_결과.pdf")
    pdf.output(output_pdf_path)
    return output_pdf_path

# ───────────────────────────────────────────────
# 🎨 Streamlit 인터페이스
st.set_page_config(page_title="선택 페이지 정답 제거기", layout="centered")
st.title("🧹 선택 페이지 정답 제거기 (파란색만 삭제)")
st.markdown("PDF에서 **선택한 페이지에만** 파란색 정답/풀이를 제거합니다.")

uploaded_file = st.file_uploader("📤 PDF 파일 업로드", type=["pdf"])

if uploaded_file:
    st.success(f"✅ 파일 '{uploaded_file.name}' 업로드 완료!")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_pdf_path = tmp_input.name

    # 전체 페이지 수 미리 파악
    try:
        all_images = convert_from_path(input_pdf_path, poppler_path=POPLER_PATH)
        total_pages = len(all_images)
        st.info(f"📄 총 {total_pages}페이지가 감지되었습니다.")
    except Exception as e:
        st.error(f"❌ PDF 처리 중 오류: {e}")
        st.stop()

    # 페이지 번호 입력
    page_input = st.text_input("✏️ 정답 제거할 페이지 번호 입력 (쉼표로 구분, 예: 1,3,5)")
    if page_input:
        try:
            selected_pages = sorted(set(int(p.strip()) for p in page_input.split(',') if p.strip().isdigit()))
            selected_pages = [p for p in selected_pages if 1 <= p <= total_pages]

            if not selected_pages:
                st.warning("⚠️ 유효한 페이지 번호가 없습니다.")
            else:
                st.success(f"🧹 선택된 페이지: {selected_pages}")

                with st.spinner("처리 중..."):
                    result_pdf_path = process_pdf_selected_pages(uploaded_file.read(), POPLER_PATH, selected_pages)

                with open(result_pdf_path, "rb") as result_file:
                    st.success("🎉 정답 제거 완료! 아래 버튼으로 다운로드하세요.")
                    st.download_button(
                        label="📥 결과 PDF 다운로드",
                        data=result_file,
                        file_name="정답제거_선택페이지.pdf",
                        mime="application/pdf"
                    )
        except Exception as e:
            st.error(f"⚠️ 페이지 번호 입력 오류: {e}")
