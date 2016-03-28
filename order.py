#!/usr/bin/python
import json
from pprint import pprint
import math, os, unittest
from datetime import date

out = []
win = []
nodes = []


def get_node_with_id(id):
    for node in nodes:
        if node["id"] == id:
            return node
    return null

def get_adj_nodes(node, way):
    ret = []
    waylen = len(way["nodes"])
    idx = way["nodes"].index(node["id"])
    if idx > 0:
        ret.append(get_node_with_id(way["nodes"][idx-1]))
    if idx < waylen - 1:
        ret.append(get_node_with_id(way["nodes"][idx+1]))

    return ret

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180 to + 180 which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


with open('nodes_in_ways.json') as data_file:
    win = json.load(data_file)

with open('nodes.json') as data_file:
    nodes = json.load(data_file)

with open('ways_in_nodes.json') as data_file:
    data = json.load(data_file)
    for node in data:
        if not "ways" in node:
            continue
        if len(node["ways"]) < 2:
            continue
            # pass
        outObj = {}
        outObj["id"] = node["id"]
        outObj["turns"] = []

        for way1 in node["ways"]:
            nearNodes1 = get_adj_nodes(node, way1)
            for nearNode1 in nearNodes1:
                for way2 in node["ways"]:
                    nearNodes2 = get_adj_nodes(node, way2)
                    for nearNode2 in nearNodes2:
                        devObj = {}
                        devObj["fromId"] = nearNode1["id"]
                        devObj["toId"] = nearNode2["id"]
                        devObj["fromMag"] = calculate_initial_compass_bearing((nearNode1["lat"], nearNode1["lon"]), (node["lat"], node["lon"]))
                        devObj["toMag"] = calculate_initial_compass_bearing((node["lat"], node["lon"]), (nearNode2["lat"], nearNode2["lon"]))
                        devObj["turnAngle"] = (devObj["toMag"] - devObj["fromMag"]) % 360
                        outObj["turns"].append(devObj)
        out.append(outObj)

with open('turns.json', 'w') as fp:
    json.dump(out, fp, sort_keys=True, indent=4)
