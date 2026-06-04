import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="스타벅스 메뉴 영양 분석",
    page_icon="☕",
    layout="wide"
)

st.title("☕ 스타벅스 메뉴 영양성분 분석")
st.markdown("스타벅스 메뉴 데이터를 활용한 수행평가 프로젝트")

# -------------------------
# 데이터 불러오기
# -------------------------
@st.cache_data
def load_data():
    return pd.read_excel("스타벅스매뉴(1).xlsx")

df = load_data()

# 컬럼명 정리
df.columns = [col.strip() for col in df.columns]

# -------------------------
# 데이터 확인
# -------------------------
st.header("📋 데이터 미리보기")

st.dataframe(df.head())

# -------------------------
# 기본 통계
# -------------------------
st.header("📊 기초 통계")

numeric_cols = df.select_dtypes(include="number").columns

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("메뉴 수", len(df))

with col2:
    st.metric(
        "평균 칼로리",
        f"{df['Calories'].mean():.1f} kcal"
    )

with col3:
    st.metric(
        "최고 칼로리",
        f"{df['Calories'].max():.0f} kcal"
    )

st.dataframe(df[numeric_cols].describe())

# -------------------------
# 칼로리 TOP10
# -------------------------
st.header("🔥 칼로리 TOP 10 메뉴")

top10 = df.nlargest(10, "Calories")

fig1 = px.bar(
    top10,
    x="Calories",
    y="Menu",
    orientation="h",
    color="Calories",
    title="칼로리가 높은 메뉴 TOP 10"
)

fig1.update_layout(
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# 히스토그램
# -------------------------
st.header("📈 칼로리 분포")

fig2 = px.histogram(
    df,
    x="Calories",
    nbins=20,
    title="칼로리 분포 히스토그램"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# 산점도
# -------------------------
st.header("🔍 지방과 칼로리의 관계")

fig3 = px.scatter(
    df,
    x="Fat",
    y="Calories",
    hover_name="Menu",
    size="Protein",
    color="Protein",
    title="지방(Fat)과 칼로리 관계"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# 메뉴 검색
# -------------------------
st.header("🔎 메뉴 검색")

keyword = st.text_input("메뉴 이름 입력")

if keyword:
    result = df[
        df["Menu"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

    st.write(f"검색 결과 : {len(result)}개")

    st.dataframe(result)

# -------------------------
# 영양성분 비교
# -------------------------
st.header("⚖️ 메뉴 영양성분 비교")

menu_list = df["Menu"].tolist()

selected = st.selectbox(
    "메뉴 선택",
    menu_list
)

selected_row = df[df["Menu"] == selected].iloc[0]

compare_df = pd.DataFrame({
    "영양성분": ["칼로리", "지방", "탄수화물", "식이섬유", "단백질"],
    "값": [
        selected_row["Calories"],
        selected_row["Fat"],
        selected_row["Carb."],
        selected_row["Fiber"],
        selected_row["Protein"]
    ]
})

fig4 = px.bar(
    compare_df,
    x="영양성분",
    y="값",
    title=f"{selected} 영양성분"
)

st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# 결론
# -------------------------
st.header("📝 분석 결과")

st.success(
"""
스타벅스 메뉴의 평균 칼로리는 약 357kcal이며,
대부분의 메뉴는 300~450kcal 구간에 분포한다.

샌드위치와 프로틴볼 메뉴는 단백질 함량이 높지만
칼로리도 높은 편이다.

과일 및 사이드 메뉴는 칼로리가 낮아
건강식 선택에 적합하다.
"""
)
