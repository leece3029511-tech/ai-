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
df = pd.read_csv("papulation.csv", encoding="cp949")

# ---------------------------
# 컬럼 공백 제거
# ---------------------------
df.columns = df.columns.str.strip()

# ---------------------------
# 행정구 컬럼
# ---------------------------
district_col = df.columns[0]

# ---------------------------
# 연령 컬럼 찾기
# ---------------------------
age_columns = []

for col in df.columns:
    if "세" in col and "계" not in col:
        age_columns.append(col)

# ---------------------------
# 제목
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
# 선택 데이터
# ---------------------------
selected_row = df[df[district_col] == selected_district].iloc[0]

# ---------------------------
# 데이터 변환
# ---------------------------
population_values = []

for col in age_columns:
    value = str(selected_row[col]).replace(",", "")
    population_values.append(int(value))

# x축 이름
x_labels = [col.replace("세", "") for col in age_columns]

# ---------------------------
# 그래프 생성
# ---------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x_labels,
        y=population_values,
        mode="lines+markers",
        line=dict(
            color="white",
            width=3
        ),
        marker=dict(
            color="white",
            size=6
        )
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
        family="Malgun Gothic",
        color="white"
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
# 출력
# ---------------------------
st.plotly_chart(fig, use_container_width=True)
