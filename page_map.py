import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd # 引入 GeoPandas

option = st.selectbox("請選擇底圖",("OpenTopoMap","Esri.EorldImagery","CartoDB.DarkMatter"))

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (向量)")

# --- 1. 用 GeoPandas 讀取資料 ---
url = "路外停車資訊.json"

# GeoPandas 可以直接從 URL 讀取 .json 檔
gdf = gpd.read_file(url)

# (選用) 驗證是否成功
st.dataframe(gdf())

# --- 2. 建立地圖 ---
m = leafmap.Map(center=[0, 0])

# --- 3. 將GeoDataFrame加入地圖 ---
# 使用 add_gdf()方法
m.add_gdf(
gdf,
layer_name="路外停車資訊",
style={"fillOpacity": 0, "color": "black", "weight": 0.5}, # 設為透明，只留邊界}
highlight=False
)
# 加入圖層控制器(右上角)
m.add_layer_control()

# --- 4. 顯示地圖 ---
m.to_streamlit(height=700)