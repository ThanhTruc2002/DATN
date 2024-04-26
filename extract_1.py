import rosbag
import sys

def extract_data_from_rosbag(rosbag_file, secs):
    longitude = None
    latitude = None
    linear_acceleration = None
    with rosbag.Bag(rosbag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=['/imu', '/gps_fix']):
            if topic == '/imu' and msg.header.stamp.secs == secs:
                linear_acceleration = msg.linear_acceleration
            elif topic == '/gps_fix' and msg.header.stamp.secs == secs:
                latitude = msg.latitude
                longitude = msg.longitude

    if longitude is not None and latitude is not None and linear_acceleration is not None:
        return longitude, latitude, linear_acceleration
    return None, None, None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_data.py <path_to_rosbag_file> <desired_secs>")
        sys.exit(0)

    rosbag_file = sys.argv[1]
    desired_secs = int(sys.argv[2])
    longitude, latitude, linear_acceleration = extract_data_from_rosbag(rosbag_file, desired_secs)
    if longitude is not None and latitude is not None and linear_acceleration is not None:
        print(f"Seconds: {desired_secs}\nLongitude: {longitude}\nLatitude: {latitude}\nLinear Acceleration: {linear_acceleration}")
    else:
        print(f"No data found for the given seconds: {desired_secs}")