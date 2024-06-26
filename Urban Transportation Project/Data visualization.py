import pandas as pd
import folium

# 加载数据
data = pd.read_csv('urban_transport_network_stops.csv')

# 创建地图对象
mymap = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# 添加站点到地图
for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Stop ID: {row['stop_id']}<br>Name: {row['name']}<br>Zone Type: {row['zone_type']}"
    ).add_to(mymap)

# 保存地图
mymap.save('interactive_map.html')
