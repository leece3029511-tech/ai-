import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="스타벅스 메뉴 영양정보",
    page_icon="☕",
    layout="centered"
)

st.title("☕ 스타벅스 메뉴 영양정보")

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_excel("스타벅스매뉴.xlsx")

df = load_data()

# 메뉴명 컬럼 (첫 번째 컬럼 사용)
menu_col = df.columns[0]

# 메뉴 선택
selected_menu = st.selectbox(
    "메뉴를 선택하세요",
    sorted(df[menu_col].unique())
)

# 선택된 메뉴 데이터
menu_info = df[df[menu_col] == selected_menu].iloc[0]

st.subheader(f"📋 {selected_menu}")

# 영양정보 표시
col1, col2 = st.columns(2)

with col1:
    if "Calories" in df.columns:
        st.metric("칼로리", f"{menu_info['Calories']} kcal")

    if "Fat" in df.columns:
        st.metric("지방", f"{menu_info['Fat']} g")

    if "Protein" in df.columns:
        st.metric("단백질", f"{menu_info['Protein']} g")

with col2:
    if "Carb." in df.columns:
        st.metric("탄수화물", f"{menu_info['Carb.']} g")

    if "Fiber" in df.columns:
        st.metric("식이섬유", f"{menu_info['Fiber']} g")

# 전체 정보 표
st.subheader("전체 영양정보")

info_df = pd.DataFrame({
    "항목": menu_info.index,
    "값": menu_info.values
})

st.dataframe(
    info_df,
    use_container_width=True,
    hide_index=True
)
