#!/usr/bin/python
# -*- coding: utf-8 -*-
# from collections import namedtuple
# Tree = mutabletuple('vertex', ['index', 'value', 'room', 'estimate', 'choice',
# 'level', 'positive', 'ls_index', 'rs_index'])
# positive: 0 - не можем идти дальше(нет смысла), 1 - можем идти дальше, 2 - действующее решение с максимальной ценой
# vertex_max - строка из 'choice' и value


import math


class Vertex:

    def __init__(vrtx, value, room, estimate, choice, level, positive, lson_id, rson_id):

        vrtx.value = value
        vrtx.room = room
        vrtx.estimate = estimate
        vrtx.choice = choice
        vrtx.level = level
        vrtx.positive = positive
        vrtx.lson_id = lson_id
        vrtx.rson_id = rson_id

    def vertex_attributes(vrtx):
        print('Цена рюкзака: {}'.format(vrtx.value))
        print('Вес свободного места: {}'.format(vrtx.room))
        print('Оценка цены рюкзака: {}'.format(vrtx.estimate))
        print('Выбор элементов: {}'.format(vrtx.choice))
        print('Уровень дерева: {}'.format(vrtx.level))
        print('Конец дерева: {}'.format(vrtx.positive))
        print('Индекс левого сына: {}'.format(vrtx.lson_id))
        print('Индекс правого сына: {}'.format(vrtx.rson_id))

    def lson(vrtx, items, best_choice, Tree, item_count):
        lson_value = vrtx.value+items[vrtx.level].value
        lson_room = vrtx.room-items[vrtx.level].weight
        lson_estimate = vrtx.estimate
        lson_choice = vrtx.choice + "1"
        lson_level = vrtx.level + 1
        if lson_room < 0 | math.ceil(lson_estimate) < best_choice.value:
            lson_positive = -1
        elif lson_level == item_count:
            lson_positive = 1
        else:
            lson_positive = 0

        lson_lson_id = -1
        lson_rson_id = -1
        Tree.append(Vertex(lson_value, lson_room, lson_estimate, lson_choice,
                    lson_level, lson_positive, lson_lson_id, lson_rson_id))
        vrtx.lson_id = len(Tree)-1
        # if lson_positive == 1 & lson_value > best_choice.value:
        #     best_choice = Tree[vrtx.lson_id]
        #     Tree.remove(Tree[vrtx.lson_id()])

        # if vrtx.lson_id != -1 & vrtx.rson_id != -1:
        #     Tree.remove(vrtx)

    def rson(vrtx, items, best_choice, Tree, item_count):
        Est_new = Double_estimate(items, vrtx.room, vrtx.level+1, item_count)
        rson_value = vrtx.value
        rson_room = vrtx.room
        rson_estimate = Est_new + vrtx.value
        rson_choice = vrtx.choice + "0"
        rson_level = vrtx.level + 1
        if rson_estimate < best_choice.value:
            rson_positive = -1
        elif rson_level == item_count:
            rson_positive = 1
        else:
            rson_positive = 0

        rson_lson_id = -1
        rson_rson_id = -1
        Tree.append(Vertex(rson_value, rson_room, rson_estimate, rson_choice,
                    rson_level, rson_positive, rson_lson_id, rson_rson_id))
        vrtx.rson_id = len(Tree)-1
        # if rson_positive == 1 & rson_value > best_choice.value:
        #     best_choice = Tree[vrtx.rson_id]
        #     Tree.remove(Tree[vrtx.rson_id()])
        # if vrtx.lson_id != -1 & vrtx.rson_id != -1:
        #     Tree.remove(vrtx)


class Item:
    def __init__(item, value, weight, density, id, kn_id):
        item.value = value
        item.weight = weight
        item.density = item.value/item.weight
        item.id = id
        item.kn_id = kn_id


def Integer_estimate(items, capacity, level, item_count):
    best_choice = Vertex(0, capacity, 0, "", 0, 0, 0, 0)
    Est_new = 0
    cap = capacity
    i = level
    while i < item_count:
        if items[i].weight > cap:
            best_choice.choice += "0"
            best_choice.level += 1
            i += 1
        else:
            Est_new += items[i].value
            cap -= items[i].weight
            best_choice.value = Est_new
            best_choice.room = cap
            best_choice.choice += "1"
            best_choice.level += 1
            i += 1
    best_choice.positive = 1
    best_choice.lson_id = -1
    best_choice.rson_id = -1
    best_choice.estimate = 0
    return best_choice

