# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="MBTI Country Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("🌍 국가별 MBTI 비율 대시보드")
st.markdown("국가를 선택하면 MBTI 유형 분포를 인터랙티브하게 확인할 수 있습니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# -----------------------------
# 국가 선택
# -----------------------------
country = st.selectbox(
    "국가를 선택하세요",
    sorted(df["Country"].unique())
)

# -----------------------------
# 선택 국가 데이터
# -----------------------------
country_data = df[df["Country"] == country].iloc[0]

mbti_cols = [col for col in df.columns if col != "Country"]

mbti_values = pd.DataFrame({
    "MBTI": mbti_cols,
    "Ratio": [country_data[col] for col in mbti_cols]
})

# 내림차순 정렬
mbti_values = mbti_values.sort_values(
    by="Ratio",
    ascending=False
).reset_index(drop=True)

# -----------------------------
# 색상 설정
# -----------------------------
max_idx = mbti_values["Ratio"].idxmax()

# 파란색 그라데이션
blue_colors = px.colors.sequential.Blues[::-1]

colors = []

for i in range(len(mbti_values)):
    if i == max_idx:
        colors.append("#ff2b2b")  # 1등 빨간색
    else:
        colors.append(
            blue_colors[min(i + 2, len(blue_colors) - 1)]
        )

# -----------------------------
# Plotly 그래프
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=mbti_values["MBTI"],
        y=mbti_values["Ratio"],
        marker_color=colors,
        text=[
            f"{v*100:.1f}%"
            for v in mbti_values["Ratio"]
        ],
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.2%}<extra></extra>"
    )
)

fig.update_layout(
    title=f"{country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    height=650,
    hovermode="x unified",
    font=dict(size=16),
    title_font=dict(size=26),
    xaxis=dict(
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        tickformat=".0%",
        gridcolor="rgba(200,200,200,0.2)"
    ),
    margin=dict(t=80, l=40, r=40, b=40)
)

# -----------------------------
# 그래프 출력
# -----------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# TOP 3 표시
# -----------------------------
st.subheader("🏆 TOP 3 MBTI")

top3 = mbti_values.head(3)

cols = st.columns(3)

for idx, (_, row) in enumerate(top3.iterrows()):
    with cols[idx]:
        st.metric(
            label=row["MBTI"],
            value=f"{row['Ratio']*100:.2f}%"
        )

# -----------------------------
# 데이터 테이블
# -----------------------------
with st.expander("데이터 보기"):
    st.dataframe(
        mbti_values,
        use_container_width=True
    )
