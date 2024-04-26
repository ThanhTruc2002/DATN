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

mapbox_access_token = 'pk.eyJ1Ijoibmd1eWVudHJ1YyIsImEiOiJjbHM4N3Zid2kxcXF2MmtyeGxiZzlycTE0In0._CIVOKhrCXrb5FVookdGrA'  # Thay YOUR_MAPBOX_ACCESS_TOKEN bằng khóa truy cập API của bạn

m = folium.Map(location=[10.8735809326, 106.801788330], zoom_start=20, control_scale=True)

# Thêm lớp bản đồ vệ tinh từ Mapbox
tile_layer_satellite = folium.TileLayer(
    tiles='https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token=' + mapbox_access_token,
    attr='Map data &copy; <a href="https://www.mapbox.com/">Mapbox</a>',
    name='Satellite Map',
).add_to(m)

# Thêm lớp bản đồ đường phố từ Mapbox
tile_layer_streets = folium.TileLayer(
    tiles='https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=' + mapbox_access_token,
    attr='Map data &copy; <a href="https://www.mapbox.com/">Mapbox</a>',
    name='Streets Map',
).add_to(m)

# Chấm các điểm trên bản đồ và thêm popup vị trí
for i in range(len(latitude)):
    if i < len(longitude):
        marker = folium.CircleMarker(location=[latitude[i], longitude[i]], radius=0.1, color='green', fill=True,
                                     fill_color='green')

        # Tạo popup vị trí
        popup_content = f"Latitude: {latitude[i]}<br>Longitude: {longitude[i]}"
        popup = folium.Popup(popup_content, max_width=200)

        # Thêm popup vào marker
        marker.add_child(popup)

        # Thêm marker vào bản đồ
        marker.add_to(m)

folium.LayerControl().add_to(m)
# Thiết lập lớp bản đồ vệ tinh là lớp mặc định
m.add_child(tile_layer_satellite)
m.save("mapcopy3.html")