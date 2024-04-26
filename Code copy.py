import csv
import pandas as pd
import folium
import math
from datetime import datetime
import scipy.integrate as spi

filename = './Input/1.csv'
outputfile = './Result/map_data1.csv'
mapsave = './Map/mapcopy.html'

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

#Hàm tính IRI
def calculate_IRI(S,av, t1, t2):
    b = t2 - t1
    # Tính vận tốc
    velocity = av * b
    # Tính quãng đường
    delta_h = spi.quad(lambda t: velocity, 0, b)[0]
    index = delta_h  / S

    return index

#-----------------------------------------------------------------------------------------------------------------------------------
L=1.4
t_th = []
lat = []
lon = []  
start_time = []
av = []
av_values = []
av_list = []
distances = []
velocity_list = []
IRI = []
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
    
#Lọc dữ liệu
for i in range(len(latitude)):
    av.append(float(math.sqrt(ax[i]*ax[i] + ay[i]*ay[i] + az[i]*az[i])))
    if (latitude[i] == latitude[i-1] and longitude[i] == longitude[i-1]):
        av_values.append(av[i])
    elif (latitude[i] != latitude[i-1] or longitude[i] != longitude[i-1]):
        if i == 0:
            av_values.append(av[0])
            start_time.append(time_list[0]) 
        elif len(av_values) > 0 :
            avg_av = sum(av_values)/len(av_values) 
            start_time.append(time_list[i])              
            lat.append(latitude[i-1])
            lon.append(longitude[i-1]) 
            av_list.append(avg_av) 
            av_values = [] 
            av_values.append(av[i]) 
            
avg_av = sum(av_values)/len(av_values) 
start_time.append(time_list[i])  
lat.append(latitude[i-1])
lon.append(longitude[i-1]) 
av_list.append(avg_av) 

#Tính vận tốc và tổng quãng đường
total_distance = 0
for i in range(len(lat)-1):
    distance = haversine(lat[i], lon[i], lat[i+1], lon[i+1])
    distances.append(distance)
    velocity = 3.6 * calculate_velocity(distances[i], start_time[i], start_time[i+1])
    velocity_list.append(velocity)
    total_distance += distance

if len(lat) > 0:
    distance = haversine(lat[-2], lon[-2], lat[-1], lon[-1])
    distances.append(distance)
    velocity = 3.6 * calculate_velocity(distances[-1], start_time[-2], start_time[-1])
    velocity_list.append(velocity)
    total_distance += distance

total_distance /= 1000

for i in range(len(av_list)):
    index = calculate_IRI(total_distance, av_list[i], start_time[i], start_time[i+1])
    IRI.append(index)

print(f"S: {total_distance}")

#Xác định bump, pothole
for i in range(len(lat)):
    t_th.append(L * 3.6 / velocity_list[i])

lat1 = []
lon1 = []
ts = []
te = []
point1 = []
     
av_th = sum(av_list) / len(av_list)
# for i in range(len(lat)):    
#     s, e, lt, ln = None, None, None, None
#     if av_list[i] >= av_th:
#         s = float(start_time[i])
#         e = s
#         lt = lat[i]
#         ln = lon[i]
#         for j in range(i + 1, len(lat)):
#             if av_list[j] >= av_th:
#                 if start_time[j] - e < t_th[j]:
#                     e = float(start_time[j])
#                     j = i + 1
#                 else:
#                     if start_time[j] - s >= t_th[j]:
#                         lat1.append(lt)
#                         lon1.append(ln)
#                         ts.append(s)
#                         te.append(start_time[j])
#                         j -= 1
#                     else:
#                         j -= 1
#                     break
#         if i == len(lat) - 1:
#             if start_time[i] - s >= t_th[i]:
#                 lat1.append(lt)
#                 lon1.append(ln)
#                 ts.append(s)
#                 te.append(start_time[i])

for i in range(len(lat)):    
    s, e, lt, ln = None, None, None, None
    if av_list[i] >= av_th:
        s = float(start_time[i])
        e = s
        lt = lat[i]
        ln = lon[i]
        while (i) < len(lat):
            if av_list[i] < av_th:
                i += 1
            else:
                if start_time[i] - e < t_th[i]:
                    e = float(start_time[i])
                    i += 1
                else:
                    if start_time[i] - s < t_th[i]:
                        i -= 1
                    else:
                        lat1.append(lt)
                        lon1.append(ln)
                        ts.append(s)
                        te.append(start_time[i])
                        i -= 1
                    break
        if i == len(lat) - 1:
            if start_time[i] - s >= t_th[i]:
                lat1.append(lt)
                lon1.append(ln)
                ts.append(s)
                te.append(start_time[i])
            
distances_RI = []

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

# Thêm lớp bản đồ TomTom
TomTom_map = folium.TileLayer(
    tiles= 'http://{s}.api.tomtom.com/map/1/tile/sat/main/{z}/{x}/{y}.jpg?view=Unified&key=Q2CfUd9PDRAKwfsK5MRw1aXzul8zRIUY',
    attr='© TomTom',
    name='TomTom Satellite',
    min_zoom=0,
    max_zoom=19
).add_to(m)

# Thêm lớp bản đồ vệ tinh
tile_layer_satellite = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    name='Satellite Map',
    attr='Map data &copy; Google',
    min_zoom=0,
    max_zoom=22
).add_to(m)  # Thêm lớp bản đồ vệ tinh vào bản đồ chính

# Chấm các điểm trên bản đồ và thêm popup vị trí
 
points = []    
for i in range(len(lat)):
    # marker = folium.CircleMarker(location=[lat[i], lon[i]], radius=1, color='yellowgreen')
    # # Tạo popup vị trí
    # popup_content = f"Latitude: {lat[i]}<br>Longitude: {lon[i]}<br>av: {av_list[i]}<br>v: {velocity_list[i]}<br>IRI: {IRI[i]}"
    # popup = folium.Popup(popup_content, max_width=200)
    # # Thêm popup vào marker
    # marker.add_child(popup)
    # # Thêm marker vào bản đồ
    # marker.add_to(m)   
    points.append([lat[i], lon[i]])
folium.PolyLine(locations=points, color='yellowgreen',weight=4).add_to(m)
# polyline.options['weight'] *= 3
# polyline.add_to(m)
    
for i in range(len(lat1)): 
    line =  folium.CircleMarker(location=[lat1[i], lon1[i]], radius=1.5, color='red',fill_color = 'red')
    popup_content = f"Latitude: {lat1[i]}<br>Longitude: {lon1[i]}"
    popup = folium.Popup(popup_content, max_width=200)
    line.add_child(popup)  
    line.add_to(m) 

folium.LayerControl().add_to(m)
# Thiết lập lớp bản đồ đất liền là lớp mặc định
m.add_child(tile_layer_satellite)
m.save(mapsave)

#----------------------------------------------------------------------------------------------------------------------------

# Lưu vào tệp CSV mới (tùy chọn)
with open('separated_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['time','timestamp','Latitude', 'Longitude', 'ax', 'ay', 'az','av'])
    for i in range(len(time)):
        writer.writerow([time[i],time_list[i],latitude[i], longitude[i], ax[i], ay[i], az[i], av[i]])

with open(outputfile, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Timestamp','Lat','Lon','avg_av','s','v(km/h)','IRI'])
    for i in range(len(lat)):
        writer.writerow([start_time[i],lat[i],lon[i],av_list[i],distances[i],velocity_list[i]])

  