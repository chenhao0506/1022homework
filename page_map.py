import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import leafmap.foliumap as leafmap 
import folium 

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (向量)")

# --- 選擇底圖 ---
with st.sidebar:
    st.header("地圖設定")
    option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 1. 讀取 JSON 檔案 ---
url = "路外停車資訊.json"

try:
    df = pd.read_json(url)
    
    st.subheader("資料預覽 (表格)")
    st.dataframe(df.head())

except Exception as e:
    st.error(f"⚠️ 檔案讀取失敗，請確認 '{url}' 檔案是否存在。錯誤訊息: {e}")
    st.stop()


# --- 2. 將經緯度轉成 geometry ---
try:
    df["wgsX"] = pd.to_numeric(df["wgsX"], errors='coerce') 
    df["wgsY"] = pd.to_numeric(df["wgsY"], errors='coerce') 
    
    df.dropna(subset=['wgsX', 'wgsY'], inplace=True)

    geometry = [Point(xy) for xy in zip(df["wgsY"], df["wgsX"])] 
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    if gdf.empty:
        st.warning("⚠️ GeoDataFrame (gdf) 為空！請檢查原始 JSON 檔案中是否有有效的 'wgsX' 和 'wgsY' 數值。")
        st.stop()
        
    st.info(f"✅ GeoDataFrame 成功建立，包含 {len(gdf)} 個有效點位。")

except Exception as e:
    st.error(f"⚠️ 經緯度轉換失敗。錯誤訊息: {e}")
    st.stop()


# --- 3. 建立地圖 ---
m = leafmap.Map(center=[0, 0])
m.add_basemap(option)

# --- 4. 將 GeoDataFrame 加到地圖 (使用 m.add_gdf) ---
m.add_gdf(
    gdf,
    layer_name="路外停車資訊",
    # 設置標記的樣式
    marker_kwds={
        "radius": 6, 
        "color": "#007BFF", 
        "fill": True, 
        "fillColor": "#007BFF", 
        "fillOpacity": 0.8
    },
)

# 顯示圖層控制項
m.add_layer_control()

# --- 5. 顯示地圖 ---
m.to_streamlit(height=700) 