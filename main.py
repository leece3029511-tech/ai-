import streamlit as st
st.title('나의 첫 웹서브스 만들기!')
a=st.text_input('이름을 입력해주새요!')
b=st.selectbox('좋아하는 축구선수를 선택해주세요!',['호날두','메시','네이마르','그리즈만','호나우지뉴','호나우두','펠레','마라도나'])
if st.button('인사말 생성'):
 st.write(a+'님!,안녕하세요,반갑습니다!')
st.write(a+'님! 안녕하세요!)
st.info('반갑습니다.')
st.warning(b+'음식을 좋아하는군요.')
st.error('자 부탁드려요.')