# !!! Спуск вниз только налево + спуск вниз последовательно по уменьшению удельной стоимости и учитывая вес


def Get_sorted_data(input_data, item_count):
    items = []
    lines = input_data.split('\n')
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        item = Item(int(parts[0]), int(parts[1]),
                    int(parts[0])/int(parts[1]), i, 0)
        items.append(item)
    return items


def Double_estimate(items, capacity, level, item_count):
    Est_new = 0
    cap = capacity
    i = level
    while i < item_count:
        if items[i].weight > cap:
            Est_new += items[i].density*cap
            break
        else:
            Est_new += items[i].value
            cap -= items[i].weight
            i += 1
    return Est_new


def Fill_nulls(vrtx, item_count):
    n = item_count - vrtx.level
    for i in range(n):
        vrtx.choice += '0'
    return vrtx


def Left_down(vrtx, items, item_count, best_choice, Tree):
    left_max = vrtx
    cap = vrtx.room
    i = vrtx.level
    while i < item_count:
        if items[i].weight > cap:
            break
        else:
            if vrtx.positive == -1:
                break
            else:
                vrtx.lson(items, best_choice, Tree, item_count)
                cap -= items[i].weight
                left_max = Tree[vrtx.lson_id]
                vrtx = Tree[vrtx.lson_id]
            i += 1
    left_max.estimate = left_max.value + Double_estimate(
        items, left_max.room, left_max.level, item_count)
    if left_max.value > best_choice.value:
        left_max.positive = 1
        best_choice = Fill_nulls(left_max, item_count)
    else:
        left_max.positive = -1
    return left_max, best_choice


input_data_1 = input()


def get_data(input_data_1):
    lines = input_data_1.split('\n')

    new_input = []

    new_input += [int(lines[1]), int(lines[0])]

    for i in range(2, lines[1]):
        new_input += [lines[i][1], lines[i][0]]
    return new_input


input_data = get_data(input_data_1)

lines = input_data.split('\n')

firstLine = lines[0].split()
item_count = int(firstLine[0])
capacity = int(firstLine[1])

items = Get_sorted_data(input_data, item_count)
items.sort(key=lambda x: x.density, reverse=True)
# В массиве "items" отсортированные вещи по удельной стоимости

best_choice = Integer_estimate(items, capacity, 0, item_count)

Est = Double_estimate(items, capacity, 0, item_count)
Tree = []
Tree.append(Vertex(0, capacity, Est, '', 0, 0, -1, -1))

wave_1 = Left_down(Tree[0], items, item_count, best_choice, Tree)
best_choice = wave_1[1]

if item_count < 100:
    m = item_count
else:
    m = (math.ceil(math.log2(item_count))
         ) ^ (25 ^ math.ceil(math.sqrt(item_count)))

for i in range(m):
    n = len(Tree)
    for j in range(n):
        if Tree[0].level == item_count | Tree[0].positive == -1:
            Tree.remove(Tree[0])
        else:
            Tree[0].rson(items, best_choice, Tree, item_count)
            w_i_j = Left_down(Tree[Tree[0].rson_id],
                              items, item_count, best_choice, Tree)
            if best_choice.value < w_i_j[1].value:
                best_choice = w_i_j[1]
            Tree.remove(Tree[0])
        j += 1
    i += 1
choice = list(best_choice.choice)
for i in range(item_count):
    items[i].kn_id = int(choice[i])
items.sort(key=lambda x: x.id)

output_data = str(best_choice.value) + ' ' + '0' + '\n'
for i in range(item_count):
    output_data += str(items[i].kn_id) + ' '
print(best_choice.value)
# return output_data
#
#     # output_data = ''
#     # output_data = str(vertex_max[1]) + ' ' + str(0) + '\n'
#     # for i in range(0, item_count):
#     #     output_data += vertex_max[0].split('')
#     #
#     # return output_data
#
#
# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) > 1:
#         file_location = sys.argv[1].strip()
#         with open(file_location, 'r') as input_data_file:
#             input_data = input_data_file.read()
#             print(solve_it(input_data))
#     else:
#         print(
#             'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
