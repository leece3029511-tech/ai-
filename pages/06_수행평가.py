import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================
# 페이지 설정
# ======================================
st.set_page_config(
    page_title="스타벅스 메뉴 영양 분석",
    page_icon="☕",
    layout="wide"
)

# ======================================
# 데이터 불러오기
# ======================================
@st.cache_data
def load_data():

    encodings = [
        "utf-8",
        "cp949",
        "euc-kr",
        "latin1"
    ]

    for enc in encodings:
        try:
            return pd.read_csv(
                "starbucks.csv",
                encoding=enc
            )
        except:
            continue

    st.error("starbucks.csv 파일을 찾을 수 없습니다.")
    st.stop()

df = load_data()

# ======================================
# 컬럼 확인
# ======================================
required_columns = [
    "Menu",
    "Calories",
    "Fat (g)",
    "Carb. (g)",
    "Fiber (g)",
    "Protein (g)"
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:
    st.error(f"필수 컬럼이 없습니다: {missing}")
    st.write("현재 컬럼:")
    st.write(df.columns.tolist())
    st.stop()

# ======================================
# 제목
# ======================================
st.title("☕ 스타벅스 메뉴 영양 분석 대시보드")
st.markdown("---")

# ======================================
# 데이터 보기
# ======================================
with st.expander("원본 데이터 보기"):
    st.dataframe(
        df,
        use_container_width=True
    )

# ======================================
# 주요 통계
# ======================================
st.subheader("📊 주요 통계")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "메뉴 수",
    len(df)
)

c2.metric(
    "평균 칼로리",
    f"{df['Calories'].mean():.1f} kcal"
)

c3.metric(
    "평균 단백질",
    f"{df['Protein (g)'].mean():.1f} g"
)

c4.metric(
    "평균 지방",
    f"{df['Fat (g)'].mean():.1f} g"
)

st.markdown("---")

# ======================================
# 칼로리 TOP10
# ======================================
st.subheader("🔥 칼로리 TOP10 메뉴")

top10 = (
    df.sort_values(
        by="Calories",
        ascending=False
    )
    .head(10)
)

fig_top10 = px.bar(
    top10,
    x="Calories",
    y="Menu",
    orientation="h",
    text="Calories",
    title="칼로리가 높은 메뉴 TOP10"
)

fig_top10.update_layout(
    height=600,
    yaxis={"categoryorder":"total ascending"}
)

st.plotly_chart(
    fig_top10,
    use_container_width=True
)

# ======================================
# 상관관계 분석
# ======================================
st.subheader("📈 영양성분 상관관계")

corr_columns = [
    "Calories",
    "Fat (g)",
    "Carb. (g)",
    "Fiber (g)",
    "Protein (g)"
]

corr = df[corr_columns].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    title="영양성분 상관관계"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# ======================================
# 산점도
# ======================================
st.subheader("🔍 칼로리와 단백질 관계")

fig_scatter = px.scatter(
    df,
    x="Calories",
    y="Protein (g)",
    hover_name="Menu",
    size="Protein (g)",
    title="칼로리 vs 단백질"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ======================================
# 건강한 메뉴 추천
# ======================================
st.subheader("🥗 건강한 메뉴 추천")

healthy = df[
    (df["Calories"] <= 300)
    & (df["Fat (g)"] <= 10)
    & (df["Protein (g)"] >= 10)
]

healthy = healthy.sort_values(
    by="Protein (g)",
    ascending=False
)

st.write(
    "조건: 칼로리 300 이하 · 지방 10g 이하 · 단백질 10g 이상"
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

# ======================================
# 건강 점수 TOP5
# ======================================
st.subheader("🏆 건강 점수 TOP5")

df["Health Score"] = (
    df["Protein (g)"] * 3
    - df["Calories"] * 0.02
    - df["Fat (g)"] * 0.5
)

best = (
    df.sort_values(
        by="Health Score",
        ascending=False
    )
    .head(5)
)

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

# ======================================
# 메뉴 검색
# ======================================
st.subheader("🔎 메뉴 검색")

keyword = st.text_input(
    "메뉴 이름 입력"
)

if keyword:

    result = df[
        df["Menu"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

    st.write(
        f"검색 결과: {len(result)}개"
    )

    st.dataframe(
        result,
        use_container_width=True
    )

st.success("분석 완료!")
