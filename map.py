# %%
import csv
import folium

filename = "gps4.csv"
latitude = []
longitude = []

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            latitude.append(float(row[0]))  
            longitude.append(float(row[1]))
        except ValueError:
            continue  

m = folium.Map(location=[10.8773155212,106.80043029780],
               zoom_start=17, control_scale=True)

# Tạo lớp bản đồ vệ tinh
tile_layer_satellite = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
    name='Satellite Map',
    attr='Map data &copy; Google',
).add_to(m)

# Chấm các điểm trên bản đồ
# Chấm các điểm bằng dấu chấm trên bản đồ
for i in range(len(latitude)):
    if i < len(longitude):
        marker = folium.CircleMarker(location=[latitude[i], longitude[i]], 
                                     radius=0.5, color='green', 
                                     fill=True, fill_color='green')
        
        # Tạo popup vị trí
        popup_content = f"Latitude: {latitude[i]}<br>Longitude: {longitude[i]}"
        popup = folium.Popup(popup_content, max_width=200)
        
        # Thêm popup vào marker
        marker.add_child(popup)
        
        # Thêm marker vào bản đồ
        marker.add_to(m)
        
        

folium.LayerControl().add_to(m)

# Tạo sự kiện click để hiển thị popup khi bấm vào điểm
# folium.LatLngPopup().add_to(m)
m
# m.save("map.html")
# %%
