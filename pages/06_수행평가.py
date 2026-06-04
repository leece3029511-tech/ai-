import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="스타벅스 메뉴 영양정보",
    page_icon="☕"
)

st.title("☕ 스타벅스 메뉴 영양정보")

uploaded_file = st.file_uploader(
    "스타벅스매뉴.xlsx 파일 업로드",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:
        df = pd.read_excel(uploaded_file)

        menu_col = df.columns[0]

        selected_menu = st.selectbox(
            "메뉴 선택",
            sorted(df[menu_col].astype(str).unique())
        )

        menu_info = df[df[menu_col] == selected_menu].iloc[0]

        st.subheader(f"📋 {selected_menu}")

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

        st.subheader("전체 영양정보")
        st.dataframe(
            pd.DataFrame({
                "항목": menu_info.index,
                "값": menu_info.values
            }),
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"파일을 읽는 중 오류 발생: {e}")

else:
    st.info("엑셀 파일을 업로드해주세요.")
