import streamlit as st

st.set_page_config(
    page_title="AI 바리스타 챗봇",
    page_icon="☕",
    layout="centered"
)

st.title("☕ AI 바리스타 챗봇")
st.write("커피에 대해 무엇이든 물어보세요!")

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("질문을 입력하세요")

# 응답 함수
def barista_bot(question):
    q = question.lower()

    if "아메리카노" in q:
        return """
☕ 아메리카노는 에스프레소에 물을 더한 커피입니다.

✔ 깔끔한 맛
✔ 낮은 칼로리
✔ 가장 인기 있는 커피 메뉴
"""

    elif "라떼" in q:
        return """
🥛 카페라떼는 에스프레소와 우유를 섞어 만든 음료입니다.

✔ 부드러운 맛
✔ 쓴맛이 적음
✔ 우유를 좋아하는 분께 추천
"""

    elif "추천" in q:
        return """
🌟 오늘의 추천 메뉴

1. 카페라떼
2. 바닐라라떼
3. 콜드브루

부드러운 맛을 좋아하면 라떼,
진한 커피를 좋아하면 아메리카노를 추천합니다.
"""

    elif "에스프레소" in q:
        return """
⚡ 에스프레소는 고압으로 추출한 진한 커피입니다.

✔ 강한 향
✔ 적은 양
✔ 카페인 집중
"""

    elif "카페인" in q:
        return """
☕ 카페인은 집중력 향상에 도움을 줄 수 있습니다.

하지만 과도한 섭취는 수면에 영향을 줄 수 있으므로 적당히 마시는 것이 좋습니다.
"""

    elif "안녕" in q or "hello" in q:
        return "안녕하세요! 저는 AI 바리스타입니다. ☕"

    else:
        return """
죄송해요. 아직 그 질문은 잘 모르겠어요.

예시 질문:
- 아메리카노 알려줘
- 라떼 설명해줘
- 커피 추천해줘
- 카페인이 뭐야?
"""

# 질문 처리
if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    answer = barista_bot(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
