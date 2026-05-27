import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("📈 서울 특정 날짜 기온 변화 분석")

# -----------------------------
# CSV 불러오기
# -----------------------------
try:
    df = pd.read_csv("seoul.csv", encoding="cp949")
except:
    try:
        df = pd.read_csv("seoul.csv", encoding="euc-kr")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8")

# -----------------------------
# 컬럼 공백 제거
# -----------------------------
df.columns = df.columns.str.strip()

# -----------------------------
# 날짜 변환 (오류 해결 핵심)
# -----------------------------
df['날짜'] = pd.to_datetime(
    df['날짜'],
    errors='coerce'
)

# 날짜 변환 실패한 행 제거
df = df.dropna(subset=['날짜'])

# -----------------------------
# 연/월/일 컬럼 생성
# -----------------------------
df['연도'] = df['날짜'].dt.year
df['월'] = df['날짜'].dt.month
df['일'] = df['날짜'].dt.day

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("날짜 선택")

selected_month = st.sidebar.selectbox(
    "월 선택",
    sorted(df['월'].unique())
)

selected_day = st.sidebar.selectbox(
    "일 선택",
    sorted(
        df[df['월'] == selected_month]['일'].unique()
    )
)

# -----------------------------
# 데이터 필터링
# -----------------------------
filtered_df = df[
    (df['월'] == selected_month) &
    (df['일'] == selected_day)
].copy()

# 결측치 제거
filtered_df = filtered_df.dropna(
    subset=['최고기온(℃)', '최저기온(℃)']
)

# -----------------------------
# 그래프 생성
# -----------------------------
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered_df['연도'],
        y=filtered_df['최고기온(℃)'],
        mode='lines+markers',
        name='최고기온',
        line=dict(color='red', width=3),
        marker=dict(size=6)
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered_df['연도'],
        y=filtered_df['최저기온(℃)'],
        mode='lines+markers',
        name='최저기온',
        line=dict(color='blue', width=3),
        marker=dict(size=6)
    )
)

# -----------------------------
# 그래프 레이아웃
# -----------------------------
fig.update_layout(
    title=f"{selected_month}월 {selected_day}일 서울 기온 변화",
    xaxis_title="연도",
    yaxis_title="기온 (℃)",
    hovermode="x unified",
    template="plotly_white",
    height=700
)

# -----------------------------
# 그래프 출력
# -----------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# 데이터 보기
# -----------------------------
with st.expander("데이터 보기"):
    st.dataframe(
        filtered_df[
            ['날짜', '최고기온(℃)', '최저기온(℃)']
        ].reset_index(drop=True),
        use_container_width=True
    )
