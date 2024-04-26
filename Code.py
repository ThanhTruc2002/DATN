import csv
import pandas as pd
import folium
import math
from datetime import datetime
import scipy.integrate as spi
import matplotlib.pyplot as plt

filename = './Input/4.csv'
outputfile = './Result/map_data4.csv'
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
def calculate_IRI(av, t1, t2):
    b = t2 - t1
    # Tính vận tốc
    velocity = av * b
    # Tính quãng đường
    Vh = spi.quad(lambda t: velocity, 0, b)[0]
    
    return Vh
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
Vh = []
Vh_values = []
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
starttime = time_list[0]
for i in range(len(latitude)-1):
    index = calculate_IRI(az[i], time_list[i], time_list[i+1])
    Vh.append(index)
    distance = haversine(latitude[i], longitude[i], latitude[i+1], longitude[i+1])
    distances.append(distance)
    if (latitude[i] == latitude[i+1] and longitude[i] == longitude[i+1]):
        if i == 0:
            starttime = time_list[0]
            velocity = 0
            velocity_list.append(velocity)
        else:
        # velocity = 3.6 * calculate_velocity(distances[i], starttime, time_list[i+1])     
            velocity = velocity_list[i-1]                 
            velocity_list.append(velocity)
    elif (latitude[i] != latitude[i+1] or longitude[i] != longitude[i+1]):        
        velocity = 3.6 * calculate_velocity(distances[i], starttime, time_list[i+1])                      
        velocity_list.append(velocity)        
        starttime = time_list[i+1] 
index = calculate_IRI(az[i], time_list[i], time_list[i+1])
Vh.append(index)   
distance = haversine(latitude[i], longitude[i], latitude[i+1], longitude[i+1])
distances.append(distance)
velocity_list.append(velocity_list[i-1])
total_distance = sum(distances)/1000
print(f"S: {total_distance}")
#Tính IRI
# starttime = endtime = time_list[0]

for i in range(len(latitude)-1):
    if (latitude[i] == latitude[i+1] and longitude[i] == longitude[i+1]):
        if i == 0:
            Vh_values.append(Vh[0])
            Vh_values.append(Vh[i+1])
        else:
            Vh_values.append(Vh[i+1])
    else:
        iri = sum(Vh_values)/total_distance
        IRI.append(iri)
        lat.append(latitude[i-1])
        lon.append(longitude[i-1])  
        Vh_values = []   
        Vh_values.append(Vh[i+1])    
lat.append(latitude[i-1])
lon.append(longitude[i-1]) 
iri = sum(Vh_values)/total_distance
IRI.append(iri)

#Xác định bump, pothole
for i in range(len(latitude)):
    if velocity_list[i] == 0:
        t_th.append(0)
    else:
        t_th.append(L * 3.6 / velocity_list[i])

lat1 = []
lon1 = []
lat2 = []
lon2 = []
ts = []
te = []   
av_th = 17
i=0
s, e = 0, 0
# s, e, lt, ln = None, None, None, None
while (i) < len(latitude): 
    if az[i] >= av_th:
        
        s = time_list[i]
        e = s
        i += 1
        while (i) < len(latitude):
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
                        lat1.append(latitude[i])
                        lon1.append(longitude[i])
                        ts.append(s)
                        te.append(time_list[i])
                        i -= 1
                    break
        if i == len(latitude) - 1:
            if time_list[i] - s >= t_th[i]:
                lat1.append(latitude[i])
                lon1.append(longitude[i])
                ts.append(s)
                te.append(time_list[i])
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
point1 = []    
point2 = []    
for i in range(len(latitude)): 
    points.append([latitude[i], longitude[i]])
folium.PolyLine(locations=points, color='yellowgreen',weight=5).add_to(m)

for i in range(len(lat)):
    lt, ln = 0, 0
    if IRI[i] > 2.8:
        lt = lat[i]
        ln = lon[i]
        j = i + 1
        while j < len(lat) and (IRI[j] > 2.8):
            point1.append([lt, ln])
            point2.append([lat[j], lon[j]])
            break
        if point1 and point2:
            color = 'yellow'
            if IRI[i] > 4:
                color = 'red'
            folium.PolyLine(locations=(point1[-1], point2[-1]), color=color, weight=5).add_to(m)
        point1 = []
        point2 = []
        

       
for i in range(len(lat1)): 
    line =  folium.CircleMarker(location=[lat1[i], lon1[i]], radius=1.5, color='black',fill_color = 'red')
    popup_content = f"Latitude: {lat1[i]}<br>Longitude: {lon1[i]}<br>Time_start: {ts[i]}<br>Time_end: {te[i]}"
    popup = folium.Popup(popup_content, max_width=200)
    line.add_child(popup)  
    line.add_to(m) 
    
# Define legend HTML content
template = """
<div id='maplegend' class='maplegend' 
    style='position: fixed; 
           z-index:9999; 
           border:2px solid grey; 
           background-color:rgba(255, 255, 255, 1);
           border-radius:6px; 
           padding: 5px; 
           font-size:14px; 
           weight: 200px; height: min-content;
           left: 10px; 
           bottom: 50px;'>
     
<div class='legend-title' style='color:black; weight: 600px; padding: 5px'>IRI(m/km):</div>
<p style='color:black;'><span style='background:yellowgreen; 
                                        opacity: 1; 
                                        width: 15px; 
                                        height: 12px; 
                                        display: inline-block;
                                        border:1px solid grey; 
                                        margin-right: 5px;'></span>Good (0 - 2.8)</p>
<p style='color:black;'><span style='background:yellow; 
                                        opacity: 1; 
                                        width: 15px; 
                                        height: 12px; 
                                        display: inline-block;
                                        border:1px solid grey; 
                                        margin-right: 5px;'></span>Fair (2.8 - 4)</p>
<p style='color:black;'><span style='background:red; 
                                        opacity: 1; 
                                        width: 15px; 
                                        height: 12px; 
                                        display: inline-block;
                                        border:1px solid grey; 
                                        margin-right: 5px;'></span>Poor (≥4)</p>
<p style='color:black;'><span style='background:black; 
                                        opacity: 1; 
                                        width: 12px; 
                                        height: 12px; 
                                        border-radius: 50%; 
                                        display: inline-block;
                                        border:1px solid grey; 
                                        margin-right: 5px;'></span>Pothole</p>
</div>
</div>
"""

m.get_root().html.add_child(folium.Element(template))
folium.LayerControl().add_to(m)
# Thiết lập lớp bản đồ đất liền là lớp mặc định
m.add_child(tile_layer_satellite)
# Thêm popup vào bản đồ
m.save(mapsave)
#----------------------------------------------------------------------------------------------------------------------------

# Lưu vào tệp CSV mới (tùy chọn)
with open('separated_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['time','timestamp','Latitude', 'Longitude', 'ax', 'ay', 'az','v','s','Vh'])
    for i in range(len(time)):
        writer.writerow([time[i],time_list[i],latitude[i], longitude[i], ax[i], ay[i], az[i],velocity_list[i],distances[i],Vh[i]])

with open(outputfile, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Lat','Lon','IRI'])
    for i in range(len(lat)):
        writer.writerow([lat[i],lon[i],IRI[i]])

# az_value = list(range(len(latitude)))
# plt.plot(az_value, az)
# plt.xlabel('Time')
# plt.ylabel('az')
# plt.title('az')
# plt.show()