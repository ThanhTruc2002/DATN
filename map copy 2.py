#%%
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

m = folium.Map(location=[10.8735809326,106.801788330], zoom_start=18, control_scale=True)

#Thêm lớp bản đồ đất liền
tile_layer_land = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    name='Land Map',
    attr='Map data &copy; Google',
).add_to(m)

# Thêm lớp bản đồ vệ tinh
tile_layer_satellite = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    name='Satellite Map',
    attr='Map data &copy; Google',
).add_to(m)  # Thêm lớp bản đồ vệ tinh vào bản đồ chính

TomTom_map = folium.TileLayer(
    tiles= 'http://{s}.api.tomtom.com/map/1/tile/sat/main/{z}/{x}/{y}.jpg?view=Unified&key=Q2CfUd9PDRAKwfsK5MRw1aXzul8zRIUY',
    name='TomTom Map',
    attr='TomTom'
).add_to(m)

# Chấm các điểm trên bản đồ và thêm popup vị trí
for i in range(len(latitude)):
    if i < len(longitude):
        marker = folium.CircleMarker(location=[latitude[i], longitude[i]], radius=0.1, color='green', fill=True,
                                     fill_color='lime')

        # Tạo popup vị trí
        popup_content = f"Latitude: {latitude[i]}<br>Longitude: {longitude[i]}"
        popup = folium.Popup(popup_content, max_width=200)

        # Thêm popup vào marker
        marker.add_child(popup)

        # Thêm marker vào bản đồ
        marker.add_to(m)

folium.LayerControl().add_to(m)
# Thiết lập lớp bản đồ đất liền là lớp mặc định
# m.add_child(tile_layer_land)
m
m.save("mapcopy2.html")
# %%
