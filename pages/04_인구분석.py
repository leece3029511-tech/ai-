import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="서울시 행정구별 인구수",
    layout="wide"
)

# ---------------------------
# 데이터 불러오기
# ---------------------------
df = pd.read_csv("papulation.csv", encoding="utf-8")

# ---------------------------
# 컬럼 이름 정리
# ---------------------------
df.columns = df.columns.str.strip()

# ---------------------------
# 연령 컬럼 찾기
# ---------------------------
age_columns = [
    col for col in df.columns
    if "세" in col and "계" not in col
]

# ---------------------------
# 행정구 컬럼 찾기
# ---------------------------
district_col = df.columns[0]

# ---------------------------
# Streamlit 제목
# ---------------------------
st.title("서울시 행정구별 인구수")

# ---------------------------
# 행정구 선택
# ---------------------------
district_list = df[district_col].tolist()

selected_district = st.selectbox(
    "행정구 선택",
    district_list
)

# ---------------------------
# 선택한 행정구 데이터
# ---------------------------
selected_row = df[df[district_col] == selected_district].iloc[0]

# 숫자형 변환
population_values = []

for col in age_columns:
    value = str(selected_row[col]).replace(",", "")
    population_values.append(int(value))

# x축 이름 정리
x_labels = [col.replace("세", "") for col in age_columns]

# ---------------------------
# Plotly 그래프
# ---------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x_labels,
        y=population_values,
        mode="lines+markers",
        line=dict(color="white", width=3),
        marker=dict(color="white", size=6)
    )
)

# ---------------------------
# 그래프 스타일
# ---------------------------
fig.update_layout(
    title="서울시 행정구별 인구수",
    plot_bgcolor="#2b2b2b",
    paper_bgcolor="#2b2b2b",
    font=dict(
        color="white",
        family="Malgun Gothic"
    ),
    xaxis=dict(
        title="나이",
        showgrid=False
    ),
    yaxis=dict(
        title="인구수",
        gridcolor="gray"
    ),
    height=600
)

# ---------------------------
# 그래프 출력
# ---------------------------
st.plotly_chart(fig, use_container_width=True)
