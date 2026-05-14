# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------
# 페이지 설정
# ---------------------------------------------------
st.set_page_config(
    page_title="MBTI World Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# 데이터 불러오기
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

mbti_types = [col for col in df.columns if col != "Country"]

# ---------------------------------------------------
# 스타일
# ---------------------------------------------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 10px;
}

.sub-text {
    color: #666;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 타이틀
# ---------------------------------------------------
st.markdown(
    '<div class="main-title">🌍 MBTI World Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-text">국가별 MBTI 비율을 인터랙티브하게 분석해보세요.</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# 탭 생성
# ---------------------------------------------------
tab1, tab2 = st.tabs([
    "🌎 국가별 MBTI 분석",
    "🏆 MBTI 상위 10% 국가"
])

# ===================================================
# TAB 1
# ===================================================
with tab1:

    st.subheader("국가별 MBTI 비율")

    country = st.selectbox(
        "국가 선택",
        sorted(df["Country"].unique())
    )

    # 선택 국가 데이터
    country_row = df[df["Country"] == country].iloc[0]

    chart_df = pd.DataFrame({
        "MBTI": mbti_types,
        "Ratio": [country_row[m] for m in mbti_types]
    })

    chart_df = chart_df.sort_values(
        by="Ratio",
        ascending=False
    ).reset_index(drop=True)

    # 색상 설정
    blues = px.colors.sequential.Blues[::-1]

    colors = []

    for i in range(len(chart_df)):
        if i == 0:
            colors.append("#ff2b2b")  # 1등 빨강
        else:
            colors.append(
                blues[min(i + 2, len(blues)-1)]
            )

    # 그래프
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=chart_df["MBTI"],
            y=chart_df["Ratio"],
            marker_color=colors,
            text=[
                f"{v*100:.1f}%"
                for v in chart_df["Ratio"]
            ],
            textposition="outside",
            hovertemplate=
            "<b>%{x}</b><br>" +
            "비율: %{y:.2%}<extra></extra>"
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=650,
        title=f"{country} MBTI 분포",
        title_font_size=28,
        font=dict(size=16),
        hovermode="x unified",
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis_tickformat=".0%",
        margin=dict(t=80, l=30, r=30, b=30)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # TOP3
    st.subheader("🏆 TOP 3 MBTI")

    top3 = chart_df.head(3)

    cols = st.columns(3)

    for idx, (_, row) in enumerate(top3.iterrows()):
        with cols[idx]:
            st.metric(
                row["MBTI"],
                f"{row['Ratio']*100:.2f}%"
            )

# ===================================================
# TAB 2
# ===================================================
with tab2:

    st.subheader("MBTI 유형별 상위 10% 국가")

    selected_mbti = st.selectbox(
        "MBTI 선택",
        mbti_types
    )

    # 상위 국가 정렬
    top_df = df.sort_values(
        by=selected_mbti,
        ascending=False
    )

    # 상위 10%
    top_n = max(1, int(len(top_df) * 0.1))

    top_df = top_df.head(top_n)

    # 색상
    blues = px.colors.sequential.Blues[::-1]

    colors = []

    for i in range(len(top_df)):
        if i == 0:
            colors.append("#ff2b2b")
        else:
            colors.append(
                blues[min(i + 2, len(blues)-1)]
            )

    # 그래프 생성
    fig2 = go.Figure()

    fig2.add_trace(
        go.Bar(
            x=top_df["Country"],
            y=top_df[selected_mbti],
            marker_color=colors,
            text=[
                f"{v*100:.1f}%"
                for v in top_df[selected_mbti]
            ],
            textposition="outside",
            hovertemplate=
            "<b>%{x}</b><br>" +
            f"{selected_mbti}: " +
            "%{y:.2%}<extra></extra>"
        )
    )

    fig2.update_layout(
        template="plotly_white",
        height=700,
        title=f"{selected_mbti} 비율 상위 10% 국가",
        title_font_size=28,
        font=dict(size=15),
        xaxis_title="국가",
        yaxis_title="비율",
        yaxis_tickformat=".0%",
        hovermode="x unified",
        margin=dict(t=80, l=30, r=30, b=80)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # 데이터 표시
    with st.expander("상위 국가 데이터 보기"):
        st.dataframe(
            top_df[["Country", selected_mbti]],
            use_container_width=True
        )
