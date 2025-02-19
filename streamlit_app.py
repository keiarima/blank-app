import streamlit as st
import folium
import json
import subprocess
import os
from folium import Icon
from streamlit_folium import st_folium

# **フォルダの作成**
if not os.path.exists("data"):
    os.makedirs("data")

# **GeoJSONのファイルパス**
geojson_path = "data/meiji_jingu_trees.geojson"

# **ファイルがない場合、自動生成**
if not os.path.exists(geojson_path):
    st.warning("🌱 植生データがありません。生成中...")
    subprocess.run(["python", "utils/geojson_generator.py"], check=True)
    st.success("✅ 植生データを作成しました！")

# **Streamlitのレイアウトをフルスクリーンに設定**
st.set_page_config(layout="wide")

# **CSSで地図のサイズを最大化**
st.markdown(
    """
    <style>
    .full-screen-map {
        height: 90vh !important;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# **Streamlit タイトル**
st.title("🌳 明治神宮 植生マップ")

# **植生データのランダム生成ボタン**
if st.button("🌿 植生をランダムに変更"):
    subprocess.run(["python", "utils/geojson_generator.py"], check=True)
    st.success("🌿 植生がランダムに配置されました！")
    
    # **最新のデータを再読み込み**
    with open(geojson_path, "r", encoding="utf-8") as file:
        st.session_state["geojson_data"] = json.load(file)

    # **ページを再読み込み**
    st.rerun()  # ✅ 修正: `st.experimental_rerun()` → `st.rerun()`

# **📥 GeoJSON ダウンロードボタン**
if "geojson_data" not in st.session_state:
    with open(geojson_path, "r", encoding="utf-8") as file:
        st.session_state["geojson_data"] = json.load(file)

geojson_str = json.dumps(st.session_state["geojson_data"], indent=4)
st.download_button(
    label="📂 GeoJSON をダウンロード",
    data=geojson_str,
    file_name="meiji_jingu_trees.geojson",
    mime="application/json"
)

# **🌍 Folium マップ作成**
m = folium.Map(location=[35.675, 139.698], zoom_start=15)

# **🌱 敷地のPolygonを表示**
folium.GeoJson(
    st.session_state["geojson_data"],
    name="Meiji Jingu Area",
    tooltip=None,
    popup=None,
    show=False,
).add_to(m)

# **🌲 木のアイコンを表示（FontAwesomeのTreeアイコンを使用）**
for feature in st.session_state["geojson_data"]["features"]:
    if feature["geometry"]["type"] == "Point":
        lon, lat = feature["geometry"]["coordinates"]
        tree_type = feature["properties"]["tree_type"]

        # **木の種類ごとのアイコン色を設定**
        icon_color = "green" if tree_type == "oak" else "darkgreen"

        # **ポップアップ情報**
        popup_text = f"🌳 <b>樹種:</b> {tree_type.capitalize()}<br>📍 <b>緯度:</b> {lat:.6f}<br>📍 <b>経度:</b> {lon:.6f}"

        # **アイコンをマップに追加**
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=300),  # **クリックで樹種と座標を表示**
            icon=Icon(icon="tree", prefix="fa", color=icon_color)
        ).add_to(m)

# **🌍 地図を全画面表示（高さ 90vh を設定）**
st_folium(m, width=1000, height=700)