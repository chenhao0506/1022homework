import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd # 引入 GeoPandas

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (向量)")

# --- 1. 用 GeoPandas 讀取資料 ---
# 這是 Natural Earth 110m cultural vectors 的官方託管 .zip 檔案連結
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

# GeoPandas 可以直接從 URL 讀取 .zip 檔
gdf = gpd.read_file(url)

# (選用) 驗證是否成功
st.dataframe(gdf.head())

# --- 2. 建立地圖 ---
m = leafmap.Map(center=[0, 0])

# --- 3. 將GeoDataFrame加入地圖 ---
# 使用 add_gdf()方法
m.add_gdf(
gdf,
layer_name="地圖國界(Vector)",
style={"fillOpacity": 0, "color": "black", "weight": 0.5}, # 設為透明，只留邊界}
# highlight=False 會關閉滑鼠懸停時的反白效果，
# 並「同時」阻止工具提示(Tooltip)的觸發
highlight=False
)
# 加入圖層控制器(右上角)
m.add_layer_control()

# --- 4. 顯示地圖 ---
m.to_streamlit(height=700)