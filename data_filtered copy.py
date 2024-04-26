import csv
import math
from datetime import datetime
import scipy.integrate as spi

filename = './Input/5.csv'
outputfile = './Result/map_data5.csv'

# Định nghĩa kiểu dữ liệu cho từng cột
column_types = {
    "Time": "datetime",
    "Latitude": "float",
    "Longitude": "float",
}


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
def calculate_IRI(S,av, ts, te):
    b = te - ts
    # Tính vận tốc
    velocity = av * b

    # Tính quãng đường
    distance = spi.quad(lambda t: velocity, 0, b)[0]
    index = distance / S

    return index

#-----------------------------------------------------------------------------------------------------------------------------------

latitude = []
longitude = []
ax = []
ay = []
az = []
time = []
time_list = []
distances = []
ax_values = []
ay_values = []
az_values = [] 
avg_ax_list = [] 
avg_ay_list = [] 
avg_az_list = [] 
lat = []
lon = []  
start_time = []
stop_time = [] 
av = []
av_list = []
IRI = []
velocity_list = []

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)
    
    for row in reader:
        # Lấy tên cột và kiểu dữ liệu
        column_name = row[1]
                
        if column_name == "Latitude:":
            latitude.append(float(row[2]))
            time.append(row[0])
            time_string = row[0]
            datetime_object = datetime.strptime(time_string, "%m/%d/%Y %H:%M:%S.%f")
            timestamp = datetime_object.timestamp()
            time_list.append(timestamp)
        elif column_name == "Longitude:":
            longitude.append(float(row[2]))
        elif column_name == "Acc":
            ax.append(float(row[2]))
            ay.append(float(row[3]))
            az.append(float(row[4]))               
    #-----------------------------------------------------------------------------------------------------------------------
    
#Lọc dữ liệu
for i in range(len(latitude)):
    if (latitude[i] == latitude[i-1] and longitude[i] == longitude[i-1]):
        ax_values.append(ax[i])
        ay_values.append(ay[i])
        az_values.append(az[i])
        # stop_time.append(time_list[i])
        
    elif (latitude[i] != latitude[i-1] or longitude[i] != longitude[i-1]):
        if i == 0:            
            ax_values.append(ax[0])
            ay_values.append(ay[0])
            az_values.append(az[0])
            start_time.append(time_list[0])
            # stop_time.append(time_list[i - 1 + len(ax_values)])
        elif len(ax_values) > 0 :
            # stop_time.append(time_list[i - 1 + len(ax_values)])
            avg_ax = sum(ax_values)/(len(ax_values))
            avg_ay = sum(ay_values)/(len(ay_values))
            avg_az = sum(az_values)/(len(az_values))
            av = math.sqrt(avg_ax*avg_ax + avg_ay*avg_ay + avg_az*avg_az)
            start_time.append(time_list[i])
            # stop_time.append(time_list[i -1 + len(ax_values)])
            lat.append(latitude[i-1])
            lon.append(longitude[i-1])
            avg_ax_list.append("{:.2f}".format(avg_ax))
            avg_ay_list.append("{:.2f}".format(avg_ay))
            avg_az_list.append("{:.2f}".format(avg_az))
            av_list.append(av)
            ax_values = []
            ax_values.append(ax[i])
            ay_values = []
            ay_values.append(ay[i])
            az_values = []
            az_values.append(az[i])

           
avg_ax = sum(ax_values)/(len(ax_values))
avg_ay = sum(ay_values)/(len(ay_values))
avg_az = sum(az_values)/(len(az_values))
av = math.sqrt(avg_ax*avg_ax + avg_ay*avg_ay + avg_az*avg_az)
start_time.append(time_list[i])
# stop_time.append(time_list[i])
lat.append(latitude[i])
lon.append(longitude[i])
avg_ax_list.append("{:.2f}".format(avg_ax))
avg_ay_list.append("{:.2f}".format(avg_ay))
avg_az_list.append("{:.2f}".format(avg_az))
av_list.append(av)

L=1.4
t_th = []
#Tính tổng quãng đường
for i in range(len(lat)):
    
    if (i < len(lat)-1):
        distance = haversine(lat[i],lon[i],lat[i+1],lon[i+1])
        distances.append(distance)
        velocity = 3.6*calculate_velocity(distances[i],start_time[i],start_time[i+1])
        velocity_list.append(velocity)
    elif i >= len(lat)-1:
        distance = haversine(lat[i],lon[i],lat[i],lon[i])
        distances.append(distance)
        velocity = 3.6*calculate_velocity(distances[i],0,start_time[i])
        velocity_list.append(velocity)
    
    total_distance = sum(distances)/1000
print(f"S: {total_distance}") 

for i in range(len(lat)):
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

for i in range(len(lat)):    
    av_th = 10.6
    s = 0
    e = 0
    lt = 0
    ln = 0
    if av_list[i] >= av_th:
        s = float(start_time[i])
        e = float(start_time[i])
        lt = lat[i]
        ln = lon[i]
        for j in range(i+1, len(lat)):
            if av_list[j] < av_th:
                break
            else:
                if start_time[j] - e < t_th[j]:
                    e = float(start_time[j])
                else:
                    if e - s >= t_th[j]:
                        lat1.append(lt)
                        lon1.append(ln)
                        lat2.append(lat[i])
                        lon2.append(lon[i])
                        ts.append(s)
                        te.append(time_list[i])
                    lat1.append(lt)
                    lon1.append(ln)
                    lat2.append(lat[j])
                    lon2.append(lon[j])
                    ts.append(s)
                    te.append(time_list[j])
        if i == len(lat)-1:
            if e - s >= t_th[i]:
                lat1.append(lt)
                lon1.append(ln)
                lat2.append(lat[i])
                lon2.append(lon[i])
                ts.append(s)
                te.append(time_list[i])
                        



#Tính IRI
for i in range(len(lat)):
    index = calculate_IRI(total_distance,av_list[i], start_time[i], start_time[i+1])
    IRI.append(index)

   
# Lưu vào tệp CSV mới (tùy chọn)
# with open('separated_data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(['time','timestamp','Latitude', 'Longitude', 'ax', 'ay', 'az'])
#     for i in range(len(time)):
#         writer.writerow([time[i],time_list[i],latitude[i], longitude[i], ax[i], ay[i], az[i]])
        
with open(outputfile, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Timestamp','Lat','Lon','avg_ax','avg_ay','avg_az','av','s','v(km/h)','IRI'])
    for i in range(len(lat)):
        writer.writerow([start_time[i],lat[i],lon[i],avg_ax_list[i],avg_ay_list[i],avg_az_list[i],av_list[i],distances[i],velocity_list[i],IRI[i]])

print(len(ts), len(lat1), len(lon1), len(lat2), len(lon2), len(te))
  
