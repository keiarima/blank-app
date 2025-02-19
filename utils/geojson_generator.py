import json
import random
import os
from shapely.geometry import Polygon, Point

# **フォルダを作成**
output_dir = "data"
output_file = os.path.join(output_dir, "meiji_jingu_trees.geojson")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# **明治神宮の敷地（Polygon）**
polygon_coords = [
    (139.6950, 35.6782), (139.6953, 35.6752), (139.6954, 35.6745), (139.6974, 35.6720),
    (139.6983, 35.6715), (139.7000, 35.6710), (139.7008, 35.6697), (139.7016, 35.6691),
    (139.7020, 35.6693), (139.7020, 35.6696), (139.7022, 35.6699), (139.7023, 35.6707),
    (139.7027, 35.6722), (139.7038, 35.6753), (139.7038, 35.6758), (139.7036, 35.6784),
    (139.7030, 35.6789), (139.7010, 35.6799), (139.7005, 35.6799), (139.6990, 35.6807),
    (139.6986, 35.6808), (139.6980, 35.6808), (139.6974, 35.6807), (139.6970, 35.6804),
    (139.6965, 35.6801), (139.6962, 35.6799), (139.6957, 35.6797), (139.6950, 35.6782)
]
polygon = Polygon(polygon_coords)

# **GeoJSONデータの初期化**
geojson_data = {"type": "FeatureCollection", "features": []}

# **Polygonデータ（敷地）を追加**
geojson_data["features"].append({
    "type": "Feature",
    "geometry": {"type": "Polygon", "coordinates": [polygon_coords]},
    "properties": {"name": "明治神宮"}
})

# **木の種類**
tree_types = [("oak", "green", 30), ("pine", "brown", 30)]

# **木をランダムに配置**
for tree_type, color, num_trees in tree_types:
    count = 0
    while count < num_trees:
        lon = random.uniform(min([p[0] for p in polygon_coords]), max([p[0] for p in polygon_coords]))
        lat = random.uniform(min([p[1] for p in polygon_coords]), max([p[1] for p in polygon_coords]))
        point = Point(lon, lat)

        if polygon.contains(point):
            geojson_data["features"].append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {"tree_type": tree_type, "icon_color": color}
            })
            count += 1

# **ファイルに保存**
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, indent=4)

print(f"✅ GeoJSONファイルを作成しました: {output_file}")