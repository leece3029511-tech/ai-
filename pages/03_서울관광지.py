import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP10",
    layout="wide"
)

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.write("관광지를 클릭하면 가까운 지하철역과 놀거리를 추천해줍니다.")

# 관광지 데이터
places = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "station": "경복궁역 (3호선)",
        "fun": ["한복 대여", "북촌 한옥마을 산책", "전통 카페 방문"]
    },
    {
        "name": "N서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "station": "명동역 (4호선)",
        "fun": ["야경 감상", "케이블카 타기", "커플 자물쇠 체험"]
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "station": "명동역 (4호선)",
        "fun": ["길거리 음식", "쇼핑", "K-뷰티 체험"]
    },
    {
        "name": "홍대거리",
        "lat": 37.5563,
        "lon": 126.9220,
        "station": "홍대입구역 (2호선)",
        "fun": ["버스킹 공연", "보드게임 카페", "감성 카페 탐방"]
    },
    {
        "name": "롯데월드타워",
        "lat": 37.513068,
        "lon": 127.102486,
        "station": "잠실역 (2호선)",
        "fun": ["서울스카이 전망대", "쇼핑몰", "롯데월드 방문"]
    },
    {
        "name": "북촌 한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "station": "안국역 (3호선)",
        "fun": ["전통 사진 촬영", "한옥 카페", "골목 산책"]
    },
    {
        "name": "DDP",
        "lat": 37.566526,
        "lon": 127.009223,
        "station": "동대문역사문화공원역 (2호선)",
        "fun": ["야경 사진", "전시회", "패션 쇼핑"]
    },
    {
        "name": "한강공원",
        "lat": 37.528726,
        "lon": 126.932243,
        "station": "여의나루역 (5호선)",
        "fun": ["치킨 먹기", "자전거 타기", "한강 피크닉"]
    },
    {
        "name": "코엑스",
        "lat": 37.5125,
        "lon": 127.0588,
        "station": "삼성역 (2호선)",
        "fun": ["별마당도서관", "아쿠아리움", "쇼핑"]
    },
    {
        "name": "익선동",
        "lat": 37.5740,
        "lon": 126.9895,
        "station": "종로3가역 (1·3·5호선)",
        "fun": ["감성 카페", "한옥 맛집", "사진 찍기"]
    }
]

# 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12
)

# 마커 추가
for place in places:

    popup_text = place["name"]

    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=popup_text,
        tooltip=place["name"],
        icon=folium.Icon(color="red")
    ).add_to(m)

# 지도 출력
map_data = st_folium(
    m,
    width=1200,
    height=600
)

st.divider()
st.subheader("📍 관광지 정보")

# 클릭 데이터 가져오기
clicked_data = map_data.get("last_object_clicked_tooltip")

if clicked_data:

    selected_place = None

    for place in places:
        if place["name"] == clicked_data:
            selected_place = place
            break

    if selected_place:

        st.markdown(f"## ✨ {selected_place['name']}")

        st.write(
            f"🚇 가까운 지하철역: {selected_place['station']}"
        )

        st.write("🎮 추천 놀거리")

        for activity in selected_place["fun"]:
            st.write(f"- {activity}")

else:
    st.info("지도에서 관광지를 클릭해보세요!")
