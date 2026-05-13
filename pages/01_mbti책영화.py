import streamlit as st

st.set_page_config(page_title="MBTI 책 & 영화 추천기", page_icon="📚")

st.title("📚🎬 MBTI 책 & 영화 추천기")
st.write("MBTI를 선택하면 어울리는 책 2권과 영화 2편을 추천해드립니다.")

recommendations = {
    "INTJ": {
        "books": ["사피엔스", "총, 균, 쇠"],
        "movies": ["인터스텔라", "셜록 홈즈"]
    },
    "INTP": {
        "books": ["코스모스", "이기적 유전자"],
        "movies": ["매트릭스", "이미테이션 게임"]
    },
    "ENTJ": {
        "books": ["린치핀", "성공하는 사람들의 7가지 습관"],
        "movies": ["아이언맨", "소셜 네트워크"]
    },
    "ENTP": {
        "books": ["넛지", "데미안"],
        "movies": ["인셉션", "레디 플레이어 원"]
    },
    "INFJ": {
        "books": ["어린 왕자", "죽은 시인의 사회"],
        "movies": ["코코", "굿 윌 헌팅"]
    },
    "INFP": {
        "books": ["미드나잇 라이브러리", "연금술사"],
        "movies": ["월터의 상상은 현실이 된다", "센과 치히로의 행방불명"]
    },
    "ENFJ": {
        "books": ["아몬드", "멋진 신세계"],
        "movies": ["업", "원더"]
    },
    "ENFP": {
        "books": ["해리포터", "모모"],
        "movies": ["라라랜드", "주토피아"]
    },
    "ISTJ": {
        "books": ["정의란 무엇인가", "팩트풀니스"],
        "movies": ["머니볼", "포레스트 검프"]
    },
    "ISFJ": {
        "books": ["나미야 잡화점의 기적", "완벽한 공부법"],
        "movies": ["리틀 포레스트", "인사이드 아웃"]
    },
    "ESTJ": {
        "books": ["그릿", "부자 아빠 가난한 아빠"],
        "movies": ["탑건", "킹스맨"]
    },
    "ESFJ": {
        "books": ["아주 작은 습관의 힘", "마당을 나온 암탉"],
        "movies": ["겨울왕국", "맘마미아"]
    },
    "ISTP": {
        "books": ["삼체", "해커와 화가"],
        "movies": ["존 윅", "마션"]
    },
    "ISFP": {
        "books": ["채식주의자", "달러구트 꿈 백화점"],
        "movies": ["비긴 어게인", "너의 이름은"]
    },
    "ESTP": {
        "books": ["트렌드 코리아", "아웃라이어"],
        "movies": ["분노의 질주", "베이비 드라이버"]
    },
    "ESFP": {
        "books": ["기분이 태도가 되지 않게", "완득이"],
        "movies": ["알라딘", "위대한 쇼맨"]
    }
}

mbti_list = list(recommendations.keys())
selected_mbti = st.selectbox("MBTI를 선택하세요", mbti_list)

if st.button("추천 보기"):
    data = recommendations[selected_mbti]

    st.subheader(f"✨ {selected_mbti} 추천 결과")

    st.markdown("## 📚 추천 책")
    for idx, book in enumerate(data["books"], start=1):
        st.write(f"{idx}. {book}")

    st.markdown("## 🎬 추천 영화")
    for idx, movie in enumerate(data["movies"], start=1):
        st.write(f"{idx}. {movie}")

st.markdown("---")
st.caption("MBTI 성향을 기반으로 한 재미용 추천입니다 😄")
