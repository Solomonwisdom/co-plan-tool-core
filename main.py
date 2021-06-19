#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
main.py
manage module
'''

from copy import deepcopy
from flight import Flight
from core import handle
from relay_core import LATITUDE, LONGITUDE, handle_relay
from output import generate_flight_mission, generate_flight_todolist, small2big, generate_relay
import math

import json
import os
# from multiprocessing import Process
CUR_DIR=os.path.abspath(os.path.dirname(__file__)) + "/"


NUM_OF_POINT = 30
NUM_OF_FLIGHT = 5
SPEED_OF_FLIGHT = 15
INTEL = True

MODEL = 0

POINT = {}
DIST = []
FLIGHT = {}

MISSIONS = []

MISSION_A = []
MISSION_B = []
TODO_LIST = []
POSITION = []
CURRENT_COST = []

CENTER = [0, 0]
RADIUS = 0
VELOCITY = 0

def initialize_point():
    global POINT
    f = open("data/point.txt")
    lines = f.read().splitlines()
    for line in lines:
        temp = line.split(" ")
        POINT[int(temp[0])] = [float(temp[1]), float(temp[2])]
    f.close()

def initialize_dist():
    global DIST
    DIST = [[float(0) for i in range(NUM_OF_POINT)] for j in range(NUM_OF_POINT)]
    f = open("data/route.txt")
    lines = f.read().splitlines()
    for line in lines:
        temp = line.split(" ")
        DIST[int(temp[0])][int(temp[1])] = float(temp[2])
        DIST[int(temp[1])][int(temp[0])] = float(temp[2])
    f.close()

def load_file():
    initialize_point()
    initialize_dist()

def init_center():
    global MISSION_A
    global MISSION_B
    global TODO_LIST
    global POSITION
    global CURRENT_COST
    global FLIGHT
    MISSION_A = []
    MISSION_B = []
    TODO_LIST = []
    POSITION = []
    CURRENT_COST = []
    FLIGHT = {}
    for i in range(NUM_OF_FLIGHT):
        FLIGHT[i] = Flight(deepcopy([118958877.0, 32114745.0]))
        POSITION.append([118958877.0, 32114745.0])
        CURRENT_COST.append(0.0)
        MISSION_A.append([])
        MISSION_B.append([])
        TODO_LIST.append([])

def generate_distance(position):
    cost = {}
    len_of_content = NUM_OF_POINT + 1
    for i in range(NUM_OF_FLIGHT):
        content = [[float(0) for j in range(len_of_content)] for k in range(len_of_content)]
        for j in range(1, len_of_content):
            c = math.sqrt(pow(position[i][0] - POINT[j-1][0], 2) + pow(position[i][1] - POINT[j-1][1], 2)) / SPEED_OF_FLIGHT
            content[0][j] = c
            content[j][0] = c
        for j in range(1, len_of_content):
            for k in range(j+1, len_of_content):
                c = DIST[j-1][k-1] / SPEED_OF_FLIGHT
                content[j][k] = c
                content[k][j] = c
        cost[i] = content
    return deepcopy(cost)

def generate_cost_current(content, flight_id):
    if len(TODO_LIST[flight_id]) == 0:
        return 0.0
    else:
        time_all = 0
        cost_all = 0
        for i in range(len(TODO_LIST[flight_id])):
            point_id = TODO_LIST[flight_id][i]["point"]
            if i == 0:
                time_all += content[0][point_id + 1]
            else:
                time_all += content[TODO_LIST[flight_id][i - 1]["point"] + 1][point_id + 1]
            if "put" in TODO_LIST[flight_id][i].keys():
                cost_all += time_all * len(TODO_LIST[flight_id][i]["put"])
        return cost_all

def initialize_cost():
    ret = {}
    for i in range(NUM_OF_FLIGHT):
        content = [[float(0) for x in range(len(DIST))] for y in range(len(DIST))]
        for j in range(0, len(DIST)):
            for k in range(j+1, len(DIST)):
                content[j][k] = DIST[j][k] / SPEED_OF_FLIGHT
                content[k][j] = DIST[k][j] / SPEED_OF_FLIGHT
        ret[i] = content
    return deepcopy(ret)

def generate_vector():
    ret = []
    for i in range(NUM_OF_FLIGHT):
        tmp = [float(0) for x in range(len(POINT))]
        for j in range(len(POINT)):
            tmp[j] = math.sqrt(pow(POINT[j][0] - POSITION[i][0], 2) + pow(POINT[j][1] - POSITION[i][1], 2)) / SPEED_OF_FLIGHT
        ret.append(tmp)
    return deepcopy(ret)

def manage():
    global TODO_LIST, MISSION_B, CURRENT_COST
    init_center()
    cost = initialize_cost()
    cost_vector = generate_vector()
    for m in MISSIONS:
        TODO_LIST, MISSION_B, CURRENT_COST = handle(m, deepcopy(TODO_LIST), MISSION_A, deepcopy(MISSION_B), cost, cost_vector, NUM_OF_FLIGHT)
    for i in range(NUM_OF_FLIGHT):
        TODO_LIST[i] = small2big(deepcopy(TODO_LIST[i]))
    print(sum(CURRENT_COST))

def solve():
    global MISSIONS
    init_center()
    for m in MISSIONS:
        mission_id = m[0]
        sp = m[1]
        ep = m[2]
        flight_id = mission_id % NUM_OF_FLIGHT
        MISSION_B[flight_id].append(deepcopy(m))
        TODO_LIST[flight_id].append({"point": sp, "get": [mission_id]})
        TODO_LIST[flight_id].append({"point": ep, "put": [mission_id]})
    cost = generate_distance(deepcopy(POSITION))
    for i in range(NUM_OF_FLIGHT):
        CURRENT_COST[i] = generate_cost_current(deepcopy(cost[i]), i)

def generate_boarder():
    boarder = []
    longitude = RADIUS / LONGITUDE
    latitude = RADIUS / LATITUDE
    boarder.append([CENTER[0] - longitude, CENTER[1] + latitude])
    boarder.append([CENTER[0] + longitude, CENTER[1] + latitude])
    boarder.append([CENTER[0] + longitude, CENTER[1] - latitude])
    boarder.append([CENTER[0] - longitude, CENTER[1] - latitude])
    boarder.append([CENTER[0] - longitude, CENTER[1] + latitude])
    return deepcopy(boarder)

load_file()

def handle(event, context):
    tmp = event['data']
    tmp = tmp.decode(("utf-8"))
    if type(tmp)==bytes: 
        tmp = json.loads(tmp)
    if type(tmp) != dict:
        return "Error"
    if "mission" in tmp:
        file_content = tmp['mission']
        first_line = file_content.splitlines()[0]
        print(file_content)
        if len(first_line.split()) == 3 and first_line.split()[0].isdigit():
            global MISSIONS
            MISSIONS = []
            lines = file_content.splitlines()
            for line in lines:
                tmp = line.split()
                MISSIONS.append([int(tmp[0]), int(tmp[1]), int(tmp[2])])
            print(MISSIONS)
            with open(CUR_DIR + "MISSION.json", "w") as f:
                f.write(json.dumps(MISSIONS))
            message = "success"
            response_body = json.dumps({"status": message})
        elif len(first_line.split()) == 3 and first_line.split()[0]=="center":
            global CENTER, RADIUS, VELOCITY
            lines = file_content.splitlines()
            for line in lines:
                tmp = line.split()
                if tmp[0] == "center":
                    CENTER = [float(tmp[1]), float(tmp[2])]
                if tmp[0] == "radius":
                    RADIUS = float(tmp[1])
                if tmp[0] == "velocity":
                    VELOCITY = float(tmp[2])
            # print(CENTER)
            # print(RADIUS)
            # print(VELOCITY)
            circle = {'CENTER': CENTER, 'RADIUS': RADIUS, "VELOCITY": VELOCITY}
            with open(CUR_DIR + "CIRCLE.json", "w") as f:
                json.dump(circle, f)
            message = "success"
            response_body = json.dumps({"status": message})
        else:
            response_body = json.dumps({"status": "fail"})
        return response_body
    else:
        input_from_ui = tmp
        t = input_from_ui["type"]
        if t==0:
            # print(input_from_ui)
            print("Optimization goal: {}".format(input_from_ui['select']))
            # print("Intel algo: {}".format(input_from_ui['switch']))
            global NUM_OF_FLIGHT, INTEL, MODEL
            NUM_OF_FLIGHT = input_from_ui['slider']
            INTEL = input_from_ui['switch']
            if input_from_ui['select'] == "minimize totole waiting time":
                MODEL = 1
            elif input_from_ui['select'] == "100% time continuous coverage":
                MODEL = 2
            all_input = {}
            all_input['MODEL'] = MODEL
            all_input['INTEL'] = INTEL
            all_input['NUM_OF_FLIGHT'] = NUM_OF_FLIGHT
            with open(CUR_DIR + "input.json", "w") as f:
                json.dump(all_input, f)
            response_body = json.dumps({"message": "save success", "model": MODEL})
            return response_body
        if t==1:
            global NUM_OF_FLIGHT, INTEL, MODEL, TODO_LIST, POSITION, MISSIONS 
            with open(CUR_DIR + "MISSION.json", "r") as f:
                MISSIONS = json.load(f)
            if os.path.isfile(CUR_DIR + 'output.json'):
                with open(CUR_DIR + "output.json", "r") as f:
                    content = json.load(f)
                    TODO_LIST = content['TODO_LIST']
                    POSITION = content['POSITION']
            print("planning...")
            input = {}
            with open(CUR_DIR + "input.json", "r") as f:
                input = json.load(f)
            MODEL = input['MODEL']
            NUM_OF_FLIGHT = input['NUM_OF_FLIGHT']
            INTEL = input['INTEL']
            if MODEL == 1:
                if INTEL:
                    manage()
                else:
                    solve()
                flight_mission = generate_flight_mission(NUM_OF_FLIGHT, deepcopy(MISSION_B), deepcopy(CURRENT_COST))
                flight_todolist = generate_flight_todolist(NUM_OF_FLIGHT, TODO_LIST)
                response_body = json.dumps({"todo_list": TODO_LIST, "position": POSITION, "flight_mission": flight_mission, "flight_todolist": flight_todolist})
                all_output = {'TODO_LIST': TODO_LIST, 'POSITION': POSITION}
                with open(CUR_DIR + "output.json","w") as f:
                    json.dump(all_output, f)
                return response_body
            elif MODEL == 2:
                circle = {}
                global CENTER, RADIUS, VELOCITY
                with open(CUR_DIR + "CIRCLE.json", "r") as f:
                    circle = json.load(f)
                CENTER = circle['CENTER']
                RADIUS = circle['RADIUS']
                VELOCITY = circle['VELOCITY']
                MODEL = input['MODEL']
                NUM_OF_FLIGHT = input['NUM_OF_FLIGHT']
                INTEL = input['INTEL']
                boarder = generate_boarder()
                uav = handle_relay(NUM_OF_FLIGHT, deepcopy(CENTER), RADIUS, VELOCITY)
                info = generate_relay(uav)
                response_body = json.dumps({"uav": uav, "info": info, "boarder": boarder})
                return response_body
