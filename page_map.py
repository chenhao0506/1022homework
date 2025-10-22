import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
# 這裡使用 leafmap.foliumap 是正確的，因為您需要 Folium 後端
import leafmap.foliumap as leafmap 
import folium # 雖然不再直接使用 folium.GeoJsonPopup，但保留引入是好習慣

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (向量)")

# --- 選擇底圖 ---
option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 1. 讀取 JSON 檔案（非 GeoJSON） ---
# 假設 "路外停車資訊.json" 存在
url = "路外停車資訊.json"
df = pd.read_json(url)

# 檢查資料
st.dataframe(df.head())

# --- 2. 將經緯度轉成 geometry ---
df["wgsX"] = df["wgsX"].astype(float)
df["wgsY"] = df["wgsY"].astype(float)
geometry = [Point(xy) for xy in zip(df["wgsX"], df["wgsY"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# --- 3. 建立地圖 ---
m = leafmap.Map(center=[23.5, 121], zoom=8, basemap=option)

# --- 4. 建立 folium popup ---
# 這裡不再需要這個 Folium 物件

# --- 5. 將 GeoDataFrame 加到地圖 (使用 m.add_gdf) ---
m.add_gdf(
    gdf,
    layer_name="路外停車資訊",
    # 設置標記的樣式 (例如：圓形標記)
    marker_kwds={
        "radius": 5, 
        "color": "blue", 
        "fill": True, 
        "fillColor": "blue", 
        "fillOpacity": 0.8
    },
    # 傳遞欄位名稱列表給 popup
    popup=["parkName", "address", "totalSpace", "payGuide"],
    # 傳遞別名列表給 aliases
    aliases=["停車場名稱：", "地址：", "總車位：", "收費方式："]
)

m.add_layer_control()

# --- 6. 顯示地圖 ---
m.to_streamlit(height=700)