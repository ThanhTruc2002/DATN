import lib_1


filename = './Input/4.csv'

data_processor = lib_1.DataProcessor(filename)
lat = data_processor.get_latitude()
lon = data_processor.get_longitude()
time = data_processor.get_time()
ax, ay, az = data_processor.get_acceleration()

print("Latitude:", lat)
print("Longitude:", lon)
print("Time:", time)
print("Acceleration (ax):", ax)
print("Acceleration (ay):", ay)
print("Acceleration (az):", az)

calculator = lib_1.Calculator()
velocity = calculator.calculate_velocity()
Vh = calculator.calculate_IRI()
total_distance = calculator.calculate_distance()