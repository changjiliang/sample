import numpy as np
import random
import pandas as pd
from scipy.interpolate import interp1d
import math
import geopy.distance


def resamplingBylen(tra, m):  #总共要多少个点
    m -= len(tra)
    if m <= 0:
        return tra

    if len(tra) == 2:
        fl = interp1d(tra[:, 0], tra[:, 1])
        x = np.linspace(tra[:, 0][0], tra[:, 0][1], m + 2)
        y = fl(x)

        return np.array(list(zip(*[x, y])))
    dic = {}
    sumdis = 0

    for i in range(len(tra) - 1):
        dis = geopy.distance.distance(tra[i], tra[i + 1]).kilometers
        sumdis += dis
        dic[i] = [tra[i:i + 2], dis]
    dic = sorted(dic.items(), key=lambda x: x[1][-1], reverse=True)

    sump = m
    for i in range(len(dic)):
        n = math.ceil(dic[i][1][1] / sumdis * sump)
        if n >= m:
            n = m
        m -= n
        dic[i][1][1] = n
        if m == 0:
            for j in range(i + 1, len(dic)):
                dic[j][1][1] = 0
            break
    for j in range(0, len(dic)):
        if dic[j][1][1] == 0:
            continue

        fl = interp1d(dic[j][1][0][:, 0], dic[j][1][0][:, 1])
        x = np.linspace(dic[j][1][0][:, 0][0], dic[j][1][0][:, 0][1],
                        dic[j][1][1] + 2)
        y = fl(x)
        dic[j][1][0] = np.array(list(zip(*[x, y])))
    dic = dict(dic)
    new_tra = dic[0][0]
    for i in range(1, len(dic)):
        new_tra = np.vstack((new_tra, dic[i][0][1:]))
    return new_tra