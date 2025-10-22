import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import leafmap.foliumap as leafmap 
import folium 

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (向量)")

# --- 選擇底圖 ---
option = st.selectbox("請選擇底圖", ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"))

# --- 1. 讀取 JSON 檔案（非 GeoJSON） ---
url = "路外停車資訊.json"

try:
    df = pd.read_json(url)
    df_preview = df.head().copy() # 使用 .copy() 避免 SettingWithCopyWarning
    
    # ⭐ 確保經緯度是浮點數，以防讀取時仍是字串
    df_preview["wgsX"] = pd.to_numeric(df_preview["wgsX"], errors='coerce')
    df_preview["wgsY"] = pd.to_numeric(df_preview["wgsY"], errors='coerce')

    st.subheader("資料預覽 (表格)")
    st.dataframe(df_preview)

except Exception as e:
    st.error(f"⚠️ 檔案讀取失敗。錯誤訊息: {e}")
    st.stop()


# --- 2. 將經緯度轉成 geometry ---
try:
    # 強制轉換為浮點數，非數字的會變成 NaN
    df["wgsX"] = pd.to_numeric(df["wgsX"], errors='coerce') 
    df["wgsY"] = pd.to_numeric(df["wgsY"], errors='coerce') 
    
    # 移除任何經緯度為 NaN 的列
    df.dropna(subset=['wgsX', 'wgsY'], inplace=True)

    # ❗ 修正關鍵：JSON中 wgsY 是經度(x)，wgsX 是緯度(y)。
    #    GeoPandas/Shapely 需要 Point(Longitude, Latitude)
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
# 自動計算中心點和縮放級別
center_lat = gdf.geometry.y.mean()
center_lon = gdf.geometry.x.mean()

m = leafmap.Map(center=[center_lat, center_lon], zoom=12, basemap=option)


# --- 4. 將 GeoDataFrame 加到地圖 (使用 m.add_gdf 確保穩定性) ---
m.add_gdf(
    gdf,
    layer_name="路外停車資訊",
    # 設置標記的樣式
    marker_kwds={
        "radius": 6, 
        "color": "#007BFF", # 藍色
        "fill": True, 
        "fillColor": "#007BFF", 
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