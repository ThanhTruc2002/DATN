import lib_1

filename = './Input/4.csv'
outputfile_1 = 'separated_data.csv'
outputfile_2 = './Result/map_data4.csv'
mapsave = './Map/mapcopy.html'

#Get sensor data
data_processor = lib_1.DataProcessor(filename)
latitude = data_processor.get_latitude()
longitude = data_processor.get_longitude()
time = data_processor.get_time()
time_list = data_processor.get_timestamp()
ax, ay, az = data_processor.get_acceleration()

#Calculate velocity and total distance
total_distance, distances, velocity_list, Vh = data_processor.calculate_velocity_distance()

#Calculate IRI
calculate_IRI = lib_1.IRICalculation(latitude, longitude, Vh, total_distance)
IRI, lat, lon = calculate_IRI.calculate_IRI()

#Detect pothole
detect_pothole = lib_1.BumpPotholeDetection(latitude, longitude, velocity_list, az, time_list)
lat1, lon1, ts, te = detect_pothole.detect_bumps_potholes()

#Map visualization
map = lib_1.MapVisualization(latitude, longitude, lat, lon, IRI, lat1, lon1, ts, te, mapsave=mapsave)
map.draw_map()

#Result 
data_writer = lib_1.csv_writing(outputfile_1, outputfile_2)
data_writer.write_to_csv_1(time, time_list, latitude, longitude, ax, ay, az, velocity_list, distances, Vh)
data_writer.write_to_csv_2(lat, lon, IRI)

print("S:", total_distance)


