import math
import matplotlib.pyplot as plt


## Creating 15 waypoints
waypoints = [
    {'lat': 12.9716, 'lon': 77.5946, 'alt': 50},
    {'lat': 12.9720, 'lon': 77.5950, 'alt': 50},
    {'lat': 12.9725, 'lon': 77.5955, 'alt': 50},
    {'lat': 12.9730, 'lon': 77.5960, 'alt': 50},
    {'lat': 12.9735, 'lon': 77.5965, 'alt': 50},
    {'lat': 12.9740, 'lon': 77.5970, 'alt': 50},
    {'lat': 12.9745, 'lon': 77.5975, 'alt': 50},
    {'lat': 12.9750, 'lon': 77.5980, 'alt': 50},
    {'lat': 12.9755, 'lon': 77.5985, 'alt': 50},
    {'lat': 12.9760, 'lon': 77.5990, 'alt': 50},
    {'lat': 12.9765, 'lon': 77.5995, 'alt': 50},
    {'lat': 12.9770, 'lon': 77.6000, 'alt': 50},
    {'lat': 12.9775, 'lon': 77.6005, 'alt': 50},
    {'lat': 12.9780, 'lon': 77.6010, 'alt': 50},
    {'lat': 12.9785, 'lon': 77.6015, 'alt': 50}
]

## Calculating distance using haversine formula 
def haversine(
        lat1,
        lon1,
        lat2,
        lon2
):

    R = 6371000

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
            math.sin(dlat / 2) ** 2
            +
            math.cos(lat1)
            *
            math.cos(lat2)
            *
            math.sin(dlon / 2) ** 2
    )

    c = (
            2
            *
            math.atan2(
                math.sqrt(a),
                math.sqrt(1 - a)
            )
    )

    distance = R * c

    return distance


## total mission distance from start to goal
def total_mission_distance(
        mission
):

    distance = 0

    for i in range(
            len(mission)-1
    ):

        wp1 = mission[i]
        wp2 = mission[i+1]

        distance += haversine(
            wp1['lat'],
            wp1['lon'],
            wp2['lat'],
            wp2['lon']
        )

    return distance


## Remaining distance 
def remaining_distance(
        mission,
        current_index
):

    distance = 0

    for i in range(
            current_index,
            len(mission) - 1
    ):

        wp1 = mission[i]
        wp2 = mission[i + 1]

        distance += haversine(
            wp1['lat'],
            wp1['lon'],
            wp2['lat'],
            wp2['lon']
        )

    return distance


## Initial mission distance
mission_distance = total_mission_distance(
    waypoints
)

print(
    "Initial Mission Distance:",
    round(mission_distance, 2),
    "meters"
)


## Inserting new waypoints
wp10 = waypoints[9]
wp11 = waypoints[10]

dx = (
        wp11['lat']
        -
        wp10['lat']
)

dy = (
        wp11['lon']
        -
        wp10['lon']
)

length = math.sqrt(
    dx ** 2 +
    dy ** 2
)

dx = dx / length
dy = dy / length

## perpendicular vector
px = -dy
py = dx

## converting 100m to degree
meters_to_degree = (
        100
        /
        111320
)


## creating new waypoint
new_wp = {

    'lat':
        wp10['lat']
        +
        px
        *
        meters_to_degree,

    'lon':
        wp10['lon']
        +
        py
        *
        meters_to_degree,

    'alt':
        wp10['alt']
}

## insert after waypoint 10
waypoints.insert(
    10,
    new_wp
)

print()
print("Inserted Waypoint")
print(new_wp)


## simulating Auto Mode
speed = 5

print()
print("Starting Mission...")

for i in range(
        len(waypoints)
):

    current_wp = waypoints[i]

    print()
    print(
        f"Reached WP{i+1}"
    )

    print(
        f"Lat : {current_wp['lat']}"
    )
    print(
        f"Lon : {current_wp['lon']}"
    )
    print(
        f"Alt : {current_wp['alt']}"
    )

    remaining = remaining_distance(
        waypoints,
        i
    )

    eta = (
            remaining/speed
    )

    print(
        f"Remaining Distance : "
        f"{remaining:.2f} m"
    )

    print(
        f"ETA : "
        f"{eta:.2f} sec"
    )


## Final mission distance including inserted waypoint
final_distance = total_mission_distance(
    waypoints
)

print()
print(
    "Final Mission Distance:",
    round(final_distance, 2),
    "meters"
)


## 2D visualization
latitudes = []
longitudes = []

for wp in waypoints:

    latitudes.append(
        wp['lat']
    )

    longitudes.append(
        wp['lon']
    )


plt.figure(
    figsize=(8, 8)
)

plt.plot(
    longitudes,
    latitudes,
    '-o'
)

## Start Point
plt.scatter(
    longitudes[0],
    latitudes[0],
    marker='o',
    s=150,
    label='Start'
)

## Goal Point
plt.scatter(
    longitudes[-1],
    latitudes[-1],
    marker='*',
    s=250,
    label='Goal'
)


## Inserted Waypoitn
plt.scatter(
    new_wp['lon'],
    new_wp['lat'],
    marker='s',
    s=200,
    label='Inserted WP'
)


## Labelling all 
plt.xlabel(
    'Longitude'
)
plt.ylabel(
    'Latitude'
)
plt.title(
    'Drone Mission Path'
)

plt.grid(True)

plt.legend()

plt.show()