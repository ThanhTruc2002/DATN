import csv
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
        
        
acceleration_changes = compute_acceleration_changes(ax, ay, az)
roughness_index = compute_roughness_index(acceleration_changes)
print("Roughness Index:", roughness_index)