import csv
import pandas as pd
import folium
import math
from datetime import datetime
import scipy.integrate as spi

class Calculator:

    #Hàm tính tổng quãng đường
    def calculate_distance(self,lat1,lon1,lat2,lon2):
        R = 6371e3 
        φ1 = math.radians(lat1)
        φ2 = math.radians(lat2)
        deltaφ = φ2 - φ1
        deltaλ = math.radians(lon2 - lon1)
        
        a = math.sin(deltaφ / 2) * math.sin(deltaφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(deltaλ / 2) * math.sin(deltaλ / 2)
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
        total_distance = R*c
        return total_distance
    
    #Hàm tính vận tốc
    def calculate_velocity(self, s, t1, t2):
        velocity = s / (t2 - t1)
        return velocity

    #Hàm tính IRI
    def calculate_IRI(self, az, t1, t2):
        b = t2 - t1
        velocity_iri = az * b
        Vh = spi.quad(lambda t: velocity_iri, 0, b)[0]
        return Vh

# # Exam class Calculator
# calculator = Calculator()
# velocity = calculator.calculate_velocity(100, 1, 5)
# print("Vận tốc:", velocity)

# Vh = calculator.calculate_IRI(10, 1, 5)
# print("IRI:", Vh)

# distance = calculator.calculate_distance(lat1,lon1,lat2,lon2)
# print("Quãng đường:", total_distance)

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

#data-filtered. cac def: get data,list of colum. append data base on name of colum. 
class DataProcessor:

    def __init__(self, filename):
        self.data = pd.read_csv(filename) 
        self.column_names = self.data.columns.tolist() 
        self.calculator = Calculator()
    
    def get_latitude(self):
        latitude = self.data.loc[(self.data[self.column_names[1]] == 'Latitude:'), self.column_names[2]].astype(float).tolist()
        return latitude
    
    def get_longitude(self):
        longitude = self.data.loc[(self.data[self.column_names[1]] == 'Longitude:'), self.column_names[2]].astype(float).tolist()
        return longitude
    
    def get_time(self):
        time = self.data.loc[(self.data[self.column_names[1]] == 'Latitude:'), self.column_names[0]].tolist()
        return time
    
    def get_timestamp(self):
        time_list = []
        for index, row in self.data.iterrows():
            column_name = row[self.column_names[1]]
            if column_name == 'Latitude:':
                time_string = row[self.column_names[0]]
                datetime_object = datetime.strptime(time_string, "%m/%d/%Y %H:%M:%S.%f")
                time_stamp = datetime_object.timestamp()
                time_list.append(float(time_stamp))
        return time_list
    
    def get_acceleration(self):
        ax = self.data.loc[self.data[self.column_names[1]] == 'Acc', self.column_names[2]].astype(float).tolist()
        ay = self.data.loc[self.data[self.column_names[1]] == 'Acc', self.column_names[3]].astype(float).tolist()
        az = self.data.loc[self.data[self.column_names[1]] == 'Acc', self.column_names[4]].astype(float).tolist()
        return ax, ay, az
    
    def calculate_velocity_distance(self):

        latitude = self.get_latitude()
        longitude = self.get_longitude() 
        time_list = self.get_timestamp()
        az = self.get_acceleration()[2]

        total_distance = 0
        starttime = time_list[0]

        distances = []
        velocity_list = []

        for i in range(len(latitude)-1):

            index = self.calculator.calculate_IRI(az[i], time_list[i], time_list[i+1])
            Vh.append(index)  

            distance = self.calculator.calculate_distance(latitude[i], longitude[i], latitude[i+1], longitude[i+1])
            distances.append(distance)

            if (latitude[i] == latitude[i+1] and longitude[i] == longitude[i+1]):
                velocity = 3.6 * self.calculator.calculate_velocity(distances[i], starttime, time_list[i+1])                      
                velocity_list.append(velocity)

            elif (latitude[i] != latitude[i+1] or longitude[i] != longitude[i+1]):        

                if i == 0:
                    starttime = time_list[0]
                else:
                    velocity = 3.6 * self.calculator.calculate_velocity(distances[i], starttime, time_list[i+1])                      
                    velocity_list.append(velocity)        
                    starttime = time_list[i+1]  

        index = self.calculator.calculate_IRI(az[i], time_list[i], time_list[i+1])
        Vh.append(index)

        distance = self.calculator.calculate_distance(latitude[i], longitude[i], latitude[i+1], longitude[i+1])  
        distances.append(distance)

        velocity_list.append(velocity_list[i-1])

        total_distance = sum(distances)/1000

        return total_distance, distances, velocity_list,Vh
    
## exam class DataProcessor
# filename = 'data.csv'
# data_processor = DataProcessor(filename)

# latitude = data_processor.get_latitude()
# print("Latitude:", latitude)

# longitude = data_processor.get_longitude()
# print("Longitude:", longitude)

# time = data_processor.get_time()
# print("Time:", time)

# ax, ay, az = data_processor.get_acceleration()
# print("Acceleration (ax):", ax)
# print("Acceleration (ay):", ay)
# print("Acceleration (az):", az)

#--------------------------------------------------------------------------------------------------

class IRICalculation:
    def __init__(self, latitude, longitude, Vh, total_distance):
        self.latitude = latitude
        self.longitude = longitude
        self.Vh = Vh
        self.total_distance = total_distance
        self.IRI = []
        self.lat = []
        self.lon = []

    def calculate_IRI(self):
        Vh_values = []
        lat = []
        lon = []

        for i in range(len(self.latitude)-1):
            if self.latitude[i] == self.latitude[i+1] and self.longitude[i] == self.longitude[i+1]:
                if i == 0:
                    Vh_values.append(self.Vh[0])
                    Vh_values.append(self.Vh[i+1])
                else:
                    Vh_values.append(self.Vh[i+1])
            else:
                iri = sum(Vh_values) / self.total_distance
                self.IRI.append(iri)
                lat.append(self.latitude[i-1])
                lon.append(self.longitude[i-1])
                Vh_values = []
                Vh_values.append(self.Vh[i+1])

        lat.append(self.latitude[-1])
        lon.append(self.longitude[-1])
        iri = sum(Vh_values) / self.total_distance
        self.IRI.append(iri)

        self.lat = lat
        self.lon = lon

        # Trả về danh sách IRI, lat, lon
        return self.IRI, self.lat, self.lon
##exam
# # Tạo một thể hiện của lớp IRICalculation
# iri_calc = IRICalculation(latitude, longitude, Vh, total_distance)
# # Gọi phương thức calculate_IRI() để tính toán chỉ số IRI
# IRI_values, lat_values, lon_values = iri_calc.calculate_IRI()

#--------------------------------------------------------------------------------------------------

class BumpPotholeDetection:
    def __init__(self, latitude, longitude, velocity_list, az, time_list):
        self.latitude = latitude
        self.longitude = longitude
        self.velocity_list = velocity_list
        self.az = az
        self.time_list = time_list
        self.lat1 = []
        self.lon1 = []
        self.ts = []
        self.te = []
        self.av_th = 17

    def detect_bumps_potholes(self):
        t_th = []
        L = 1  # Giá trị L của bạn, có thể thay đổi tùy theo yêu cầu

        for i in range(len(self.latitude)):
            if self.velocity_list[i] == 0:
                t_th.append(0)
            else:
                t_th.append(L * 3.6 / self.velocity_list[i])

        for i in range(len(self.latitude)):
            s, e = 0, 0
            if self.az[i] >= self.av_th:
                s = self.time_list[i]
                e = s
                i += 1
                while i < len(self.latitude):
                    if self.az[i] < self.av_th:
                        i += 1
                    else:
                        if self.time_list[i] - e < t_th[i]:
                            e = self.time_list[i]
                            i += 1
                        else:
                            if self.time_list[i] - s < t_th[i]:
                                i -= 1
                                break
                            else:
                                self.lat1.append(self.latitude[i])
                                self.lon1.append(self.longitude[i])
                                self.ts.append(s)
                                self.te.append(self.time_list[i])
                                i -= 1
                            break
                if i == len(self.latitude) - 1:
                    if self.time_list[i] - s >= t_th[i]:
                        self.lat1.append(self.latitude[i])
                        self.lon1.append(self.longitude[i])
                        self.ts.append(s)
                        self.te.append(self.time_list[i])

        # Trả về danh sách các tọa độ và thời điểm tương ứng
        return self.lat1, self.lon1, self.ts, self.te
# #exam BumpPotholeDetection    
# # Tạo một thể hiện của lớp BumpPotholeDetection
# detection = BumpPotholeDetection(latitude, longitude, velocity_list, az, time_list)
# # Gọi phương thức detect_bumps_potholes() để xác định các bump và pothole
# bumps_lat, bumps_lon, start_times, end_times = detection.detect_bumps_potholes()
    
#-------------------------------------------------------------------------------------------------- 

#--------------------------------------------------------------------------------------------------


class MapVisualization:
    def __init__(self, latitude, longitude, lat, lon, IRI, lat1, lon1, ts, te, mapsave='map.html'):
        self.latitude = latitude
        self.longitude = longitude
        self.lat = lat
        self.lon = lon
        self.IRI = IRI
        self.lat1 = lat1
        self.lon1 = lon1
        self.ts = ts
        self.te = te
        self.mapsave = mapsave
        self.m = folium.Map(location=[latitude[0], longitude[0]], zoom_start=18, control_scale=True)

    def draw_map(self):
        # Thêm lớp bản đồ đất liền
        tile_layer_land = folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            name='Land Map',
            attr='Map data &copy; Google',
            min_zoom=0,
            max_zoom=22
        ).add_to(self.m)
        # Thêm lớp bản đồ vệ tinh vào bản đồ chính
        tile_layer_satellite = folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            name='Satellite Map',
            attr='Map data &copy; Google',
            min_zoom=0,
            max_zoom=22
        ).add_to(self.m)

        # Chấm các điểm trên bản đồ và thêm popup vị trí
        points = []
        point1 = []
        point2 = []
        for i in range(len(self.latitude)):
            points.append([self.latitude[i], self.longitude[i]])
        folium.PolyLine(locations=points, color='yellowgreen', weight=5).add_to(self.m)

        for i in range(len(self.lat)):
            lt, ln = 0, 0
            if 2.8 < self.IRI[i] <= 4 or self.IRI[i] > 4:
                lt = self.lat[i]
                ln = self.lon[i]
                j = i + 1
                while j < len(self.lat) and (2.8 < self.IRI[j] <= 4 or self.IRI[j] > 4):
                    point1.append([lt, ln])
                    point2.append([self.lat[j], self.lon[j]])
                    break
                if point1 and point2:
                    color = 'yellow'
                    if self.IRI[i] > 4:
                        color = 'red'
                    folium.PolyLine(locations=(point1[-1], point2[-1]), color=color, weight=5).add_to(self.m)
                point1 = []
                point2 = []

        for i in range(len(self.lat1)):
            line = folium.CircleMarker(location=[self.lat1[i], self.lon1[i]], radius=1.5, color='black', fill_color='red')
            popup_content = f"Latitude: {self.lat1[i]}<br>Longitude: {self.lon1[i]}<br>Time_start: {self.ts[i]}<br>Time_end: {self.te[i]}"
            popup = folium.Popup(popup_content, max_width=200)
            line.add_child(popup)
            line.add_to(self.m)

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
             
        <div class='legend-title' style='color:black; weight: 500'>IRI(m/km):</div>
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

        self.m.get_root().html.add_child(folium.Element(template))
        folium.LayerControl().add_to(self.m)
        # Thiết lập lớp bản đồ đất liền là lớp mặc định
        self.m.add_child(tile_layer_satellite)
        # Thêm popup vào bản đồ
        self.m.save(self.mapsave)

