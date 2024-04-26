import csv
import folium
import pandas as pd
import math

# Function to calculate acceleration changes  
def compute_acceleration_changes(ax, ay, az):
    acceleration_changes = []
    
    for i in range(1, len(ax)):
        delta_ax = (ax[i] - ax[i-1])**2 
        delta_ay = (ay[i] - ay[i-1])**2 
        delta_az = (az[i] - az[i-1])**2 
        
        acceleration_changes.append((delta_ax, delta_ay, delta_az))
    
    return acceleration_changes

# Function to calculate roughness index  
def compute_roughness_index(acceleration_changes):
    absolute_changes = [delta_ax + delta_ay + delta_az for delta_ax, delta_ay, delta_az in acceleration_changes]
    roughness_index = math.sqrt(sum(absolute_changes)) / (2 - 1)
    return roughness_index

# Đường dẫn tới tệp csv
csv_file = './csv/5v2_22_2_24/5.csv'

# Đọc dữ liệu từ tệp csv sử dụng pandas
data = pd.read_csv(csv_file)

ax = data.iloc[:, 4].tolist()
ay = data.iloc[:, 5].tolist()
az = data.iloc[:, 6].tolist()
latitude = data.iloc[:, 2].tolist()
longitude = data.iloc[:, 3].tolist()
time = data.iloc[:, 1].tolist()


num_intervals = 2
interval_shift = 1

# Tạo bản đồ
m = folium.Map(location=[latitude[0], longitude[0]], zoom_start=15)

tile_layer = folium.TileLayer(
    tiles='https://api.tomtom.com/map/1/tile/basic/main/{z}/{x}/{y}.png?key=sNkPGUd6uBwkm0fzLOUlsr5LKZQCQyh5',
    attr='© TomTom',  # Thông tin attribution của TomTom
    name='TomTom Satellite',
    min_zoom=0,
    max_zoom=22
).add_to(m)

tile_layer = folium.TileLayer(
    tiles='https://api.tomtom.com/map/1/tile/sat/main/{z}/{x}/{y}.jpg?key=sNkPGUd6uBwkm0fzLOUlsr5LKZQCQyh5',
    attr='© TomTom',
    name='TomTom Satellite',
    # overlay=True,
    # control=True,
    min_zoom=0,
    max_zoom=19
).add_to(m)

for i in range(len(ax) - num_intervals + interval_shift):
    sub_ax = ax[i:i+num_intervals]
    sub_ay = ay[i:i+num_intervals]
    sub_az = az[i:i+num_intervals]
    acceleration_changes = compute_acceleration_changes(sub_ax, sub_ay, sub_az)
    ri = compute_roughness_index(acceleration_changes)

    latitude_i = latitude[i]
    longitude_i = longitude[i]
    time_i = time[i]

    popup_content = f"Roughness Index: {ri}<br>Time: {time_i}"  # Thêm thông tin thời gian vào popup

    if ri < 2:
        folium.CircleMarker(
            location=[latitude_i, longitude_i],
            radius=1,
            color='green',
            popup=popup_content  # Gắn popup cho điểm
        ).add_to(m)
    elif ri >= 2:
        icon = folium.features.CustomIcon(icon_image='./img/bump.png', icon_size=(10, 10))
        folium.Marker(
            location=[latitude_i, longitude_i],
            icon=icon,
            popup=popup_content  # Gắn popup cho điểm
        ).add_to(m)

# Lưu bản đồ vào tệp HTML
m.save('map_2.html')