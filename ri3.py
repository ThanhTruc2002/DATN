import csv
import math
import folium 

# filename = "separated_data.csv"
filename = 'separated_data.csv'
outputfile = './Result/data4.csv'
mapsave = './Map/mapcopy2.html'

def haversine(lat1,lon1,lat2,lon2):
    R = 6371e3 #Bán kinh trái đất
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    deltaφ = φ2 - φ1
    deltaλ = math.radians(lon2 - lon1)

    a = math.sin(deltaφ / 2) * math.sin(deltaφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(deltaλ / 2) * math.sin(deltaλ / 2)
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    return R * c

def calculate_velocity(s,t1,t2):
    velocity = s/(t2-t1)
    
    return velocity

time = []
time_list = []
av = []
lat = []
lon = []
ts = []
te = []
lat1 = []
lon1 = []
lat2 = []
lon2 = []
distances = []
point1 = []
point2 = []
points = []
velocity_list = []
t_th = []

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)    
    for row in reader:
      time_list.append(float(row[1]))
      lat.append(float(row[2]))
      lon.append(float(row[3]))
      av.append(float(row[6]))
      
total_distance = 0
for i in range(len(lat)-1):
    distance = haversine(lat[i], lon[i], lat[i+1], lon[i+1])
    distances.append(distance)
    velocity = 3.6 * calculate_velocity(distances[i], time_list[i], time_list[i+1])
    velocity_list.append(velocity)
    total_distance += distance

if len(lat) > 0:
    distance = haversine(lat[-2], lon[-2], lat[-1], lon[-1])
    distances.append(distance)
    velocity = 3.6 * calculate_velocity(distances[-1], time_list[-2], time_list[-1])
    velocity_list.append(velocity)
    total_distance += distance

total_distance /= 1000

L=1.4
for i in range(len(lat)):
    if velocity_list[i] == 0:
        t_th.append(0)
    else:
        t_th.append(L * 3.6 / velocity_list[i])
      
for i in range(len(lat)):
        m = folium.Map(location=[lat[0], lon[0]], zoom_start=18, control_scale=True)

# for i in range(len(lat)):
#     s = 0
#     e = 0
#     lt = 0
#     ln = 0
#     if av[i] >= av_th:
#         # ts.append(time_list[i])
#         s = float(time_list[i])
#         e = float(time_list[i])
#         lt = lat[i]
#         ln = lon[i]
#         for j in range(i+1, len(lat)):
#             if av[j] < av_th:
#                 break
#             else:
#                 if time_list[j] - e < t_th:
#                     e = float(time_list[j])
#                 else:
#                     if e - s >= t_th:
#                         lat1.append(lt)
#                         lon1.append(ln)
#                         lat2.append(lat[i])
#                         lon2.append(lon[i])
#                         ts.append(s)
#                         te.append(time_list[i])
#                     lat1.append(lt)
#                     lon1.append(ln)
#                     lat2.append(lat[j])
#                     lon2.append(lon[j])
#                     ts.append(s)
#                     te.append(time_list[j])
#         if i == len(lat)-1:
#             if e - s >= t_th:
#                 lat1.append(lt)
#                 lon1.append(ln)
#                 lat2.append(lat[i])
#                 lon2.append(lon[i])
#                 ts.append(s)
#                 te.append(time_list[i])


av_th =  2*9.8

for i in range(len(lat)):    
    s, e, lt, ln = None, None, None, None
    if av[i] >= av_th:
        s = float(time_list[i])
        e = s
        lt = lat[i]
        ln = lon[i]
        while (i) < len(lat):
            if av[i] < av_th:
                i += 1
            else:
                if time_list[i] - e < t_th[i]:
                    e = float(time_list[i])
                    i += 1
                else:
                    if e - s < t_th[i]:
                        i -= 1
                    else:
                        lat1.append(lt)
                        lon1.append(ln)
                        ts.append(s)
                        te.append(time_list[i])
                        i -= 1
                    break
        if i == len(lat) - 1:
            if e - s >= t_th[i]:
                lat1.append(lt)
                lon1.append(ln)
                ts.append(s)
                te.append(time_list[i])               

          
#------------------------------------------------------------------------------------------------------------------------------------
# Thêm lớp bản đồ đất liền
tile_layer_land = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    name='Land Map',
    attr='Map data &copy; Google',
    min_zoom=0,
    max_zoom=19
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
    max_zoom=19
).add_to(m)  # Thêm lớp bản đồ vệ tinh vào bản đồ chính

# folium.PolyLine(locations=list(zip(lat, lon)), color='yellowgreen', opacity=0.85).add_to(m)
for i in range(len(lat)):
      points.append([lat[i], lon[i]])
folium.PolyLine(locations=points, color='yellowgreen',weight=4).add_to(m)

for i in range(len(lat1)): 
    line =  folium.CircleMarker(location=[lat1[i], lon1[i]], radius=1.5, color='red',fill_color = 'red')
    popup_content = f"Latitude: {lat1[i]}<br>Longitude: {lon1[i]}"
    popup = folium.Popup(popup_content, max_width=200)
    line.add_child(popup)  
    line.add_to(m)              

        
with open(outputfile, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['time_start','time_end','lat1','lon1','lat2','lon2','s'])
    for i in range(len(lat1)):
        writer.writerow([ts[i],te[i],lat1[i], lon1[i]])


print(len(ts), len(lat1), len(lon1),len(te))
folium.LayerControl().add_to(m)


# Thiết lập lớp bản đồ đất liền là lớp mặc định
m.add_child(tile_layer_satellite)
m.save(mapsave)
  