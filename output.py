#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from copy import deepcopy

def generate_flight_mission(n, mb, c):
    ret = []
    for i in range(n):
        tmp = {}
        tmp["key"] = str(i)
        tmp["id"] = str(i)
        tmp["mission"] = ""
        for j in range(len(mb[i])):
            tmp["mission"] += str(mb[i][j][0])
            if j < len(mb[i]) - 1:
                tmp["mission"] += " , "
        tmp["cost"] = "{:.2f}".format(c[i])
        ret.append(tmp)
    return deepcopy(ret)

def generate_flight_todolist(n, td):
    ret = []
    for i in range(n):
        tmp = {}
        tmp["key"] = str(i)
        tmp["id"] = str(i)
        tmp["list"] = ""
        for j in range(len(td[i])):
            tmp["list"] += " -> " + str(td[i][j]["point"]) + " : "
            tmp["list"] += "( "
            if "put" in td[i][j].keys():
                tmp["list"] += "put : "
                for k in range(len(td[i][j]["put"])):
                    tmp["list"] += str(td[i][j]["put"][k]) + " "
            if "get" in td[i][j].keys():
                tmp["list"] += "get : "
                for k in range(len(td[i][j]["get"])):
                    tmp["list"] += str(td[i][j]["get"][k]) + " "
            tmp["list"] += ")"
        ret.append(tmp)
    return deepcopy(ret)

def small2big(todolist):
    ret = []
    for i in range(len(todolist)):
        # start
        if i == 0:
            ret.append(deepcopy(todolist[i]))
            # id -> [id] list
            if "put" in ret[-1].keys():
                ret[-1]["put"] = [todolist[i]["put"]]
            else:
                ret[-1]["get"] = [todolist[i]["get"]]
        else:
            # new point
            if todolist[i]["point"] != ret[-1]["point"]:
                ret.append(deepcopy(todolist[i]))
                if "put" in ret[-1].keys():
                    ret[-1]["put"] = [todolist[i]["put"]]
                else:
                    ret[-1]["get"] = [todolist[i]["get"]]
            # merge point
            else:
                if "put" in todolist[i].keys():
                    if "put" not in ret[-1].keys():
                        ret[-1]["put"] = []
                    ret[-1]["put"].append(todolist[i]["put"])
                if "get" in todolist[i].keys():
                    if "get" not in ret[-1].keys():
                        ret[-1]["get"] = []
                    ret[-1]["get"].append(todolist[i]["get"])
    return deepcopy(ret)

def generate_relay(uav):
    info = []
    for i in range(len(uav)):
        tmp = {}
        tmp["key"] = str(i)
        tmp["id"] = str(i)
        tmp["position"] = "{:.4f} , {:.4f}".format(uav[i]["longitude"], uav[i]["latitude"])
        tmp["center"] = "{:.4f} , {:.4f}".format(uav[i]["move_center"][0], uav[i]["move_center"][1])
        tmp["velocity"] = uav[i]["velocity"]
        tmp["radius"] = uav[i]["r_uav"]
        tmp["route"] = uav[i]["r_move"]
        info.append(tmp)
    return deepcopy(info)