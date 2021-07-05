# F1 2020 - The Official Video Game from Codemasters
A tool for forwarding the UDP telemetry data from the simulator game F1 2020 to InfluxDB
for display via ang graphing application.

[UDP Specification](https://forums.codemasters.com/topic/54423-f1%C2%AE-2020-udp-specification/)

# Data Storage
I used [InfluxDB](https://www.influxdata.com/) which is a great time series database.
See [Docker Hub](https://hub.docker.com/_/influxdb).
```bash
docker pull quay.io/influxdb/influxdb:latest
```

# Graphing Using Grafana
I used Grafana to connect to InfluxDB. See - https://grafana.com/docs/grafana/latest/installation/docker/
```bash
docker run -d -p 3000:3000 grafana/grafana
```

## Connection to InfluxDB
Connecting to InfluxDB 2 requires 7.1 and above.

![alt text](images/influxdb_grafana_config_1.png "Top half of config of datasource")
![alt text](images/influxdb_grafana_config_2.png "Bottom half of config of datasource")

## Refresh Rate
To enable sub second updates, alter the following in `/etc/grafana/grafana.ini`

```ini
#################################### Dashboards History ##################
[dashboards]
# Number dashboard versions to keep (per dashboard). Default: 20, Minimum: 1
;versions_to_keep = 20
min_refresh_interval = 100ms
```

Next add the refresh rate as an option in the dashboard setting, otherwise you won't be able
to select it.

![alt text](images/grafana_refresh_rate.png "Set refresh rate")


# Links
* Excellent Telemetry tool [PXG F1](https://bitbucket.org/Fiingon/pxg-f1-telemetry/src)
* Library for reading packets [Python](https://pypi.org/project/f1-2020-telemetry/)
* Similar project using [Kafka](https://www.youtube.com/watch?v=Re9LOAYZi2A) and
  with [Camel](https://www.youtube.com/watch?v=2efOtyFAZ4s)

# Demo
Youtube:
* [Grafana Demo](https://youtu.be/zWDqIcY03e0)


# Imaging Car Position

```python
# print(f'{packet["worldPositionX"]},{packet["worldPositionY"]},'
#       f'{packet["worldPositionZ"]}')

# print(f'{packet["worldPositionX"]}, {packet["worldPositionZ"]}')
maze = io.imread('cassandra/track_layouts/Red_Bull_Ring.png')

# g = ggplot(df) + geom_point(
#     aes(x=NGPSLongitude, y=NGPSLatitude, col=sign(gLat),
#         size=abs(gLat)))
# print(g)

# Pit Exit -48.612972259521484, 218.2395477294922
# Turn 3 (-525.0587158203125, -450.0421142578125)

# GPS: 47.220135, 14.760147
# 47.226171, 14.754152

ax, ay = 2, 442
dx, dy = 0, 75
cx, cy = 300, 750
# Arrow(ay, ax, dy, dx, width=100., color='green'),

patches.append(Circle((packet["worldPositionX"], packet["worldPositionZ"]), radius=2, color='red'))
li.append((packet["worldPositionX"] + 95.8331072,
           packet["worldPositionZ"] - 203.4794))
if len(patches) > 500:
    with open('data_gps.json', 'w') as file:
        file.write(json.dumps(li))
    # print()
    plt.scatter(*zip(*li))
    fig, ax = plt.subplots(1)
    ax.imshow(maze)
    for p in patches:
        ax.add_patch(p)
    plt.show()


https://blog.ouseful.info/2012/03/14/plotting-latitude-and-longitude-with-ggplot-map-projections-in-r/
```

Pit Lane Exit Austria
-48.612972259521484, 218.2395477294922
GPS: 47.220135, 14.760147