# #exam MapVisualization
# map_visualization = MapVisualization(latitude, longitude, lat, lon, IRI, lat1, lon1, ts, te)
# map_visualization.draw_map()

#--------------------------------------------------------------------------------------------------

class csv_writing:
    def __init__(self, outputfile_1, outputfile_2):
        self.outputfile_1 = outputfile_1
        self.outputfile_2 = outputfile_2

    def write_to_csv_1(self, time, time_list, latitude, longitude, ax, ay, az, velocity_list, distances, Vh):
        with open(self.outputfile_1, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['time', 'timestamp', 'Latitude', 'Longitude', 'ax', 'ay', 'az', 'v', 's', 'Vh'])
            for i in range(len(time)):
                writer.writerow([time[i], time_list[i], latitude[i], longitude[i], ax[i], ay[i], az[i], velocity_list[i], distances[i], Vh[i]])

    def write_to_csv_2(self, lat, lon, IRI):
        with open(self.outputfile_2, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Lat', 'Lon', 'IRI'])
            for i in range(len(lat)):
                writer.writerow([lat[i], lon[i], IRI[i]])

## exam csv_writing
# data_writer = csv_writing()
# data_writer.write_to_csv_1(time, time_list, latitude, longitude, ax, ay, az, velocity_list, distances, Vh)
# data_writer.write_to_csv_2(lat, lon, IRI)