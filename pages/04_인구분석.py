import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 행정구별 인구수", layout="wide")

# -----------------------------
# CSV 읽기 (인코딩 오류 해결)
# -----------------------------
try:
    df = pd.read_csv("papulation.csv", encoding="cp949")
except:
    df = pd.read_csv("papulation.csv", encoding="euc-kr")

# -----------------------------
# 컬럼 공백 제거
# -----------------------------
df.columns = [col.strip() for col in df.columns]

# 행정구 컬럼
district_col = df.columns[0]

# 숫자형 변환
for col in df.columns[1:]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# 연령대 컬럼 추출
# -----------------------------
age_columns = []

for col in df.columns:
    if "~" in col and "계" not in col:
        age_columns.append(col)

# -----------------------------
# 제목
# -----------------------------
st.title("서울시 행정구별 인구수")

# -----------------------------
# 행정구 선택
# -----------------------------
districts = df[district_col].tolist()

selected_district = st.selectbox(
    "행정구 선택",
    districts
)

selected_row = df[df[district_col] == selected_district].iloc[0]

# 그래프 데이터
x = age_columns
y = [selected_row[col] for col in age_columns]

# -----------------------------
# 꺾은선 그래프
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        line=dict(color="white", width=3),
        marker=dict(color="white", size=7),
        name=selected_district
    )
)

fig.update_layout(
    title="서울시 행정구별 인구수",
    paper_bgcolor="#2b2b2b",
    plot_bgcolor="#2b2b2b",
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

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 연령대별 TOP10
# =====================================================

st.divider()

st.subheader("연령대별 인구 TOP10 행정구")

selected_age = st.selectbox(
    "10살 간격 연령대 선택",
    age_columns
)

top10 = df[[district_col, selected_age]].sort_values(
    by=selected_age,
    ascending=False
).head(10)

fig2 = go.Figure()

for _, row in top10.iterrows():

    fig2.add_trace(
        go.Scatter(
            x=[selected_age],
            y=[row[selected_age]],
            mode="lines+markers",
            name=row[district_col]
        )
    )

fig2.update_layout(
    title=f"{selected_age} 인구 TOP10 행정구",
    paper_bgcolor="#2b2b2b",
    plot_bgcolor="#2b2b2b",
    font=dict(
        color="white",
        family="Malgun Gothic"
    ),
    xaxis=dict(
        title="나이대",
        showgrid=False
    ),
    yaxis=dict(
        title="인구수",
        gridcolor="gray"
    ),
    height=700
)

st.plotly_chart(fig2, use_container_width=True)
