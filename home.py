import streamlit as st
st.title("范宸晧")
st.header("范宸晧的GIS專題 in 1022")
st.write("我是地理三的范宸晧，這個APP是用來...")

pages = [
    st.Page('page_map.py', title = '互動地圖瀏覽')
    st.Page('home.py', title = '關於我們'),
    ]

with st.sidebar:
    st.title("App 導覽")
    # st.navigation() 會回傳被選擇的頁面
    selected_page = st.navigation(pages)

selected_page.run()