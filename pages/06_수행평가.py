import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="스타벅스 메뉴 영양 분석",
    page_icon="☕",
    layout="wide"
)

# -------------------------
# 데이터 불러오기
# -------------------------
@st.cache_data
def load_data():

    encodings = ["utf-8", "cp949", "euc-kr", "latin1"]

    for enc in encodings:
        try:
            return pd.read_csv("starbucks(1).csv", encoding=enc)
        except:
            pass

    return pd.read_csv("starbucks(1).csv")

df = load_data()

# -------------------------
# 컬럼명 정리
# -------------------------
df.columns = [c.strip() for c in df.columns]

st.title("☕ 스타벅스 메뉴 영양 분석 대시보드")
st.markdown("---")

# -------------------------
# 데이터 미리보기
# -------------------------
with st.expander("데이터 보기"):
    st.dataframe(df, use_container_width=True)

# -------------------------
# 주요 통계
# -------------------------
st.subheader("📊 주요 통계")

col1, col2, col3, col4 = st.columns(4)

col1.metric("메뉴 수", len(df))
col2.metric("평균 칼로리", f"{df['Calories'].mean():.1f} kcal")
col3.metric("평균 단백질", f"{df['Protein (g)'].mean():.1f} g")
col4.metric("평균 지방", f"{df['Fat (g)'].mean():.1f} g")

st.markdown("---")

# -------------------------
# TOP10 칼로리 메뉴
# -------------------------
st.subheader("🔥 칼로리 TOP10 메뉴")

top10 = df.sort_values(
    by="Calories",
    ascending=False
).head(10)

fig_top10 = px.bar(
    top10,
    x="Calories",
    y="Menu",
    orientation="h",
    text="Calories",
    title="칼로리가 높은 메뉴 TOP10"
)

fig_top10.update_layout(height=600)

st.plotly_chart(
    fig_top10,
    use_container_width=True
)

# -------------------------
# 상관관계 분석
# -------------------------
st.subheader("📈 영양성분 상관관계")

corr_cols = [
    "Calories",
    "Fat (g)",
    "Carb. (g)",
    "Fiber (g)",
    "Protein (g)"
]

corr = df[corr_cols].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="영양성분 상관관계"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# -------------------------
# 산점도
# -------------------------
st.subheader("🔍 칼로리 vs 단백질")

fig_scatter = px.scatter(
    df,
    x="Calories",
    y="Protein (g)",
    hover_name="Menu",
    size="Protein (g)",
    title="칼로리와 단백질 관계"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# -------------------------
# 건강한 메뉴 추천
# -------------------------
st.subheader("🥗 건강한 메뉴 추천")

healthy = df[
    (df["Calories"] <= 300) &
    (df["Fat (g)"] <= 10) &
    (df["Protein (g)"] >= 10)
]

healthy = healthy.sort_values(
    by="Protein (g)",
    ascending=False
)

st.write(
    "조건: 칼로리 300 이하 + 지방 10g 이하 + 단백질 10g 이상"
)

st.dataframe(
    healthy[
        [
            "Menu",
            "Calories",
            "Protein (g)",
            "Fat (g)"
        ]
    ],
    use_container_width=True
)

# -------------------------
# 메뉴 검색
# -------------------------
st.subheader("🔎 메뉴 검색")

keyword = st.text_input("메뉴 이름 입력")

if keyword:

    result = df[
        df["Menu"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

    st.write(f"검색 결과: {len(result)}개")

    st.dataframe(
        result,
        use_container_width=True
    )

# -------------------------
# 최고 건강 메뉴
# -------------------------
st.subheader("🏆 추천 메뉴 TOP5")

score = (
    df["Protein (g)"] * 3
    - df["Calories"] * 0.02
    - df["Fat (g)"] * 0.5
)

df["Health Score"] = score

best = df.sort_values(
    by="Health Score",
    ascending=False
).head(5)

st.dataframe(
    best[
        [
            "Menu",
            "Calories",
            "Protein (g)",
            "Fat (g)",
            "Health Score"
        ]
    ],
    use_container_width=True
)

st.success("분석 완료!")
