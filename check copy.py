import csv
import pandas as pd
import folium
import math
from datetime import datetime
import scipy.integrate as spi
import matplotlib.pyplot as plt

filename = './Input/4.csv'
outputfile = './Result/map_data4_1.csv'
outputfile1 = './Result/map_data4_2.csv'
mapsave = './Map/mapcopy1.html'
#-----------------------------------------------------------------------------------------------------------------------------------
#Hàm tính tổng quãng đường
def haversine(lat1,lon1,lat2,lon2):
    R = 6371e3 #Bán kinh trái đất
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    deltaφ = φ2 - φ1
    deltaλ = math.radians(lon2 - lon1)
    
    a = math.sin(deltaφ / 2) * math.sin(deltaφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(deltaλ / 2) * math.sin(deltaλ / 2)
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    return R * c
#Hàm tính vận tốc
def calculate_velocity(s,t1,t2):
    velocity = s/(t2-t1)
    
    return velocity

def interpolate_points(lat1,lon1,lat2,lon2,num_points):
    d = math.sqrt( (lat2-lat1)**2 + (lon2-lon1)**2 )
    interpolation_distance = d/(num_points+1)
    lat_i = []
    lon_i = []
    for i in range (1,num_points+1):
        lat = lat1 + (lat2-lat1) * (i*interpolation_distance/d)
        lat_i.append(lat)
        lon = lon1 + (lon2-lon1) * (i*interpolation_distance/d)
        lon_i.append(lon)
    return lat_i, lon_i
#Hàm tính IRI
def calculate_IRI(av, t1, t2):
    az = abs(av / 1)
    b = t2 - t1
    # Tính vận tốc
    velocity = az * b
    # Tính quãng đường
    Vh = spi.quad(lambda t: velocity, 0, b)[0]
        
    return Vh
#-----------------------------------------------------------------------------------------------------------------------------------

# Lấy dữ liệu
data = pd.read_csv(filename)

column_names = data.columns.tolist()  # Lấy danh sách tên cột

latitude = data.loc[(data[column_names[1]] == 'Latitude:'), column_names[2]].astype(float).tolist()
longitude = data.loc[(data[column_names[1]] == 'Longitude:'), column_names[2]].astype(float).tolist()
time = data.loc[(data[column_names[1]] == 'Latitude:'), column_names[0]].tolist()
time_list = []
for index, row in data.iterrows():
    column_name = row[column_names[1]]                
    if column_name == 'Latitude:':
        time_string = row[column_names[0]]
        datetime_object = datetime.strptime(time_string, "%m/%d/%Y %H:%M:%S.%f")
        time_stamp = datetime_object.timestamp()
        time_list.append(float(time_stamp))

ax = data.loc[data[column_names[1]] == 'Acc', column_names[2]].astype(float).tolist()
ay = data.loc[data[column_names[1]] == 'Acc', column_names[3]].astype(float).tolist()
az = data.loc[data[column_names[1]] == 'Acc', column_names[4]].astype(float).tolist()             
    #-----------------------------------------------------------------------------------------------------------------------
#Tính vận tốc và tổng quãng đường
total_distance = 0
num_points = 0
distances = []
velocity_list = []
starttime = time_list[0]
lat_i = []
lon_i = []
lat = []
lon = []
lat1 = []
lon1 = []
lat2 = []
lon2 = []
L=1.4
t_th = []
start_time = []
IRI = []
Vh = []
Vh_values = []

#Nội suy các điểm tọa độ 
for i in range(len(latitude) - 1):
    if latitude[i] == latitude[i + 1] and longitude[i] == longitude[i + 1]:
        if i == 0:
            num_points += 1
            lat.append(latitude[0])
            lon.append(longitude[0])
        else:   
            num_points += 1
    else:
        lat_i, lon_i = interpolate_points(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1],  num_points)
        
        for j in range(len(lat_i)):
            lat.append(round(lat_i[j], 8))
            lon.append(round(lon_i[j], 8))
        lat.append(latitude[i+1])
        lon.append(longitude[i+1])
        num_points = 0

#Tính quãng đường và vận tốc
for i in range(len(lat)-1):
    distance = haversine(lat[i], lon[i], lat[i+1], lon[i+1])
    distances.append(distance)
    index = calculate_IRI(az[i], time_list[i], time_list[i+1])
    Vh.append(index)
    velocity = 3.6 * calculate_velocity(distances[i], time_list[i], time_list[i+1])                      
    velocity_list.append(velocity)        
    starttime = time_list[i+1]       
    t_th.append(L * 3.6 / velocity_list[i])   
index = calculate_IRI(az[i], time_list[i], time_list[i+1])
Vh.append(index) 
distance = haversine(lat[i], lon[i], lat[i+1], lon[i+1])
distances.append(distance)
velocity_list.append(velocity_list[i-1])  
t_th.append(L * 3.6 / velocity_list[i])
total_distance = sum(distances)/1000
print(f"S: {total_distance}")

s = 0
s_th = 100
vh_sum = 0
distance_segments = []
v_segments = []
v_values = []
for i in range(len(lat)):    
    if s < 100:
        if i == 0:
            lt = lat[0]
            ln = lon[0]
            s += distances[i]
            Vh_values.append(Vh[i]) 
            v_values.append(velocity_list[i])
        else:            
            s += distances[i]
            Vh_values.append(Vh[i]) 
            lt1 = lat[i]
            ln1 = lon[i]
            v_values.append(velocity_list[i])
    else:
        distance_segments.append(s)
        avg_vh = sum(Vh_values)
        id = avg_vh/(s_th*s_th/1000)
        IRI.append(id)
        v_segments.append(sum(v_values)/len(v_values))
        lat1.append(lt)
        lon1.append(ln)
        lat2.append(lt1)
        lon2.append(ln1)
        s = distances[i]
        lt = lat[i]
        ln = lon[i]
        Vh_values = []
        Vh_values.append(Vh[i])
        v_values = []
        v_values.append(velocity_list[i])
