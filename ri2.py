import csv
import matplotlib.pyplot as plt

def compute_acceleration_changes(ax, ay, az):
    acceleration_changes = []

    for i in range(1, len(ax)):
        delta_ax = ax[i] - ax[i-1]
        delta_ay = ay[i] - ay[i-1]
        delta_az = az[i] - az[i-1]
        acceleration_changes.append((delta_ax, delta_ay, delta_az))

    return acceleration_changes


def compute_roughness_index(acceleration_changes):
    absolute_changes = [max(abs(change[0]), abs(change[1]), abs(change[2])) for change in acceleration_changes]
    roughness_index = sum(absolute_changes) / (len(acceleration_changes) - 1)
    return roughness_index


filename = "imu1.csv"
ax = []
ay = []
az = []

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ax.append(float(row[0]))
        ay.append(float(row[1]))
        az.append(float(row[2]))

segment_length = 9  # Độ dài của mỗi phân đoạn

roughness_indices = []
num_segments = len(ax) // segment_length

for i in range(num_segments):
    start_index = i * segment_length
    end_index = start_index + segment_length
    segment_acceleration_changes = compute_acceleration_changes(ax[start_index:end_index],
                                                                ay[start_index:end_index],
                                                                az[start_index:end_index])
    segment_roughness_index = compute_roughness_index(segment_acceleration_changes)
    roughness_indices.append(segment_roughness_index)
    print("Roughness Index of Segment", i+1, ":", segment_roughness_index)
    
distances = []
v=13
for i in range(num_segments):
    distance = (segment_length/10) * v 
    distances.append(distance)
    print("Length:", distance)

print("Roughness Indices:", roughness_indices)

# Vẽ đồ thị
segment_numbers = list(range(1, num_segments + 1))
plt.plot(segment_numbers, roughness_indices)
plt.xlabel('Segment Number')
plt.ylabel('Roughness Index')
plt.title('Roughness Index for Segments')
plt.show()