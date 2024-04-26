#%%
import csv
import folium

filename = "4.csv"
latitude = []
longitude = []
ax = []
ay = []
az = []
time = []

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)
    
    for row in reader:
        # Lấy tên cột và kiểu dữ liệu
        column_name = row[1]
                
        if column_name == "Latitude:":
            latitude.append(row[2])
        elif column_name == "Longitude:":
            longitude.append(row[2])
        elif column_name == "Acc":
            time.append(row[0])
            ax.append(float(row[2]))
            ay.append(float(row[3]))
            az.append(float(row[4]))
for i in range(len(latitude)):
    if i < len(longitude):
        m = folium.Map(location=[latitude[0], longitude[0]], zoom_start=18, control_scale=True)
        

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



# Chấm các điểm trên bản đồ và thêm popup vị trí
for i in range(len(latitude)):
    if 6<=az[i]<=11.5:
        marker = folium.CircleMarker(location=[latitude[i], longitude[i]], radius=0.1, color='yellowgreen', fill=True)
    else:
        marker = folium.CircleMarker(location=[latitude[i], longitude[i]], radius=0.1, color='red', fill=True)
    # Tạo popup vị trí
    popup_content = f"Latitude: {latitude[i]}<br>Longitude: {longitude[i]}<br>az: {az[i]}"
    popup = folium.Popup(popup_content, max_width=200)

    # Thêm popup vào marker
    marker.add_child(popup)
    
    # Thêm marker vào bản đồ
    marker.add_to(m)
    
for i in range(len(latitude)):
    if 7<=az[i]<=11:
       point = []
        

folium.LayerControl().add_to(m)


# Thiết lập lớp bản đồ đất liền là lớp mặc định
m.add_child(tile_layer_satellite)
m.save("mapcopy 4.html")
m
# %%
