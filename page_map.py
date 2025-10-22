import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (向量)")

# --- 選擇底圖 ---
option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 1. 讀取 JSON 檔案 ---
url = "路外停車資訊.json"
df = pd.read_json(url)

# 檢查資料
st.dataframe(df.head())

# --- 2. 將經緯度轉成 geometry ---
# 注意 wgsX 是經度，wgsY 是緯度
df["wgsX"] = df["wgsX"].astype(float)
df["wgsY"] = df["wgsY"].astype(float)
geometry = [Point(xy) for xy in zip(df["wgsX"], df["wgsY"])]

gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# --- 3. 建立地圖 ---
m = leafmap.Map(center=[23.5, 121], zoom=8, basemap=option)

# --- 4. 加入地圖 ---
m.add_gdf(
    gdf,
    layer_name="路外停車資訊",
    style={"fillOpacity": 0.8, "color": "blue", "weight": 1},
    popup=["parkName", "address", "totalSpace", "payGuide"]
)
m.add_layer_control()

# --- 5. 顯示地圖 ---
m.to_streamlit(height=700)
