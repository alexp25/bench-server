import matplotlib.pyplot as plt
import csv
import copy
import numpy as np

folder = "field test 1"
file = "log.csv"

headers = None

with open(folder + "/headers.csv", 'r') as csvfile:
    headers1 = csv.reader(csvfile, delimiter=",")
    for row in headers1:
        headers = row

print(headers)


class ContainerElement:
    def __init__(self):
        self.label = ""
        self.key = None
        self.color = ""
        self.plot = False
        self.marker = None
        self.index = -1
        self.data = []


m = [
    {
        'label': 'x',
        'key': 'timestamp',
        'color': ''
    },
    {
        'label': 'calibrated heading',
        'key': 'calibratedHeading',
        'disp': True,
        'color': 'blue'
    },
    {
        'label': 'gyro heading',
        'key': 'gyroHeading',
        'disp': True,
        # 'marker': '+',
        'color': 'red'
    },
    {
        'label': 'compass heading',
        'key': 'compassHeading',
        'disp': True,
        'color': 'green'
    },
    {
        'label': 'lat',
        'key': 'lat',
        'disp': False,
        'color': 'green'
    },
    {
        'label': 'lng',
        'key': 'lng',
        'disp': False,
        'color': 'green'
    },
    {
        'label': 'dx',
        'key': 'dx',
        'disp': False,
        'color': 'green'
    },
    {
        'label': 'dy',
        'key': 'dy',
        'disp': False,
        'color': 'green'
    },
    {
        'label': 'diff',
        'disp': False,
        'color': 'green'
    }
]


def get_mc_by_key(mc, key):
    for m in mc:
        if m.key == key:
            return m
    return None

def get_mc_by_label(mc, key):
    for m in mc:
        if m.label == key:
            return m
    return None

mc = []

for (index, key) in enumerate(headers):
    new_elem = ContainerElement()
    new_elem.key = key
    new_elem.index = -1
    for (index2, e) in enumerate(m):
        if 'key' in e and e['key'] == key:
            new_elem.index = index
            new_elem.label = e['label']
            new_elem.color = e['color']
            if 'disp' in e:
                new_elem.plot = e['disp']
            if 'marker' in e:
                new_elem.marker = e['marker']
            break

    new_elem.data = []
    mc.append(new_elem)


print(', '.join(str(e.index) for e in mc))

