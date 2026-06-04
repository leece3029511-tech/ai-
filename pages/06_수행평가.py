import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ===================================
# 페이지 설정
# ===================================
st.set_page_config(
    page_title="☕ Starbucks 메뉴 분석",
    page_icon="☕",
    layout="wide"
)

# ===================================
# 데이터 로드
# ===================================
@st.cache_data
def load_data():

    possible_files = [
        "starbucks.csv",
        "Starbucks.csv",
        "data/starbucks.csv",
        Path(__file__).parent.parent / "starbucks.csv"
    ]

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp949",
        "euc-kr",
        "latin1"
    ]

    for file in possible_files:

        try:
            if not Path(file).exists():
                continue

            for enc in encodings:

                try:
                    df = pd.read_csv(
                        file,
                        encoding=enc
                    )

                    if len(df) > 0:
                        return df

                except Exception:
                    pass

            try:
                df = pd.read_excel(file)

                if len(df) > 0:
                    return df

            except Exception:
                pass

        except Exception:
            pass

    st.error("❌ starbucks.csv 파일을 찾거나 읽을 수 없습니다.")
    st.stop()

df = load_data()

# ===================================
# 컬럼명 정리
# ===================================
df.columns = (
    df.columns
    .str.strip()
    .str.replace("\n", "")
)

# ===================================
# 필수 컬럼 확인
# ===================================
required_cols = [
    "Menu",
    "Calories",
    "Fat (g)",
    "Carb. (g)",
    "Protein (g)"
]

missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"필수 컬럼이 없습니다: {missing}")
    st.write("현재 컬럼 목록")
    st.write(df.columns.tolist())
    st.stop()

# ===================================
# 제목
# ===================================
st.title("☕ Starbucks 메뉴 분석 대시보드")
st.markdown("---")

# ===================================
# 데이터 확인
# ===================================
with st.expander("원본 데이터 보기"):
    st.dataframe(df)

# ===================================
# KPI
# ===================================
st.header("📊 데이터 요약")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "메뉴 수",
    len(df)
)

c2.metric(
    "평균 칼로리",
    round(df["Calories"].mean(), 1)
)

c3.metric(
    "평균 지방(g)",
    round(df["Fat (g)"].mean(), 1)
)

c4.metric(
    "평균 단백질(g)",
    round(df["Protein (g)"].mean(), 1)
)

# ===================================
# 칼로리 분포
# ===================================
st.header("🔥 칼로리 분포")

fig_hist = px.histogram(
    df,
    x="Calories",
    nbins=20,
    title="칼로리 분포"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ===================================
# 상관관계
# ===================================
st.header("📈 지방과 칼로리 관계")

corr = df["Calories"].corr(df["Fat (g)"])

st.info(
    f"상관계수: {corr:.2f}"
)

fig_scatter = px.scatter(
    df,
    x="Fat (g)",
    y="Calories",
    color="Protein (g)",
    size="Protein (g)",
    hover_name="Menu",
    title="지방 vs 칼로리"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ===================================
# TOP10
# ===================================
st.header("🏆 칼로리 TOP10 메뉴")

top10 = (
    df.sort_values(
        "Calories",
        ascending=False
    )
    .head(10)
)

fig_top = px.bar(
    top10,
    x="Calories",
    y="Menu",
    orientation="h",
    color="Calories",
    text="Calories"
)

fig_top.update_layout(
    yaxis={
        "categoryorder":"total ascending"
    }
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)

# ===================================
# 건강 점수
# ===================================
st.header("🥗 건강한 메뉴 추천")

healthy = df.copy()

healthy["건강점수"] = (
    healthy["Protein (g)"] * 3
    - healthy["Calories"] * 0.03
    - healthy["Fat (g)"] * 0.5
)

healthy = healthy.sort_values(
    "건강점수",
    ascending=False
)

best10 = healthy.head(10)

st.dataframe(
    best10[
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

# ===================================
# 건강점수 그래프
# ===================================
fig_health = px.bar(
    best10,
    x="건강점수",
    y="Menu",
    orientation="h",
    color="건강점수",
    text_auto=".1f"
)

fig_health.update_layout(
    yaxis={
        "categoryorder":"total ascending"
    }
)

st.plotly_chart(
    fig_health,
    use_container_width=True
)

# ===================================
# 메뉴 검색
# ===================================
st.header("🔍 메뉴 검색")

menu = st.selectbox(
    "메뉴 선택",
    sorted(df["Menu"].unique())
)

row = df[df["Menu"] == menu].iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "칼로리",
    row["Calories"]
)

c2.metric(
    "지방(g)",
    row["Fat (g)"]
)

c3.metric(
    "탄수화물(g)",
    row["Carb. (g)"]
)

c4.metric(
    "단백질(g)",
    row["Protein (g)"]
)

# ===================================
# 결론
# ===================================
st.header("📌 분석 결과")

st.success(
"""
1. 지방 함량이 높을수록 칼로리가 증가하는 경향이 있다.

2. Protein Bowl, Panini 계열은 단백질 함량이 높다.

3. 일부 샐러드는 건강해 보이지만 지방 함량이 높다.

4. 건강 점수 기준으로는 고단백·저지방 메뉴가 상위권을 차지한다.
"""
)

# ===================================
# 디버그
# ===================================
with st.expander("⚙️ 디버그 정보"):
    st.write("파일 컬럼")
    st.write(df.columns.tolist())

    st.write("데이터 크기")
    st.write(df.shape)
