import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
# 使用 leafmap.foliumap 讓 Streamlit 正確渲染
import leafmap.foliumap as leafmap 
# 雖然不再直接使用，但保留以利未來擴充
import folium 

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (向量)")

# --- 選擇底圖 ---
option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 1. 讀取 JSON 檔案（非 GeoJSON） ---
url = "路外停車資訊.json"

try:
    df = pd.read_json(url)
except Exception as e:
    st.error(f"⚠️ 檔案讀取失敗，請確認 '{url}' 檔案是否存在於應用程式同目錄。錯誤訊息: {e}")
    st.stop()


# 檢查資料
st.subheader("資料預覽 (表格)")
st.dataframe(df.head())

# --- 2. 將經緯度轉成 geometry ---
try:
    df["wgsX"] = df["wgsX"].astype(float)
    df["wgsY"] = df["wgsY"].astype(float)
    geometry = [Point(xy) for xy in zip(df["wgsX"], df["wgsY"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    # ⭐ 偵錯點 1：檢查 GeoDataFrame 是否有資料
    if gdf.empty:
        st.warning("⚠️ GeoDataFrame (gdf) 為空！請檢查原始 JSON 檔案中是否有 'wgsX' 和 'wgsY' 欄位。")
        st.stop()
        
    st.info(f"✅ GeoDataFrame 成功建立，包含 {len(gdf)} 個點位。")

except Exception as e:
    st.error(f"⚠️ 經緯度轉換失敗，請檢查 'wgsX' 和 'wgsY' 欄位的資料格式。錯誤訊息: {e}")
    st.stop()


# --- 3. 建立地圖 ---
# 將中心點設為所有點的平均值，讓地圖可以自動縮放到點位
center_lat = gdf["wgsY"].mean() if not gdf.empty else 23.5
center_lon = gdf["wgsX"].mean() if not gdf.empty else 121

m = leafmap.Map(center=[center_lat, center_lon], zoom=10, basemap=option)

# --- 4. 將 GeoDataFrame 加到地圖 (使用 m.add_gdf 確保穩定性) ---
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

# --- 5. 顯示地圖 ---
st.subheader("Leafmap 地圖顯示")
m.to_streamlit(height=700)