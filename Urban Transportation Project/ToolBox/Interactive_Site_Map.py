import pandas as pd
import folium

def add_map():
    # Load data加载数据
    stops_df = pd.read_csv("urban_transport_network_stops.csv")

    # Create a map centered at an average location以平均位置为中心创建地图
    m = folium.Map(location=[stops_df['latitude'].mean(), stops_df['longitude'].mean()], zoom_start=13)

    # Add stops to the map在地图上添加停靠点
    for _, row in stops_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Name: {row['name']}<br>Zone: {row['zone_type']}",
            tooltip=row['name']
        ).add_to(m)

    # Save the map to an HTML file将地图保存为 HTML 文件
    m.save("interactive_transport_network_map.html")
    print("interactive_transport.network_map.html has been successfully added!")