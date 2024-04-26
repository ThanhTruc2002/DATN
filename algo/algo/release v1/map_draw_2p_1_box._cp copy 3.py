import csv
import folium
import pandas as pd
import math
from geopy.distance import geodesic

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
# csv_file = './csv/4v2_22_2_24/4.csv'

# # Đọc dữ liệu từ tệp csv sử dụng pandas
# data = pd.read_csv(csv_file)

# time = data.iloc[:, 0].tolist()
# latitude = data.iloc[:, 1].tolist()
# longitude = data.iloc[:,2].tolist()
# ax = data.iloc[:, 3].tolist()
# ay = data.iloc[:, 4].tolist()
# az = data.iloc[:, 5].tolist()

csv_file = './algo/4.csv'

latitude = []
longitude = []
time = []
ax = []
ay = []
az = []

with open(csv_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)
    
    for row in reader:
        time.append(row[0])
        latitude.append(float(row[1]))
        longitude.append(float(row[2]))        
        ax.append(float(row[2]))
        ay.append(float(row[3]))
        az.append(float(row[4]))


num_intervals = 2
interval_shift = 1
roughness_values = []

# Tạo bản đồ
m = folium.Map(location=[latitude[0], longitude[0]], zoom_start=15)
total_distance = 0

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
    roughness_values.append(ri)
    roughness_average = sum(roughness_values) / len(ax)

    latitude_i = latitude[i]
    longitude_i = longitude[i]
    latitude_i_ = latitude[i-1]
    longitude_i_ = longitude[i-1]
    time_i = time[i]

    distance = geodesic((latitude_i, longitude_i), (latitude_i_, longitude_i_)).meters
    
    # Cộng dồn vào tổng quảng đường
    total_distance += distance

    popup_content = f"Roughness Index: {ri}<br>Time: {time_i}"  # Thêm thông tin thời gian vào popup
    
    df_ri = 2
    h_ri = 4 

    if  ri < df_ri:
        folium.CircleMarker(
            location=[latitude_i, longitude_i],
            radius=1,
            color='green',
            popup=popup_content
        ).add_to(m)
    

    if  df_ri <= ri < h_ri:
        folium.CircleMarker(
            location=[latitude_i, longitude_i],
            radius=1,
            color='blue',
            popup=popup_content
        ).add_to(m)
    if ri >= h_ri:
        folium.CircleMarker(
            location=[latitude_i, longitude_i],
            radius=1,
            color='red',
            popup=popup_content
        ).add_to(m)
# Lưu bản đồ vào tệp HTML
m.save('mapcopy3.html')