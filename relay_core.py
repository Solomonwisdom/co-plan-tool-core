#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import math

from copy import deepcopy

from assign import assign

LONGITUDE = 94120
LATITUDE = 111120

def get1(center, radius, velocity):
    r_uav = 1.62 * radius
    r_move = 0.2 * radius
    x = center[0] + (r_move * math.sin(velocity * 0 / r_move)) / LONGITUDE
    y = center[1] + (r_move * math.cos(velocity * 0 / r_move)) / LATITUDE
    return [{"key": 0, "longitude": x, "latitude": y, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center}]

def get2(center, radius, velocity):
    r_uav = 1.5 * radius
    r_move = 0.5 * radius
    x1 = center[0] + (r_move * math.sin(velocity * 0 / r_move)) / LONGITUDE
    y1 = center[1] + (r_move * math.cos(velocity * 0 / r_move)) / LATITUDE
    x2 = center[0] + (r_move * math.sin(velocity * 0 / r_move + math.pi)) / LONGITUDE
    y2 = center[1] + (r_move * math.cos(velocity * 0 / r_move + math.pi)) / LATITUDE
    return [{"key": 1, "longitude": x1, "latitude": y1, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center},
            {"key": 1, "longitude": x2, "latitude": y2, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center}]

def get3(center, radius, velocity):
    r_uav = 1.23 * radius
    r_move = 0.75 * radius
    x1 = center[0] + (r_move * math.sin(velocity * 0 / r_move)) / LONGITUDE
    y1 = center[1] + (r_move * math.cos(velocity * 0 / r_move)) / LATITUDE
    x2 = center[0] + (r_move * math.sin(velocity * 0 / r_move + math.pi * 2 / 3)) / LONGITUDE
    y2 = center[1] + (r_move * math.cos(velocity * 0 / r_move + math.pi * 2 / 3)) / LATITUDE
    x3 = center[0] + (r_move * math.sin(velocity * 0 / r_move + math.pi * 4 / 3)) / LONGITUDE
    y3 = center[1] + (r_move * math.cos(velocity * 0 / r_move + math.pi * 4 / 3)) / LATITUDE
    return [{"key": 2, "longitude": x1, "latitude": y1, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center},
            {"key": 2, "longitude": x2, "latitude": y2, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center},
            {"key": 2, "longitude": x3, "latitude": y3, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center}]

def get4(center, radius, velocity):
    r_uav = 1 * radius
    r_move = 1 * radius
    x1 = center[0] + (r_move * math.sin(velocity * 0 / r_move)) / LONGITUDE
    y1 = center[1] + (r_move * math.cos(velocity * 0 / r_move)) / LATITUDE
    x2 = center[0] + (r_move * math.sin(velocity * 0 / r_move + math.pi * 1 / 2)) / LONGITUDE
    y2 = center[1] + (r_move * math.cos(velocity * 0 / r_move + math.pi * 1 / 2)) / LATITUDE
    x3 = center[0] + (r_move * math.sin(velocity * 0 / r_move + math.pi)) / LONGITUDE
    y3 = center[1] + (r_move * math.cos(velocity * 0 / r_move + math.pi)) / LATITUDE
    x4 = center[0] + (r_move * math.sin(velocity * 0 / r_move + math.pi * 3 / 2)) / LONGITUDE
    y4 = center[1] + (r_move * math.cos(velocity * 0 / r_move + math.pi * 3 / 2)) / LATITUDE
    return [{"key": 3, "longitude": x1, "latitude": y1, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center},
            {"key": 3, "longitude": x2, "latitude": y2, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center},
            {"key": 3, "longitude": x3, "latitude": y3, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center},
            {"key": 3, "longitude": x4, "latitude": y4, "r_uav": r_uav, "r_move": r_move, "velocity": velocity, "move_center": center}]

FUNC = [get1, get2, get3, get4]

def handle_relay(n, center, radius, velocity):
    uav = []
    if n <= 4:
        res = FUNC[n-1](center, radius, velocity)
        for i in res:
            uav.append(i)
    else:
        r = radius / 2
        longitude = r / LONGITUDE
        latitude = r / LATITUDE
        center1 = [center[0] - longitude, center[1] + latitude]
        center2 = [center[0] + longitude, center[1] + latitude]
        center3 = [center[0] + longitude, center[1] - latitude]
        center4 = [center[0] - longitude, center[1] - latitude]
        res1 = FUNC[assign[n][0] - 1](center1, r, velocity)
        res2 = FUNC[assign[n][1] - 1](center2, r, velocity)
        res3 = FUNC[assign[n][2] - 1](center3, r, velocity)
        res4 = FUNC[assign[n][3] - 1](center4, r, velocity)
        for i in res1 + res2 + res3 + res4:
            uav.append(i)
    return deepcopy(uav)