import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd  # 引入 GeoPandas

# --- 1. Streamlit 介面設定 ---
st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (向量)")

# --- 2. 選擇底圖 ---
option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 3. 讀取 GeoJSON ---
url = "路外停車資訊.json"  # 這裡要確定檔案路徑或上傳方式

# GeoPandas 可以直接讀取本地或 URL 的 GeoJSON 檔
gdf = gpd.read_file(url)

# (選用) 驗證是否成功
st.dataframe(gdf)  # ❌ 原本的 gdf() 是錯的，應該是 gdf

# --- 4. 建立地圖 ---
m = leafmap.Map(center=[0, 0], zoom=7, basemap=option)

# --- 5. 加入 GeoDataFrame ---
m.add_gdf(
    gdf,
    layer_name="路外停車資訊",
    style={"fillOpacity": 0, "color": "black", "weight": 0.5},
    highlight=False
)

# 加入圖層控制器
m.add_layer_control()

# --- 6. 顯示地圖 ---
m.to_streamlit(height=700)