# distance_segments.append(s)
# avg_vh = sum(Vh_values)
# id = avg_vh/(s*(s/1000))
# IRI.append(id)
# v_segments.append(sum(v_values)/len(v_values))
# lat1.append(lt)
# lon1.append(ln)
# lat2.append(lat[i])
# lon2.append(lon[i])

#Phát hiện pothole
ts = []
te = []  
lat3 = []
lon3 = [] 
av_th = 17
s, e, lt, ln = 0, 0, 0, 0
i=0
while i < len(lat):
    if az[i] >= av_th:     
        lt = lat[i]
        ln = lon [i]
        s = time_list[i]
        e = s
        i += 1
        while i < len(lat):
            if az[i] < av_th:
                i += 1
            else:
                if time_list[i] - e < t_th[i]:
                    e = time_list[i]
                    i += 1
                else:
                    if time_list[i] - s < t_th[i]:
                        i -= 1                  
                    else:
                        lat3.append(lt)
                        lon3.append(ln)
                        ts.append(s)
                        te.append(time_list[i])
                        i += 1
                    break
        if i == len(lat) - 1:
            if time_list[i] - s >= t_th[i]:
                lat3.append(lt)
                lon3.append(ln)
                ts.append(s)
                te.append(time_list[i])
                s = 0
    else:
        i += 1
#----------------------------------------------------------------------------------------------------------------------------
#Vẽ bản đồ
for i in range(len(latitude)):
    if i < len(longitude):
        m = folium.Map(location=[latitude[0], longitude[0]], zoom_start=18, control_scale=True)        

# Thêm lớp bản đồ đất liền
tile_layer_land = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    name='Land Map',
    attr='Map data &copy; Google',
    min_zoom=0,
    max_zoom=22
).add_to(m)

# Thêm lớp bản đồ vệ tinh
tile_layer_satellite = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    name='Satellite Map',
    attr='Map data &copy; Google',
    min_zoom=0,
    max_zoom=22
).add_to(m)   

for i in range(len(lat1)):
    start = lat.index(lat1[i])
    end = lat.index(lat2[i], start + 1) + 1 if lat2[i] in lat[start + 1:] else len(lat)
    if v_segments[i] < 10:
        if IRI[i] < 17.99:
            color = 'yellowgreen'
        elif 18 <= IRI[i] < 32.32:
            color = 'yellow'
        elif IRI[i] > 32.32:
            color = 'red'            
    elif 10 <= v_segments[i] < 20:
        if IRI[i] < 8.99:
            color = 'yellowgreen'
        elif 9 <= IRI[i] < 16.16:
            color = 'yellow'
        elif IRI[i] > 16.16:
            color = 'red'
    elif 20 <= v_segments[i] < 30:
        if IRI[i] < 5.99:
            color = 'yellowgreen'
        elif 6 <= IRI[i] < 10.8:
            color = 'yellow'
        elif IRI[i] > 10.8:
            color = 'red'
    elif 30 <= v_segments[i] < 40:
        if IRI[i] < 4.49:
            color = 'yellowgreen'
        elif 4.5 <= IRI[i] < 8.08:
            color = 'yellow'
        elif IRI[i] > 8.08:
            color = 'red'
    elif 40 <= v_segments[i] < 50:
        if IRI[i] < 3.59:
            color = 'yellowgreen'
        elif 3.6 <= IRI[i] < 6.25:
            color = 'yellow'
        elif IRI[i] > 6.25:
            color = 'red'
    
    for k in range(start, end):
        marker = folium.CircleMarker(location=[lat[k], lon[k]], radius=1, color=color)
         # Tạo popup vị trí
        popup_content = f"Latitude: {lat[i]}<br>Longitude: {lon[i]}"
        popup = folium.Popup(popup_content, max_width=200)
        
        # Thêm popup vào marker
        marker.add_child(popup)
        
        # Thêm marker vào bản đồ
        marker.add_to(m)
        

for i in range(len(lat3)): 
    line =  folium.CircleMarker(location=[lat3[i], lon3[i]], radius=1, color='black')
    popup_content = f"Latitude: {lat3[i]}<br>Longitude: {lon3[i]}<br>Time_start: {ts[i]}<br>Time_end: {te[i]}"
    popup = folium.Popup(popup_content, max_width=200)
    line.add_child(popup)  
    line.add_to(m)
  
    
folium.LayerControl().add_to(m)
# Thiết lập lớp bản đồ đất liền là lớp mặc định
m.add_child(tile_layer_satellite)
# Thêm popup vào bản đồ
m.save(mapsave)                                    
    
with open(outputfile, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Time','Latitude', 'Longitude','az','s','v','IRI'])  # Ghi dòng tiêu đề
    for i in range(len(lat)):
        writer.writerow([time_list[i],lat[i], lon[i], az[i],distances[i],velocity_list[i],Vh[i]])
with open(outputfile1, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Latitude', 'Longitude','Latitude', 'Longitude','s','v','IRI'])  # Ghi dòng tiêu đề
    for i in range(len(lat1)):
        writer.writerow([lat1[i], lon1[i],lat2[i], lon2[i],distance_segments[i],v_segments[i],IRI[i]])

