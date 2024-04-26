
import csv
import scipy.integrate as spi

av = []
t_s = []
t_e = []
lat = []
lon = []

def calculate_IRI(S,av, ts, te):
    b = te - ts
    # Tính vận tốc
    velocity = av * b

    # Tính quãng đường
    distance = spi.quad(lambda t: velocity, 0, b)[0]
    index = distance / S

    return index

filename = "separated_data1.csv"

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)

    for row in reader:
        av.append(float(row[7]))
        t_s.append(float(row[0]))
        t_e.append(float(row[1]))
        lat.append(float(row[2]))
        lon.append(float(row[3]))

IRI = []
S=1.49
for i in range(len(lat)):
    index = calculate_IRI(S,av[i], t_s[i], t_e[i])
    IRI.append(index)

with open('IRI.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Start', 'Stop', 'Lat', 'Lon', 'av', 'IRI'])
    for i in range(len(av)):
        writer.writerow([t_s[i], t_e[i], lat[i], lon[i], av[i], IRI[i]])
