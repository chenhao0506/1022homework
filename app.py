import streamlit as st


pages = [
    st.Page('page_map.py', title = '互動地圖瀏覽'),
    st.Page('home.py', title = '關於我們')
    ]

with st.sidebar:
    st.title("App 導覽")
    # st.navigation() 會回傳被選擇的頁面
    selected_page = st.navigation(pages)

selected_page.run()