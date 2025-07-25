
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ------------------ 데이터 로딩 ------------------
@st.cache_data
def load_data():
    return pd.read_csv("202506_202506_연령별인구현황_월간_남여구분.csv", encoding="cp949")

@st.cache_data
def load_coordinates():
    # 위경도 포함된 행정동별 좌표 파일 예시
    coords_url = "https://raw.githubusercontent.com/younghoonjo/data/main/korea_adm_geocoded.csv"
    return pd.read_csv(coords_url)

df = load_data()
coords_df = load_coordinates()

# ------------------ 지역 컬럼 분리 ------------------
df["시도"] = df["행정구역"].str.extract(r"(^[^\s]+[시도])")
df["시도_이후"] = df["행정구역"].str.replace(r"\([^)]*\)", "", regex=True)
df["구군"] = df["시도_이후"].str.extract(r"(?:[^\s]+[시도])?\s*([^\s]+[구군시동면])")

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="2025 인구 분석", layout="wide")
st.title("👥 2025년 6월 연령별 인구 분석 + 지도 시각화")

# 시도 선택
sido_list = df["시도"].dropna().unique()
selected_sido = st.selectbox("🗺️ 시/도 선택", sorted(sido_list))

# 자치구 선택
gugun_df = df[df["시도"] == selected_sido]
gugun_list = gugun_df["구군"].dropna().unique()
selected_gugun = st.selectbox("🏙️ 자치구/지역 선택", sorted(gugun_list))

# 선택 지역 필터링
matched_region = df[(df["시도"] == selected_sido) & (df["구군"] == selected_gugun)]
if matched_region.empty:
    st.warning("선택한 지역에 해당하는 데이터가 없습니다.")
    st.stop()
region_df = matched_region.iloc[0]

# ------------------ 연령별 컬럼 분리 ------------------
male_cols = [col for col in df.columns if "남_" in col and "세" in col]
female_cols = [col for col in df.columns if "여_" in col and "세" in col]
ages = [col.split("_")[-1] for col in male_cols]

# 숫자 처리 함수
def clean_number(val):
    if pd.isna(val):
        return 0
    return int(str(val).replace(",", ""))

male_values = region_df[male_cols].apply(clean_number).values
female_values = region_df[female_cols].apply(clean_number).values

# ------------------ 통계 계산 ------------------
total_population = male_values.sum() + female_values.sum()

age_groups = {
    "유소년(0~14세)": range(0, 15),
    "청년층(15~29세)": range(15, 30),
    "중장년층(30~64세)": range(30, 65),
    "고령층(65세 이상)": range(65, 101)
}

group_counts = {}
for label, age_range in age_groups.items():
    count = 0
    for i, age_label in enumerate(ages):
        if "세" in age_label:
            age = int(age_label.replace("세", "").replace("이상", "").strip())
            if age in age_range:
                count += male_values[i] + female_values[i]
    group_counts[label] = count

# ------------------ 통계 출력 ------------------
st.subheader(f"📈 {selected_sido} {selected_gugun} 인구 통계 요약")
col1, col2 = st.columns(2)
with col1:
    st.metric("총 인구 수", f"{total_population:,} 명")
with col2:
    elderly_ratio = (group_counts["고령층(65세 이상)"] / total_population) * 100
    st.metric("고령 인구 비율", f"{elderly_ratio:.2f} %")

# ------------------ 연령대 비율 ------------------
st.subheader("🧮 연령 그룹별 인구 구성 비율")
group_df = pd.DataFrame({
    "연령대": list(group_counts.keys()),
    "인구수": list(group_counts.values())
})
group_df["비율(%)"] = group_df["인구수"] / total_population * 100
st.dataframe(group_df, use_container_width=True)

fig_pie = go.Figure(data=[
    go.Pie(labels=group_df["연령대"], values=group_df["인구수"], hole=0.4)
])
fig_pie.update_layout(title="연령 그룹별 인구 비율")
st.plotly_chart(fig_pie, use_container_width=True)

# ------------------ 인구 피라미드 ------------------
st.subheader("👤 연령별 인구 피라미드")
fig = go.Figure()
fig.add_trace(go.Bar(y=ages, x=male_values * -1, name="남성", orientation='h', marker=dict(color='steelblue')))
fig.add_trace(go.Bar(y=ages, x=female_values, name="여성", orientation='h', marker=dict(color='lightcoral')))
fig.update_layout(
    title=f"{selected_sido} {selected_gugun} 연령별 인구 피라미드 (2025년 6월)",
    barmode='relative',
    xaxis=dict(title='인구 수', tickvals=[-50000, -25000, 0, 25000, 50000],
               ticktext=['50,000', '25,000', '0', '25,000', '50,000']),
    yaxis=dict(title='연령'),
    height=800
)
st.plotly_chart(fig, use_container_width=True)

# ------------------ 지도 시각화 ------------------
st.subheader("🗺️ 선택 지역 인구 지도 시각화")

# 위경도 병합
df_map = df.copy()
df_map["행정구역_정제"] = df_map["행정구역"].str.replace(r"\([^)]*\)", "", regex=True).str.strip()
merged = pd.merge(df_map, coords_df, left_on="행정구역_정제", right_on="행정구역", how="left")
merged["총인구"] = merged[male_cols + female_cols].applymap(clean_number).sum(axis=1)

map_data = merged[(merged["시도"] == selected_sido) & (merged["구군"] == selected_gugun)]
map_data = map_data.dropna(subset=["lat", "lon"])

if map_data.empty:
    st.info("이 지역에 대한 위경도 정보가 없어 지도에 표시할 수 없습니다.")
else:
    fig_map = px.scatter_mapbox(
        map_data,
        lat="lat",
        lon="lon",
        size="총인구",
        color="총인구",
        hover_name="행정구역_정제",
        zoom=11,
        height=600,
        mapbox_style="carto-positron",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_map, use_container_width=True)