with open(folder + "/" + file, 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        row_length = len(row)
        # print(row)
        for (index, e) in enumerate(mc):
            if e.index != -1 and e.index < row_length:
                d = float(row[e.index])
                e.data.append(d)

colors = []
for e in mc:
    if e.plot:
        colors.append(e.color)

print(colors)
plt.gca().set_color_cycle(colors)

time_axis = get_mc_by_key(mc, 'timestamp').data
# print(x)

x1 = np.array(time_axis)
x1 = (x1 - np.min(x1))/1000
time_axis = list(x1)


# diff = get_mc_by_label(mc, 'diff')
# d1 = get_mc_by_key(mc, 'compassHeading')
# d2 = get_mc_by_key(mc, 'gyroHeading')
# d1 = np.array(d1.data)
# d2 = np.array(d2.data)
# diff.data = list(d2 - d1)


wp_lat = get_mc_by_key(mc, 'lat').data
wp_lng = get_mc_by_key(mc, 'lng').data
wp_x = get_mc_by_key(mc, 'dx').data
wp_y = get_mc_by_key(mc, 'dy').data

# print(wp_lng)

def deg_to_rad(deg):
    return deg * np.pi / 180

def rad_to_deg(rad):
    return rad * 180 / np.pi

def get_distance_between_earth_coords(lat1, lng1, lat2, lng2):
    earthRadius = 6371000 # meters
    phi1 = deg_to_rad(lat1)
    phi2 = deg_to_rad(lat2)
    delta_phi = deg_to_rad(lat2 - lat1)
    delta_lambda = deg_to_rad(lng2 - lng1)

    a = np.sin(delta_phi/2)**2 + np.cos(phi1)*np.cos(phi2)*(np.sin(delta_lambda/2)**2)
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return earthRadius * c

def get_distance_between_earth_coords_on_axis(lat1, lng1, lat2, lng2):
    earthRadius = 6371000 # meters
    dx = 2*np.pi*earthRadius*np.cos(lat1)*(lng2-lng1)/360
    dy = 2*np.pi*earthRadius*(lat2-lat1)/360
    return dx, dy

def get_point_on_heading(lat1, lng1, distance, heading):
    t = deg_to_rad(heading)
    # r = rad_to_deg(distance)
    r = distance * 0.000008998719243599958
    deltax = r * np.cos(t)
    deltay = r * np.sin(t)

    lat2 = lat1 + deltax
    lng2 = lng1 + deltay
    return (lat2, lng2)


def get_total_distance_gps(wp_lat, wp_lng):
    total_distance = 0
    for (i, wp) in enumerate(wp_lat):
        if i < len(wp_lat) - 1:
            segment_distance = get_distance_between_earth_coords(wp_lat[i], wp_lng[i], wp_lat[i + 1], wp_lng[i + 1])
            total_distance += segment_distance

    return total_distance


def reconstruct_trajectory(wp_lat, wp_lng, heading, timestamp):
    total_distance = 0
    wp_lat_recon = []
    wp_lng_recon = []
    wp_x_recon = [0]
    wp_y_recon = [0]
    # print(wp_lat)
    segment_distance_calculated = 0
    for (i, wp) in enumerate(wp_lat):
        if i < len(wp_lat) - 1:
            segment_distance = get_distance_between_earth_coords(wp_lat[i], wp_lng[i], wp_lat[i+1], wp_lng[i+1])
            segment_speed = segment_distance / (timestamp[i+1] - timestamp[i])

            # segment_distance_axis = get_distance_between_earth_coords_on_axis(wp_lat[i], wp_lng[i], wp_lat[i+1], wp_lng[i+1])
            total_distance += segment_distance

        if i == 0:
            # start recon
            wp_lat_recon.append(wp_lat[i])
            wp_lng_recon.append(wp_lng[i])
        else:
            # reconstruct the current waypoint from the prev waypoint and heading, distance data
            # get the segment distance from the gps speed and time diff
            # because the segment distance is from the gps and we assume that the trajectory should be based only on internal sensors

            wp_new = get_point_on_heading(wp_lat_recon[i - 1], wp_lng_recon[i - 1], segment_distance, heading[i-1])
            wp_lat_recon.append(wp_new[0])
            wp_lng_recon.append(wp_new[1])

            segment_distance_axis_recon = get_distance_between_earth_coords_on_axis(wp_lat_recon[i - 1], wp_lng_recon[i - 1], wp_lat_recon[i], wp_lng_recon[i])
            # segment_distance_calculated = segment_distance / (timestamp[i + 1] - timestamp[i])

            wp_x_recon.append(wp_x_recon[i - 1] + segment_distance_axis_recon[0])
            wp_y_recon.append(wp_y_recon[i - 1] + segment_distance_axis_recon[1])

            # print(segment_distance, segment_distance_calculated)

    return wp_lat_recon, wp_lng_recon, wp_x_recon, wp_y_recon, total_distance


def get_xyz_trajectory(wp_lat, wp_lng):
    wp_x_recon = [0]
    wp_y_recon = [0]
    # print(wp_lat)
    for (i, wp) in enumerate(wp_lat):
        if i < len(wp_lat) - 1:
            segment_distance_axis = get_distance_between_earth_coords_on_axis(wp_lat[i], wp_lng[i], wp_lat[i + 1],
                                                                              wp_lng[i + 1])
        if i == 0:
            pass
        else:
            # reconstruct the current waypoint from the prev waypoint and heading, distance data
            wp_x_recon.append(wp_x_recon[i - 1] + segment_distance_axis[0])
            wp_y_recon.append(wp_y_recon[i - 1] + segment_distance_axis[1])

    return wp_x_recon, wp_y_recon


recon1 = reconstruct_trajectory(wp_lat, wp_lng, get_mc_by_key(mc, 'compassHeading').data, time_axis)
recon = reconstruct_trajectory(wp_lat, wp_lng, get_mc_by_key(mc, 'calibratedHeading').data, time_axis)
recon2 = reconstruct_trajectory(wp_lat, wp_lng, get_mc_by_key(mc, 'gyroHeading').data, time_axis)
# print(recon[0])

absolute_trajectory = get_xyz_trajectory(wp_lat, wp_lng)

dist1 = get_total_distance_gps(wp_lat, wp_lng)
dist2 = get_total_distance_gps(recon[0], recon[1])
print(dist1)
print(dist2)

# print(recon[0])

# diff = np.array(recon[3]) - np.array(absolute_trajectory[1])
# print(diff)

def plot_timeseries():

    samples = None
    # samples = 1000

    if samples is not None:
        x = time_axis[0:samples]
    else:
        x = time_axis

    for (index, e) in enumerate(mc):
        if samples is not None:
            e.data = e.data[0:samples]

        # print(e.key)
        if e.plot:
            if e.marker is not None:
                plt.plot(x, e.data, label=e.label, marker=e.marker)
            else:
                plt.plot(x, e.data, label=e.label)

    plt.xlabel('time (s)')
    plt.ylabel('heading (deg)')

    # plt.legend(['y', 'yp', 'yref'], loc='upper left')

    plt.title('Experimental data')
    plt.legend()
    save_plot(plt)
    plt.show()


def plot_trajectory(x, y, label, color):
    if color is not None:
        plt.plot(x, y, label=label, color=color)
    else:
        plt.plot(x, y, label=label)

def plot_trajectory_experiment():
    # plot_trajectory(absolute_trajectory[0], absolute_trajectory[1], "absolute")
    # plot_trajectory(recon[2], recon[3], "calibrated heading")
    plot_trajectory(wp_x, wp_y, "path from calibrated heading (app)", color="blue")
    # plot_trajectory(recon1[2], recon1[3], "compass heading")
    plot_trajectory(recon2[2], recon2[3], "path from gyro heading", color="red")

    plt.xlabel('dx (meters)')
    plt.ylabel('dy (meters)')

    plt.legend()
    save_plot(plt)
    plt.show()


def plot_trajectory_experiment_1(plot_lng):
    print(wp_x)
    plt.plot(time_axis, absolute_trajectory[1 if plot_lng else 0], label="absolute path", color="green")
    plt.plot(time_axis, wp_y if plot_lng else wp_x, label="path from calibrated heading (app)", color="blue")
    # plt.plot(time_axis, recon[3 if plot_lng else 2], label="calibrated heading")
    plt.plot(time_axis, recon1[3 if plot_lng else 2], label="path from compass heading", color="orange")
    plt.plot(time_axis, recon2[3 if plot_lng else 2], label="path from gyro heading", color="red")
    # plt.plot(x, wp_lng, label="absolute")
    # plt.plot(x, recon[2], label="sensor")

    plt.xlabel('time (s)')
    plt.ylabel('dx (meters)')

    plt.legend()
    save_plot(plt)
    plt.show()

def save_plot(plt):
    plt.savefig('result.png', format='png', dpi=1200)

def plot_check_sampling_rate():
    ns = len(time_axis)
    x = [i for i in range(ns)]
    sampling_time_avg = 0
    for (i, s) in enumerate(time_axis):
        if i != 0:
            sampling_time_avg += time_axis[i] - time_axis[i-1]
    sampling_time_avg /= len(time_axis) - 1
    sampling_rate_avg = 1/sampling_time_avg

    print(str(sampling_time_avg*1000) + " ms" + " / " + str(sampling_rate_avg) + " fps")
    plt.plot(x, time_axis, label="timestamp")
    save_plot(plt)
    plt.show()


# plot_timeseries()
# plot_trajectory_experiment_1(True)
plot_trajectory_experiment()
# plot_check_sampling_rate()



