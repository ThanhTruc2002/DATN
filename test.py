
import csv
import math
from datetime import datetime

# Định nghĩa kiểu dữ liệu cho từng cột
column_types = {
    "Time": "datetime",
    "Latitude": "float",
    "Longitude": "float",
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Bán kính trái đất
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    deltaφ = φ2 - φ1
    deltaλ = math.radians(lon2 - lon1)

    a = math.sin(deltaφ / 2) * math.sin(deltaφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(deltaλ / 2) * math.sin(deltaλ / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


filename = "4.csv"
latitude = []
longitude = []
ax = []
ay = []
az = []
time_list = []
distances = []

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)

    for row in reader:
        # Lấy tên cột và kiểu dữ liệu
        column_name = row[1]

        if column_name == "Latitude:":
            latitude.append(float(row[2]))
        elif column_name == "Longitude:":
            longitude.append(float(row[2]))
        elif column_name == "Acc":
            time_string = row[0]
            datetime_object = datetime.strptime(time_string, "%m/%d/%Y %H:%M:%S.%f")
            timestamp = datetime_object.timestamp()*1000
            time_list.append(timestamp)
            ax.append(row[2])
            ay.append(row[3])
            az.append(row[4])

# Lưu vào tệp CSV mới (tùy chọn)
with open('separated_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['timestamp', 'Latitude', 'Longitude', 'ax', 'ay', 'az'])
    for i in range(len(longitude)):
        writer.writerow([time_list[i], latitude[i], longitude[i], ax[i], ay[i], az[i]])

for i in range(len(longitude) - 1):
    distance = haversine(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1])
    distances.append(distance)
total_distance = sum(distances)
print(f"S: {total_distance}")