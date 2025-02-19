import streamlit as st
import folium
import json
from streamlit_folium import folium_static

# タイトル
st.title("GeoJSON 植生マップ 🌳")

# GeoJSONの読み込み
geojson_path = "data/trees.geojson"
with open(geojson_path, "r", encoding="utf-8") as file:
    geojson_data = json.load(file)

# マップの作成
m = folium.Map(location=[35.675, 139.698], zoom_start=15)

# Polygon（植生エリア）を描画
folium.GeoJson(geojson_data, name="Polygon").add_to(m)

# 各木のアイコンを追加（色つき）
for feature in geojson_data["features"]:
    if feature["geometry"]["type"] == "Point":
        lon, lat = feature["geometry"]["coordinates"]
        tree_type = feature["properties"]["tree_type"]

        # 木の種類ごとの色設定
        icon_color = "green" if tree_type == "oak" else "darkred"

        # マーカーを追加（色つき）
        folium.Marker(
            location=[lat, lon],
            popup=f"Type: {tree_type}",
            icon=folium.Icon(color=icon_color, icon="tree")
        ).add_to(m)

# Streamlit上にFoliumマップを表示
folium_static(m)