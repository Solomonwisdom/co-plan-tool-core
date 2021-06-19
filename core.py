#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
core.py
manage core module
'''

from copy import deepcopy

MAX_WEIGHT = 100000000

def generate_before_cost(cost_vector, cost, todolist, num):
    ret = []
    for i in range(num):
        if len(todolist[i]) == 0:
            ret.append(0.0)
        else:
            flight_time = 0
            cost_time = 0
            for j in range(len(todolist[i])):
                point_id = todolist[i][j]["point"]
                if j == 0:
                    # current position to point 0
                    flight_time += cost_vector[i][point_id]
                else:
                    # point i-1 to point i
                    flight_time += cost[i][todolist[i][j - 1]["point"]][point_id]
                # cost += flight_time * 1
                if "put" in todolist[i][j].keys():
                    cost_time += flight_time
            ret.append(cost_time)
    return deepcopy(ret)

def generate_cost1(cost_vector, todolist, cost):
    flight_time = 0
    cost_time = 0
    for i in range(len(todolist)):
        point_id = todolist[i]["point"]
        # start point
        if i == 0:
            flight_time += cost_vector[point_id]
        # mid point
        else:
            flight_time += cost[todolist[i - 1]["point"]][point_id]
        if "put" in todolist[i].keys():
            cost_time += flight_time
    return cost_time, flight_time

def generate_cost2(todolist, upbound, cost1, flight1, point, cost):
    flight_time = flight1
    cost_time = cost1
    for i in range(len(todolist)):
        point_id = todolist[i]["point"]
        # start point
        if i == 0:
            flight_time += cost[point][point_id]
        # mid point
        else:
            flight_time += cost[todolist[i - 1]["point"]][point_id]
        if "put" in todolist[i].keys():
            cost_time += flight_time
        # stop early
        if cost_time > upbound:
            return MAX_WEIGHT * 2
    return cost_time

def generate_after_cost(cost_vector, cost, todolist, num):
    # cost
    ret = []
    for i in range(num):
        if len(todolist[i]) == 0:
            ret.append(0.0)
        else:
            flight_time = 0
            cost_time = 0
            for j in range(len(todolist[i])):
                point_id = todolist[i][j]["point"]
                if j == 0:
                    flight_time += cost_vector[i][point_id]
                else:
                    flight_time += cost[i][todolist[i][j - 1]["point"]][point_id]
                if "put" in todolist[i][j].keys():
                    cost_time += flight_time
            ret.append(cost_time)
    return deepcopy(ret)

def test(cost_vector, todolist, a, b, cost):
    time_all = 0
    cost_all = 0
    for i in range(len(todolist)):
        point_id = todolist[i]["point"]
        # start point
        if i == 0:
            time_all += cost_vector[point_id]
        # mid point
        else:
            time_all += cost[todolist[i - 1]["point"]][point_id]
        if "put" in todolist[i].keys():
            a_ = deepcopy([k[0] for k in a])
            # not get yet
            if todolist[i]["put"] not in a_:
                return MAX_WEIGHT
            cost_all += time_all
            finish = []
            for j in range(len(a)):
                if a[j][0] == todolist[i]["put"]:
                    finish.append(a[j])
            for j in range(len(finish)):
                a.remove(finish[j])
        if "get" in todolist[i].keys():
            start = []
            for j in range(len(b)):
                if b[j][0] == todolist[i]["get"]:
                    start.append(b[j])
            for j in range(len(start)):
                b.remove(start[j])
                a.append(start[j])
    return cost_all

def addition(after_cost, cost_vector, todolist, a, b, cost, num):
    for i in range(num):
        for j in range(1):
            for k in range(0, len(todolist[i])):
                for l in range(k+1, len(todolist[i])):
                    tmp = deepcopy(todolist[i][0:k]) + deepcopy([todolist[i][l]]) + deepcopy(todolist[i][k + 1:l]) + deepcopy([todolist[i][k]]) + deepcopy(todolist[i][l + 1:])
                    ma = deepcopy(a[i])
                    mb = deepcopy(b[i])
                    new = test(cost_vector[i], tmp, deepcopy(ma), deepcopy(mb), cost[i])
                    if new < after_cost[i]:
                        after_cost[i] = new
                        todolist[i] = deepcopy(tmp)

    return deepcopy(after_cost), deepcopy(todolist)

def handle(m, todolist, a, b, cost, cost_vector, num):
    # generate before cost
    before_cost = generate_before_cost(cost_vector, cost, todolist, num)
    index = -1
    min_delta = MAX_WEIGHT
    temp_todo = []
    # insertion greedy
    for i in range(num):
        for j in range(0, len(todolist[i]) + 1):
            tmp1 = todolist[i][0:j] + [{"point":m[1],"get":m[0]}]
            cost1, flight1 = generate_cost1(cost_vector[i], tmp1, cost[i])
            if cost1 == MAX_WEIGHT:
                continue
            for k in range(j, len(todolist[i]) + 1):
                bound = before_cost[i] + min_delta
                tmp2 = todolist[i][j:k] + [{"point":m[2],"put":m[0]}] + todolist[i][k:]
                new_delta = generate_cost2(tmp2, bound, cost1, flight1, m[1], cost[i]) - before_cost[i]
                if new_delta < min_delta:
                    min_delta = new_delta
                    index = i
                    temp_todo = deepcopy(tmp1 + tmp2)
    assert(index != -1)
    todolist[index] = deepcopy(temp_todo)
    b[index].append(deepcopy(m))
    # generate after cost
    after_cost = generate_after_cost(cost_vector, cost, todolist, num)
    new_cost, todolist = addition(deepcopy(after_cost), cost_vector, deepcopy(todolist), a, b, cost, num)
    return deepcopy(todolist), deepcopy(b), deepcopy(new_cost)