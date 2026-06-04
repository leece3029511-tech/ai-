import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Starbucks 메뉴 분석",
    page_icon="☕",
    layout="wide"
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("starbucks.csv")

df = load_data()

# -----------------------------
# 제목
# -----------------------------
st.title("☕ Starbucks 메뉴 영양성분 분석 대시보드")
st.markdown("수행평가용 데이터 분석 프로젝트")

# -----------------------------
# 데이터 미리보기
# -----------------------------
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df)

# -----------------------------
# 기본 통계
# -----------------------------
st.header("📊 데이터 요약")

col1, col2, col3, col4 = st.columns(4)

col1.metric("메뉴 수", len(df))
col2.metric("평균 칼로리", f"{df['Calories'].mean():.1f} kcal")
col3.metric("평균 지방", f"{df['Fat (g)'].mean():.1f} g")
col4.metric("평균 단백질", f"{df['Protein (g)'].mean():.1f} g")

# -----------------------------
# 상관관계 그래프
# -----------------------------
st.header("🔥 칼로리와 지방의 관계")

fig_scatter = px.scatter(
    df,
    x="Fat (g)",
    y="Calories",
    hover_name="Menu",
    size="Protein (g)",
    color="Protein (g)",
    title="지방이 많을수록 칼로리가 높은가?"
)

st.plotly_chart(fig_scatter, use_container_width=True)

corr = df["Calories"].corr(df["Fat (g)"])

st.info(f"상관계수 : {corr:.2f}")

# -----------------------------
# TOP10 메뉴
# -----------------------------
st.header("🏆 칼로리 TOP10 메뉴")

top10 = df.sort_values(
    "Calories",
    ascending=False
).head(10)

fig_top10 = px.bar(
    top10,
    x="Calories",
    y="Menu",
    orientation="h",
    color="Calories",
    text="Calories",
    title="칼로리 TOP10"
)

fig_top10.update_layout(
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(fig_top10, use_container_width=True)

# -----------------------------
# 건강한 메뉴 추천
# -----------------------------
st.header("🥗 건강한 메뉴 추천")

healthy = df.copy()

healthy["건강점수"] = (
    healthy["Protein (g)"] * 2
    - healthy["Calories"] * 0.02
    - healthy["Fat (g)"] * 0.5
)

healthy = healthy.sort_values(
    "건강점수",
    ascending=False
)

recommend = healthy.head(10)

st.dataframe(
    recommend[
        [
            "Menu",
            "Calories",
            "Fat (g)",
            "Protein (g)",
            "건강점수"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# 메뉴 검색
# -----------------------------
st.header("🔍 메뉴 검색")

menu = st.selectbox(
    "메뉴 선택",
    df["Menu"].sort_values()
)

selected = df[df["Menu"] == menu]

if not selected.empty:

    row = selected.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("칼로리", row["Calories"])
    col2.metric("지방", row["Fat (g)"])
    col3.metric("탄수화물", row["Carb. (g)"])
    col4.metric("단백질", row["Protein (g)"])

# -----------------------------
# 건강점수 TOP10 그래프
# -----------------------------
st.header("💪 건강점수 TOP10")

fig_health = px.bar(
    recommend,
    x="건강점수",
    y="Menu",
    orientation="h",
    color="건강점수",
    text="건강점수"
)

fig_health.update_layout(
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(fig_health, use_container_width=True)

# -----------------------------
# 결론
# -----------------------------
st.header("📌 분석 결론")

st.success(
"""
1. 지방 함량이 높을수록 칼로리가 증가하는 경향이 있다.
2. 단백질이 높은 메뉴는 포만감이 높아 건강식으로 적합하다.
3. Protein Bowl 계열 메뉴가 건강점수가 가장 높게 나타난다.
4. 일부 샌드위치 메뉴는 단백질 대비 칼로리가 높다.
"""
)
