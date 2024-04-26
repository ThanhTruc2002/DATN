import csv
import math
from datetime import datetime
import pandas as pd
import scipy.integrate as spi
# Định nghĩa kiểu dữ liệu cho từng cột

filename = './Input/4.csv'
outputfile1 = './Result/separated_data.csv'
outputfile2 = './Result/separated_data4.csv'

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


distances = []
av_values = []
ay_values = []
az_values = [] 
avg_ax_list = [] 
avg_ay_list = [] 
avg_az_list = [] 
lat = []
lon = []  
start_time = []
timestamp = [] 
av = []
av_list = []
IRI = []
velocity_list = []

# with open(filename, 'r') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     next(reader, None)
    
#     for row in reader:
#         # Lấy tên cột và kiểu dữ liệu
#         column_name = row[1]
                
#         if column_name == "Latitude:":
#             latitude.append(float(row[2]))
#             time.append(row[0])
#             time_string = row[0]
#             datetime_object = datetime.strptime(time_string, "%m/%d/%Y %H:%M:%S.%f")
#             time_stamp = datetime_object.timestamp()
#             time_list.append(float(time_stamp))
#         elif column_name == "Longitude:":
#             longitude.append(float(row[2]))
#         elif column_name == "Acc":
#             # time.append(row[0])
#             # time_string = row[0]
#             # datetime_object = datetime.strptime(time_string, "%m/%d/%Y %H:%M:%S.%f")
#             # timestamp = datetime_object.timestamp()
#             # time_list.append(timestamp)
#             ax.append(float(row[2]))
#             ay.append(float(row[3]))
#             az.append(float(row[4]))  

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
            timestamp.append(time_list[0]) 
        elif len(av_values) > 0 :
            avg_av = sum(av_values)/len(av_values) 
            timestamp.append(time_list[i])
              
            lat.append(latitude[i-1])
            lon.append(longitude[i-1]) 
            av_list.append(avg_av) 
            av_values = [] 
            av_values.append(av[i]) 
            
avg_av = sum(av_values)/len(av_values) 
timestamp.append(time_list[i])  
lat.append(latitude[i-1])
lon.append(longitude[i-1]) 
av_list.append(avg_av) 
    
#Tính tổng quãng đường
for i in range(len(lat)):
    # if i == len(lat):
    #     distance = haversine(lat[i],lon[i],lat[i],lon[i])
    #     distances.append(distance)
    #     velocity = 3.6*calculate_velocity(distances[i],start_time[i],0)
    #     velocity_list.append(velocity)
    if (i < len(lat)-1):
        distance = haversine(lat[i],lon[i],lat[i+1],lon[i+1])
        distances.append(distance)
        velocity = 3.6*calculate_velocity(distances[i],timestamp[i],timestamp[i+1])
        velocity_list.append(velocity)
    elif i >= len(lat)-1:
        distance = haversine(lat[i],lon[i],lat[i],lon[i])
        distances.append(distance)
        velocity = 3.6*calculate_velocity(distances[i],0,timestamp[i])
        velocity_list.append(velocity)
    total_distance = sum(distances)/1000
print(f"S: {total_distance}") 

# #Tính IRI
# for i in range(len(lat)):
#     index = calculate_IRI(total_distance,av_list[i], start_time[i], start_time[i+1])
#     IRI.append(index)

   
# Lưu vào tệp CSV mới (tùy chọn)
with open(outputfile1, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['time','timestamp','Latitude', 'Longitude', 'ax', 'ay', 'az','av'])
    for i in range(len(time)):
        writer.writerow([time[i],time_list[i],latitude[i], longitude[i], ax[i], ay[i], az[i], av[i]])
        
with open(outputfile2, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Timestamp','Lat','Lon','avg_av','s','v(km/h)','IRI'])
    for i in range(len(lat)):
        writer.writerow([timestamp[i],lat[i],lon[i],av_list[i],distances[i],velocity_list[i]])


# with open('separated_data5.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(['Timestamp','Lat','Lon','avg_ax','avg_ay','avg_az','av','s','v(km/h)','IRI'])
#     for i in range(len(lat)):
#         writer.writerow([start_time[i],lat[i],lon[i],avg_ax_list[i],avg_ay_list[i],avg_az_list[i],av_list[i],distances[i],velocity_list[i],IRI[i]])
    
