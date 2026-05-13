import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천기", page_icon="💼")

st.title("💼 MBTI 진로 추천기")
st.write("MBTI를 선택하면 어울리는 진로 2가지를 추천해드립니다.")

career_data = {
    "INTJ": [
        {
            "career": "데이터 사이언티스트",
            "major": "컴퓨터공학과, 통계학과",
            "personality": "논리적이고 분석적인 사람",
            "salary": "평균 연봉 약 6,500만원"
        },
        {
            "career": "연구원",
            "major": "자연과학계열, 공학계열",
            "personality": "집중력이 높고 탐구심이 강한 사람",
            "salary": "평균 연봉 약 5,500만원"
        }
    ],
    "INTP": [
        {
            "career": "프로그래머",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "창의적이고 문제 해결을 좋아하는 사람",
            "salary": "평균 연봉 약 5,800만원"
        },
        {
            "career": "게임 개발자",
            "major": "게임공학과, 컴퓨터공학과",
            "personality": "아이디어가 많고 독창적인 사람",
            "salary": "평균 연봉 약 5,000만원"
        }
    ],
    "ENTJ": [
        {
            "career": "기업 경영인",
            "major": "경영학과",
            "personality": "리더십이 강하고 추진력이 있는 사람",
            "salary": "평균 연봉 약 7,000만원"
        },
        {
            "career": "마케팅 매니저",
            "major": "광고홍보학과, 경영학과",
            "personality": "전략적인 사고를 잘하는 사람",
            "salary": "평균 연봉 약 6,000만원"
        }
    ],
    "ENTP": [
        {
            "career": "기획자",
            "major": "경영학과, 미디어학과",
            "personality": "아이디어가 많고 도전을 좋아하는 사람",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "career": "창업가",
            "major": "경영학과",
            "personality": "모험심이 강하고 창의적인 사람",
            "salary": "평균 연봉 약 6,500만원"
        }
    ],
    "INFJ": [
        {
            "career": "상담사",
            "major": "심리학과",
            "personality": "공감 능력이 뛰어난 사람",
            "salary": "평균 연봉 약 4,500만원"
        },
        {
            "career": "작가",
            "major": "문예창작학과",
            "personality": "감수성이 풍부한 사람",
            "salary": "평균 연봉 약 4,000만원"
        }
    ],
    "INFP": [
        {
            "career": "디자이너",
            "major": "시각디자인학과",
            "personality": "창의적이고 감성적인 사람",
            "salary": "평균 연봉 약 4,800만원"
        },
        {
            "career": "웹툰 작가",
            "major": "애니메이션학과",
            "personality": "상상력이 풍부한 사람",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],
    "ENFJ": [
        {
            "career": "교사",
            "major": "교육학과",
            "personality": "사람을 이끄는 것을 좋아하는 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "career": "인사담당자",
            "major": "경영학과",
            "personality": "대인관계가 좋은 사람",
            "salary": "평균 연봉 약 5,500만원"
        }
    ],
    "ENFP": [
        {
            "career": "유튜버",
            "major": "미디어학과",
            "personality": "에너지가 넘치고 표현력이 좋은 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "career": "광고 기획자",
            "major": "광고홍보학과",
            "personality": "창의적이고 사교적인 사람",
            "salary": "평균 연봉 약 5,500만원"
        }
    ],
    "ISTJ": [
        {
            "career": "공무원",
            "major": "행정학과",
            "personality": "성실하고 책임감이 강한 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "career": "회계사",
            "major": "회계학과",
            "personality": "꼼꼼하고 계획적인 사람",
            "salary": "평균 연봉 약 7,000만원"
        }
    ],
    "ISFJ": [
        {
            "career": "간호사",
            "major": "간호학과",
            "personality": "배려심이 깊고 책임감 있는 사람",
            "salary": "평균 연봉 약 5,200만원"
        },
        {
            "career": "사회복지사",
            "major": "사회복지학과",
            "personality": "도움을 주는 것을 좋아하는 사람",
            "salary": "평균 연봉 약 4,000만원"
        }
    ],
    "ESTJ": [
        {
            "career": "경찰관",
            "major": "경찰행정학과",
            "personality": "책임감과 리더십이 강한 사람",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "career": "관리자",
            "major": "경영학과",
            "personality": "체계적이고 결단력 있는 사람",
            "salary": "평균 연봉 약 6,000만원"
        }
    ],
    "ESFJ": [
        {
            "career": "승무원",
            "major": "항공서비스학과",
            "personality": "친절하고 사교적인 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "career": "호텔리어",
            "major": "호텔관광학과",
            "personality": "서비스 정신이 뛰어난 사람",
            "salary": "평균 연봉 약 4,800만원"
        }
    ],
    "ISTP": [
        {
            "career": "엔지니어",
            "major": "기계공학과",
            "personality": "실용적이고 손재주가 좋은 사람",
            "salary": "평균 연봉 약 6,000만원"
        },
        {
            "career": "파일럿",
            "major": "항공운항학과",
            "personality": "침착하고 판단력이 좋은 사람",
            "salary": "평균 연봉 약 8,000만원"
        }
    ],
    "ISFP": [
        {
            "career": "플로리스트",
            "major": "원예학과",
            "personality": "감각적이고 섬세한 사람",
            "salary": "평균 연봉 약 3,800만원"
        },
        {
            "career": "패션 디자이너",
            "major": "패션디자인학과",
            "personality": "예술 감각이 뛰어난 사람",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],
    "ESTP": [
        {
            "career": "영업 전문가",
            "major": "경영학과",
            "personality": "활동적이고 말솜씨가 좋은 사람",
            "salary": "평균 연봉 약 5,500만원"
        },
        {
            "career": "스포츠 코치",
            "major": "체육학과",
            "personality": "에너지가 넘치고 행동력이 강한 사람",
            "salary": "평균 연봉 약 4,500만원"
        }
    ],
    "ESFP": [
        {
            "career": "배우",
            "major": "연극영화과",
            "personality": "표현력이 뛰어나고 밝은 사람",
            "salary": "평균 연봉 약 5,000만원"
        },
        {
            "career": "이벤트 플래너",
            "major": "관광경영학과",
            "personality": "사람들과 어울리는 것을 좋아하는 사람",
            "salary": "평균 연봉 약 4,500만원"
        }
    ]
}

mbti_list = list(career_data.keys())
selected_mbti = st.selectbox("MBTI를 선택하세요", mbti_list)

if st.button("진로 추천 보기"):
    st.subheader(f"✨ {selected_mbti} 추천 진로")

    for idx, item in enumerate(career_data[selected_mbti], start=1):
        st.markdown(f"---")
        st.markdown(f"### {idx}. {item['career']}")
        st.write(f"📚 적합한 학과: {item['major']}")
        st.write(f"😊 어울리는 성격: {item['personality']}")
        st.write(f"💰 {item['salary']}")

st.markdown("---")
st.caption("※ 연봉은 평균적인 예시이며 실제와 다를 수 있습니다.")

