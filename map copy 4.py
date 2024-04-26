#%%
import csv
import folium
import tomtom_api as TomTom

filename = "022124_1.csv"
latitude = []
longitude = []

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)
    i = 0  # Biến đếm để theo dõi vị trí hàng
    for row in reader:
        time = row[1]
        if i % 2 == 0:
            # Dữ liệu vĩ độ
            longitude.append(row[2])
        else:
            # Dữ liệu kinh độ
            latitude.append(row[2])
        i += 1

tomtom_api_key = "98866b2d-15ff-468e-bd36-0acc03edd605"
tomtom = TomTom(tomtom_api_key)

m = folium.Map(location=[10.87374973,106.8014297], zoom_start=18, control_scale=True)

# Thêm lớp bản đồ TomTom
tile_layer_tomtom = folium.TileLayer(
    tiles=tomtom.get_map_tile('standard', '{z}/{x}/{y}'),
    name='TomTom Standard Map',
    attr='Map data &copy; TomTom',
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
# Thiết lập lớp bản đồ đất liền là lớp mặc định
m.add_child(tile_layer_tomtom)
# m
m.save("mapcopy4.html")
# %%
