'''
Date: 2022-04-19 15:33:19
LastEditors: ZSudoku
LastEditTime: 2022-06-24 17:00:06
FilePath: \Digita-twin\Digital twin\model_5 taskFlow.py
立库模块，主要计算堆垛机的任务

未与模块五同步内容:CargoNow 参数化处理

'''
import codecs
import random
from time import strftime
from time import gmtime

import datetime

from InPutCodeOptimization import *
from InPutCodeOriginal import *
from InPutData5 import *
from jtyStep1 import *
import mysql_goodsLocationInfo as CargoNow_sql
import mysql_productionLineData as ddjData_sql
import copy
import json

global PlanFlag
#PlanFlag = False
#CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
# R = 39
# S = 14
# H = 14
# C = 17
LineTimeList=[ 31.84, 32.69, 34.55, 35.41, 37.29, 38.15, 40.02, 40.88, 42.78, 44.70, 46.58 ]
LisCross = [[[1,3,48],[3,4,17.78]],[[2,3,5.17],[3,4,17.78]]] #程天宇计算
#各种类型的上货数量  
# LisGoodsNum = [{'10':8,'11':6,'13':6,'15':7,'16':12}]
# dirInspect = {'10':8,'15':6}
#3箱一垛或者是5箱一垛
mod1 = 3
mod2 = 5
inrTime = 4 #叠一次货物运行时长
flodTime = 5 #两次叠箱间的等待时长
lostTime = inrTime + flodTime 


graph_of_spots = [  #陈薛强输出
    [1, 10, 9, 2.5],
    [1, 11, 9, 2.1],
    [2, 9, 5, 2.3],
    [3, 4, 2, 2.4],
    [3, 5, 2, 1.5],
    [3, 6, 2, 1.4],
    [4, 2, 1, 2.5],
    [6, 1, 3, 3],
    [7, 3, 8, 3.4],
    [7, 3, 7, 3.1]
]

fold_id = 1  # 叠箱机的 id  陈薛强输出

global LisInspectTaskTime 
global LisInspectTaskNum
LisInspectTaskTime = [[],[],[],[]]
LisInspectTaskNum = [0,0,0,0]

global returnOutTime  #创造一垛回库资产的时间
global DdjTotalTask
global TaskFlow
global CargoNow
global R
global S
global H
global C
global dirInspect
global LisGoodsNum
global LisDdjTime 
global LisDdjTimeD
global LisInspect
global LisReturnTime
global inspectIndex #已读送检数量
global returnIndex  #已读回库数量
global LisEnterTime #入库资产到达对应入库口的时间
global DdjEnterXYZ
global DdjOutXYZ
global DdjInspectXYZ
global InspectTypeFloorNum
global ReadInspectTypeNum
global DirReturnXYZ
global LisTypeOrder#入库的顺序（类型）
global DirEnterTypeNum#入库资产的类型以及对应的箱数
global InspectFloor
global upEnterType
global nowEnterType
global EnterTypeNum
global rrr#每个堆垛机对应的line，二维list
global ans#所有line编号,一维set
global r#所有入库的编号,一维set
global dr#每个入库编号对应的line编号,一维dict3
global lineToDdj
global idToL

returnOutTime = 200
lineToDdj={};
idToL={};
# global LisupLoadTimeLis #上货点到叠箱机的时间序列
dr = {}
r=set()
ans = set();
rrr=[];
R = 0
S = 0
H = 0
C = 0
null=None
DdjTotalTask = []
CargoNow = []
LisGoodsNum = []
dirInspect = {}
LisDdjTime = []
LisDdjTimeD = []
LisInspect = [{'2':[11,17,13]},{'3':[10]},{'4':[10,14,12]},{'5':[11,11]}]#json 文件中获得
LisReturnTime = []
LisEnterTime = []
inspectIndex = 0
returnIndex = 0
upEnterType = 0
nowEnterType = 0
EnterTypeNum = 0
DdjEnterXYZ = []  #[[[ddj1_x1.ddj1_y1,ddj1_z1],[...]],[[ddj2_x1,...],[....]],...[]]
DdjOutXYZ = []  
DirReturnXYZ = {}  
DirEnterTypeNum = {}
DdjInspectXYZ = []   #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
InspectTypeFloorNum = []
ReadInspectTypeNum = []
TaskFlow = {}
def initCode(flag):
    global inrTime
    global flodTime 
    global lostTime
    mod1 = 3
    mod2 = 5
    inrTime = 6 #叠一次货物运行时长
    flodTime = 8 #两次叠箱间的等待时长
    lostTime = inrTime + flodTime 
    
    #CargoNow = [{'x': 1869.90466, 'y': 19.9703217, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 3, 'column': 26, 'type': '10', 'id': 'A-7-3-26', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1869.26843, 'y': 7.68457127, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 10, 'type': '10', 'id': 'B-16-2-10', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1878.222, 'y': 18.434639, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 16, 'column': 24, 'type': '10', 'id': 'B-8-16-24', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1881.42786, 'y': 18.434639, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 21, 'column': 24, 'type': '10', 'id': 'A-15-21-24', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1900.63, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 51, 'column': 25, 'type': '10', 'id': 'A-9-51-25', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1889.743, 'y': 16.1310234, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 34, 'column': 21, 'type': '10', 'id': 'A-7-34-21', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1898.0625, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 47, 'column': 20, 'type': '10', 'id': 'A-15-47-20', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1871.82764, 'y': 19.9703979, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 26, 'type': '10', 'id': 'B-8-6-26', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1889.10876, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 33, 'column': 2, 'type': '11', 'id': 'B-10-33-2', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1868.62036, 'y': 15.3631821, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 1, 'column': 20, 'type': '11', 'id': 'B-16-1-20', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1878.222, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 16, 'column': 25, 'type': '11', 'id': 'A-9-16-25', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1890.38525, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 35, 'column': 24, 'type': '11', 'id': 'B-6-35-24', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1892.94763, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 39, 'column': 23, 'type': '11', 'id': 'B-16-39-23', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1879.50464, 'y': 16.8989182, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 18, 'column': 22, 'type': '11', 'id': 'A-15-18-22', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1871.18518, 'y': 6.14884233, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 5, 'column': 8, 'type': '13', 'id': 'B-16-5-8', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1868.62036, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 11, 'type': '13', 'id': 'A-15-1-11', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1892.31165, 'y': 10.7560148, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 38, 'column': 14, 'type': '13', 'id': 'A-15-38-14', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1874.38452, 'y': 16.1310234, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 10, 'column': 21, 'type': '13', 'id': 'A-13-10-21', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1898.70679, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 48, 'column': 18, 'type': '13', 'id': 'A-13-48-18', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1898.70679, 'y': 11.5238724, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 48, 'column': 15, 'type': '13', 'id': 'A-15-48-15', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1882.06409, 'y': 19.9703217, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 22, 'column': 26, 'type': '15', 'id': 'A-9-22-26', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1875.02258, 'y': 7.68457127, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 11, 'column': 10, 'type': '15', 'id': 'A-15-11-10', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1898.06311, 'y': 18.434639, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 47, 'column': 24, 'type': '15', 'id': 'B-16-47-24', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1874.38452, 'y': 16.1310234, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 10, 'column': 21, 'type': '15', 'id': 'A-11-10-21', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1870.54688, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 4, 'column': 20, 'type': '15', 'id': 'A-15-4-20', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1869.26843, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 23, 'type': '15', 'id': 'B-16-2-23', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1891.02551, 'y': 13.8274679, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 36, 'column': 18, 'type': '15', 'id': 'A-15-36-18', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1884.62317, 'y': 16.1310234, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 26, 'column': 21, 'type': '16', 'id': 'B-8-26-21', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1871.18518, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 5, 'column': 24, 'type': '16', 'id': 'B-6-5-24', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1892.31165, 'y': 13.0595894, 'z': 50.35678, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 38, 'column': 17, 'type': '16', 'id': 'B-14-38-17', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1882.71045, 'y': 16.1310616, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 23, 'column': 21, 'type': '16', 'id': 'B-6-23-21', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1898.0625, 'y': 18.434639, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 47, 'column': 24, 'type': '16', 'id': 'A-13-47-24', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1877.58569, 'y': 10.7560148, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 15, 'column': 14, 'type': '16', 'id': 'B-16-15-14', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1888.46655, 'y': 19.2025337, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 32, 'column': 25, 'type': '16', 'id': 'B-8-32-25', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1892.94763, 'y': 13.0595894, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 39, 'column': 17, 'type': '16', 'id': 'B-12-39-17', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1882.71045, 'y': 13.0595894, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 17, 'type': '16', 'id': 'A-13-23-17', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1883.3446, 'y': 19.2024975, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 24, 'column': 25, 'type': '16', 'id': 'A-5-24-25', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1896.14722, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 44, 'column': 11, 'type': '16', 'id': 'A-15-44-11', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1898.70679, 'y': 19.97036, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 48, 'column': 26, 'type': '16', 'id': 'A-5-48-26', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 40}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 41}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 42}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 43}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 44}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 45}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 47}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 48}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 49}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 50}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 51}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 52}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 53}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 54}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 55}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 56}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 57}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 58}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 59}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 61}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 62}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 63}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 64}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 65}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 66}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 67}, {'x': 1871.82764, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 6, 'type': 10, 'id': 'B-6-6-8', 'bidBatch': '2021年第一批', 'factory': '宁夏隆基', 'num': 68}, {'x': 1873.74841, 'y': 10.7560148, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 14, 'column': 9, 'type': 10, 'id': 'B-8-9-14', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 69}, {'x': 1887.82837, 'y': 7.68457127, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 10, 'column': 31, 'type': 10, 'id': 'B-14-31-10', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 70}, {'x': 1888.46655, 'y': 13.8274679, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 18, 'column': 32, 'type': 11, 'id': 'B-8-32-18', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1889.743, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 34, 'type': 11, 'id': 'A-13-34-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1896.7876, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 45, 'type': 11, 'id': 'B-14-45-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1899.34912, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 49, 'type': 11, 'id': 'A-13-49-3', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 74}, {'x': 1874.38452, 'y': 9.220296, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 12, 'column': 10, 'type': 11, 'id': 'A-9-10-12', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 75}, {'x': 1875.66882, 'y': 16.1310234, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 21, 'column': 12, 'type': 11, 'id': 'B-12-12-21', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 77}, {'x': 1871.82764, 'y': 1.5416708, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 2, 'column': 6, 'type': 13, 'id': 'A-9-6-2', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 78}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 79}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2021年第一批', 'factory': '苏源杰瑞', 'num': 80}, {'x': 1873.74841, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 9, 'type': 13, 'id': 'A-5-9-1', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 81}, {'x': 1880.14307, 'y': 4.613105, 'z': 53.2860031, 's1': 1, 's2': 1, 'flag': 'B', 'line': 16, 'row': 6, 'column': 19, 'type': 15, 'id': 'B-16-19-6', 'bidBatch': '2021年第一批', 'factory': '宁波三星', 'num': 82}, {'x': 1882.71045, 'y': 4.613105, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 6, 'column': 23, 'type': 15, 'id': 'A-11-23-6', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1877.58582, 'y': 11.5238724, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 15, 'column': 15, 'type': 15, 'id': 'A-5-15-15', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 84}]
    # CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
    # R = 39
    # S = 14
    # H = 14
    # C = 17
    LineTimeList=[ 31.84, 32.69, 34.55, 35.41, 37.29, 38.15, 40.02, 40.88, 42.78, 44.70, 46.58 ]
    LisCross = [[[1,3,47.11],[3,4,17.78]],[[2,3,5.17],[3,4,17.78]]] #程天宇计算
    #各种类型的上货数量  
    #LisGoodsNum = [{'10':8,'11':6,'13':6,'15':7,'16':12}]

    graph_of_spots = [
        [1, 10, 9, 2.5],
        [1, 11, 9, 2.1],
        [2, 9, 5, 2.3],
        [3, 4, 2, 2.4],
        [3, 5, 2, 1.5],
        [3, 6, 2, 1.4],
        [4, 2, 1, 2.5],
        [6, 1, 3, 3],
        [7, 3, 8, 3.4],
        [7, 3, 7, 3.1]
    ]

    fold_id = 1  # 叠箱机的 id
    
    global LisInspectTaskTime 
    global LisInspectTaskNum
    LisInspectTaskTime = [[],[],[],[]]
    LisInspectTaskNum = [0,0,0,0]
    
    #global Report
    global returnOutTime  #创造一垛回库资产的时间
    global DdjTotalTask
    global TaskFlow
    global CargoNow
    global R
    global S
    global H
    global C
    global dirInspect
    global LisGoodsNum
    global LisInspect
    global LisReturnTime
    global inspectIndex #已读送检数量
    global returnIndex  #已读回库数量
    global LisEnterTime #入库资产到达对应入库口的时间
    global DdjEnterXYZ
    global DdjOutXYZ
    global DdjInspectXYZ
    global InspectTypeFloorNum
    global ReadInspectTypeNum
    global DirReturnXYZ
    global LisTypeOrder#入库的顺序（类型）
    global DirEnterTypeNum#入库资产的类型以及对应的箱数
    global InspectFloor
    global upEnterType
    global nowEnterType
    global EnterTypeNum
    global rrr#每个堆垛机对应的line，二维list
    global ans#所有line编号,一维set
    global r#所有入库的编号,一维set
    global dr#每个入库编号对应的line编号,一维dict3
    global lineToDdj
    global idToL
    global LisDdjTime
    
    #Report = {}
    returnOutTime = 200
    lineToDdj={};
    idToL={};
    # global LisupLoadTimeLis #上货点到叠箱机的时间序列
    dr = {}
    r=set()
    ans = set();
    rrr=[];
    R = 0
    S = 0
    H = 0
    C = 0
    CargoNow = CargoOptimized[Days]
    TaskFlow = {}
    DdjTotalTask = [0,0,0,0,0,0] #堆垛机已完成任务量
    LisInspect = [{'2':[11,17,13]},{'3':[10]},{'4':[10,14,12]},{'5':[11,11]}]#json 文件中获得
    LisReturnTime = []
    LisEnterTime = []
    inspectIndex = 0
    returnIndex = 0
    DdjEnterXYZ = []  #[[[ddj1_x1.ddj1_y1,ddj1_z1],[...]],[[ddj2_x1,...],[....]],...[]]
    DdjOutXYZ = []  
    DirReturnXYZ = {}  
    DirEnterTypeNum = {}
    LisTypeOrder = []
    DdjInspectXYZ = []   #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
    InspectTypeFloorNum = []
    ReadInspectTypeNum = []
    LisDdjTime = []
    InspectFloor = []
    upEnterType = 0
    nowEnterType = 0
    EnterTypeNum = 0
    if(flag == False):
        # CargoNow = [{'x': 1868.62036, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 1, 'type': 10, 'id': 'A-5-1-1', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1901.27039, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 52, 'type': 10, 'id': 'B-6-52-1', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1894.86646, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 42, 'type': 10, 'id': 'A-7-42-1', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1896.14722, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 44, 'type': 10, 'id': 'B-8-44-1', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1891.02551, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 36, 'type': 10, 'id': 'A-9-36-1', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1883.98486, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 25, 'type': 10, 'id': 'B-10-25-1', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1877.58582, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 15, 'type': 10, 'id': 'A-11-15-2', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1873.74841, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 9, 'type': 10, 'id': 'B-12-9-1', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1883.3446, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 24, 'type': 11, 'id': 'A-13-24-1', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1887.82837, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 31, 'type': 11, 'id': 'B-14-31-1', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1898.70679, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 48, 'type': 11, 'id': 'A-15-48-1', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1869.26843, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 2, 'type': 11, 'id': 'A-5-2-1', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1900.63, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 51, 'type': 11, 'id': 'B-6-51-1', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1885.26343, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 27, 'type': 11, 'id': 'A-7-27-1', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1898.0625, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 47, 'type': 13, 'id': 'B-8-47-1', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1871.82764, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 6, 'type': 13, 'id': 'A-9-6-1', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1881.42786, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 21, 'type': 13, 'id': 'B-10-21-1', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1885.90771, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 28, 'type': 13, 'id': 'A-11-28-2', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1886.54578, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 29, 'type': 13, 'id': 'B-12-29-1', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1901.27039, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 52, 'type': 13, 'id': 'A-13-52-1', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1875.66882, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 12, 'type': 15, 'id': 'B-14-12-1', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1895.50488, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 43, 'type': 15, 'id': 'A-15-43-1', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1889.10876, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 33, 'type': 15, 'id': 'A-5-33-1', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1899.98157, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 50, 'type': 15, 'id': 'B-6-50-1', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1883.3446, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 24, 'type': 15, 'id': 'A-7-24-1', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1873.74841, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 9, 'type': 15, 'id': 'B-8-9-1', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1887.192, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 30, 'type': 15, 'id': 'A-9-30-2', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1879.50464, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 18, 'type': 16, 'id': 'B-10-18-1', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1898.70679, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 48, 'type': 16, 'id': 'A-11-48-2', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1894.2262, 'y': 3.84524536, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 5, 'column': 41, 'type': 16, 'id': 'B-12-41-5', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1898.0625, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 47, 'type': 16, 'id': 'A-13-47-1', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1869.90466, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 3, 'type': 16, 'id': 'B-14-3-1', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1891.65967, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 37, 'type': 16, 'id': 'A-15-37-1', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1869.90466, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 3, 'type': 16, 'id': 'A-5-3-1', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1880.78748, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 20, 'type': 16, 'id': 'B-6-20-1', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1869.26843, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 2, 'type': 16, 'id': 'A-7-2-1', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1876.94336, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 14, 'type': 16, 'id': 'B-8-14-1', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1899.34912, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 49, 'type': 16, 'id': 'A-9-49-2', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1876.94336, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 2, 'column': 14, 'type': 16, 'id': 'B-10-14-2', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 40}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 41}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 1, 's2': 0, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 42}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 43}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 44}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 45}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 47}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 48}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 49}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 50}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 51}, 
        #             {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 52}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 53}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 54}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 55}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 0, 's2': 1, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 56}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 57}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 58}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 59}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 61}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 62}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 63}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 64}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 65}, {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 66}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 67}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 68}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 69}, {'x': 1901.27039, 'y': 8.452438, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 11, 'column': 52, 'type': 10, 'id': 'A-11-52-11', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 70}, {'x': 1901.27039, 'y': 6.916702, 'z': 44.90394, 's1': 1, 's2': 1, 'flag': 'B', 'line': 10, 'row': 9, 'column': 52, 'type': 11, 'id': 'B-10-52-9', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1901.27039, 'y': 6.916702, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 9, 'column': 52, 'type': 11, 'id': 'A-13-52-9', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1901.27039, 'y': 11.5238724, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 15, 'column': 52, 'type': 11, 'id': 'A-7-52-15', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1901.27039, 'y': 11.5238724, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 15, 'column': 52, 'type': 11, 'id': 'B-6-52-15', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 74}, {'x': 1901.27039, 'y': 13.8274679, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 18, 'column': 52, 'type': 11, 'id': 'B-14-52-18', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 75}, {'x': 1901.27039, 'y': 4.613105, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 6, 'column': 52, 'type': 11, 'id': 'B-12-52-6', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 77}, {'x': 1898.70679, 'y': 0.7738123, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 1, 'column': 48, 'type': 13, 'id': 'A-9-48-1', 'bidBatch': '2019年第二批', 'factory': '宁波三星', 'num': 78}, {'x': 1898.70679, 'y': 0.7738123, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 1, 'column': 48, 'type': 13, 'id': 'B-6-48-1', 'bidBatch': '2019年第二批', 'factory': '宁夏隆基', 'num': 79}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 80}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 81}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 82}, {'x': 1901.27039, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 52, 'type': 15, 'id': 'A-13-52-3', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1901.27039, 'y': 13.8274679, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 18, 'column': 52, 'type': 15, 'id': 'A-7-52-18', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 84}]
        CargoNow = CargoOriginal[Days]
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0):
            R += 1
        elif(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            S += 1
        elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 0):
            H += 1
        elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 1):
            C += 1
    LisGoodsNum = CALCLisGoodsNum()
    dirInspect = CALCdirInspect() 
#任务流变量初始化
def initJson():
    null=None
    global TaskFlow
    true = True
    TaskFlow = {
        "version":0.2,
        "system": "Dynamitic_Digitaltwin",
        "stage": "ResponseDeduction",
        "type":"//Dynamitic",
        "time": "2022-04-30",
        "runTime": 0,
        "data": {
            "responseCode": 101,
            "userName": "admin",
            "planNames": null,
            "taskContent": 
            {
                "loadPointTask": [
                    {
                        "taskNumber": 0, #//0表示当前设备没有任务，有数字表示有任务且有任务号
                        "equipmentName": "上货点1",
                        "loadPosition": null,
                        "assertType": 0,  #//1-6
                        "assertId": 0, #//资产ID  0
                        "target": null, #//移动目标位置
                        "workStatus": "运行", #//"运行"
                        "cumulativeTask": 0, #//累计任务量  1的总量
                        "currentTask": 0, #//当前任务量
                        "outTask": 0, #//表示总出库  给值
                        "equipmentFrequency": 0, #//设备频次
                        "maintenanceStatus": 0 ,#//维保状态
                        "factory": "",#//  deal
                        "arrivedBatch": "", #//到货批次deal
                        "bidBatch": "", #//招标批次deal
                        "checkStatus": true, #//检定状态deal
                        "contain": 0, #//垛容量deal
                        "strackerNo": "3,A" #// 堆垛机号, 去哪个堆垛机哪一侧。A / B对应货架的储位deal
                    }
                ],
                "stackerMachines": #//堆垛机任务集合
                    [
                        {
                            "taskType": 0, #//移库入库、检定出库、检定入库、配送出库  -1表示仅仅是移动  
                            "taskNumber": 1,
                            "equipmentName": "堆垛机3",
                            "workStatus": "运行", #//运行
                            "totalTask": 0, #//总任务量数
                            "currentTask": 0, #//已完成任务数
                            "equipmentFrequency": 0, #//设备频次
                            "maintenanceStatus": 0, #//维保状态
                            
                            "stackerGetItems": 
                            [
                            {
                                "getPosition": null, #/取货点目标 "A-1-1-1" " "
                                "getAssertType1": 0, #//第1取货叉取货资产类型  实际类型
                                "getAssert1Id": 1, #//资产ID
                                "getDirection1": null, #//第1取货叉取货方向  null
                                "getAssertType2": 0, #//第2取货叉取货资产类型
                                "getAssert2Id": 1, #//资产ID
                                "getDirection2": null #//第2取货叉取货方向,如果只取一个，这里传 null
                            },
                            {
                                "getPosition": null, #//取货点目标  null
                                "getAssertType1": 0, #//第1取货叉取货资产类型
                                "getAssert1Id": 1, #//资产ID
                                "getDirection1": null, #//第1取货叉取货方向
                                "getAssertType2": 0, #//第2取货叉取货资产类型
                                "getAssert2Id": 1, #//资产ID
                                "getDirection2": null #//第2取货叉取货方向
                            }
                            ],
                            
                            "statckPutItems":
                            [
                            {
                                "putPosition": null, #//放货点目标 
                                "putAssertType1": 0, #//第1取货叉放货资产类型
                                "putDirection1": null, #//第1放货叉放货方向
                                "putAssertType2": 0, #//第1放货叉取货资产类型
                                "putDirection2": null #/第2放货叉放货方向
                            },

                            {
                                "putPosition": null, #//放货点目标
                                "putAssertType1": 0, #//第1取货叉放货资产类型
                                "putDirection1": null, #//第1放货叉放货方向
                                "putAssertType2": 0, #//第1放货叉取货资产类型
                                "putDirection2": null #//第2放货叉放货方向
                            }

                            ]
                        }
                        
                    ]
            }
        }
    }
#创建任务流文件
def CreatJson():
    global TaskFlow
    if(PlanFlag == False):
        a = str(datetime.date(2022, 4, Days+1))
        file = f'output/original_{a}.json'
        fp = codecs.open(file, 'a+', 'utf-8')
        fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
        fp.write("\n,\n")
        fp.close()
    else:
        a = str(datetime.date(2022, 4, Days+1))
        file = f'output/optimize_{a}.json'
        fp = codecs.open(file, 'a+', 'utf-8')
        fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
        fp.write("\n,\n")
        fp.close()
#去重
def delList(L):
    L1 = []
    for i in L:
        if i not in L1:
            L1.append(i)
    return L1

#计算入库资产类型数量
def CALCLisGoodsNum():
    global LisGoodsNum
    LisGoodsNum = []
    LisGoodsNum.append({})
    LisTemp = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0 ):
            LisTemp.append(int(CargoNow[i]['type']))
            LisTemp =  delList(LisTemp)
    for i in range(len(LisTemp)):
        count = 0
        for j in range(len(CargoNow)):
            if(CargoNow[j]['s1'] == 0 and CargoNow[j]['s2'] == 0 ):
                if(int(CargoNow[j]['type']) == LisTemp[i]):
                    count += 1
        LisGoodsNum[0]['%d'%(LisTemp[i])] = count
    return LisGoodsNum
#print(CALCLisGoodsNum())
#计算检定资产的类型和数量
def CALCdirInspect():
    global dirInspect
    dirInspect = {}
    LisTemp = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1 ):
            LisTemp.append(int(CargoNow[i]['type']))
            LisTemp =  delList(LisTemp)
    for i in range(len(LisTemp)):
        count = 0
        for j in range(len(CargoNow)):
            if(CargoNow[j]['s1'] == 0 and CargoNow[j]['s2'] == 1 ):
                if(int(CargoNow[j]['type']) == LisTemp[i]):
                    count += 1
        dirInspect['%d'%(LisTemp[i])] = count
    return dirInspect
#print(CALCdirInspect())
#cty model_3
def emu(org,die,tStop=[]): #算法二输出，叠箱机编号，
    # 记录无入边的
    ru = set();
    # 存放上货点
    d0 = set();
    # 存放交通点
    tran = set();
    # 存树边
    ed = {};
    # 存边权
    t = {};
    # org.append([-1,-1,-1,-1]);
    for i in range(0,len(org)):
            ru.add(org[i][2]);
            ed[org[i][1]] = org[i][2];  # ed[起点]=[终点]
            t[org[i][1]]=org[i][3];
    # 找出上货点
    for i in range(0,len(org)):
        if(org[i][1] not in ru):
            d0.add(org[i][1]);
            # tran.add(ed[key]);
    # 假设已有叠箱机编号
    # die = 1;
    # 首交通点 到 叠箱机
    # 直接全算，没算法
    res={};
    for i in d0:
        st = ed[i];
        if(st not in res):
            res[st] = 0;
            j=st;
            while(j!=die):
                res[st]+=t[j];
                #留待加停留时间
                j=ed[j];
    Liscross = [];
    for i in d0:
        tem=[];
        ttm=[];
        tem.append(i);
        tem.append(ed[i]);
        tem.append(t[i]);
        ttm.append(ed[i]);
        ttm.append(die);
        ttm.append(res[ed[i]]);
        Liscross.append([tem,ttm]);
    return Liscross;
###


#model_4


#n个上货点的最短上货频率和资产初始上货时刻
def upLoad():
    
    return 0


#计算上货点的上货频率
def CALCupLoadFre(lostTime,upLoadNum):
    return lostTime*upLoadNum + 10


#找出上货点的对应数标
def CALCupLoadSign(LisCross):
    LisupLoadSign = [] 
    for i in LisCross:
        LisupLoadSign.append(i[0][0])
    return LisupLoadSign

#找出上货点 交汇的所有数标
def CALCupLoadCross(LisCross):
    upLoadCross = []
    for i in LisCross:
        upLoadCross.append(i[0][1])
    upLoadCross = delList(upLoadCross)
    return upLoadCross

#根据上货点的交汇点，将上货点进行分类
def CALCupLoadSameCross(LisCross,upLoadCross):
    LisupLoadSameCross = []
    j = 0
    LisTemp = []
    for i in range(len(upLoadCross)):
        LisupLoadSameCross.append([])
    for j in range(len(upLoadCross)):   
        for i in LisCross:
            if(i[0][1] == upLoadCross[j]):
                LisupLoadSameCross[j].append(i[0])
    return LisupLoadSameCross


#计算各上货点到第一个交汇点的时间
def CALCupLoadFirstCrossTime(LisCross):
    LisUpLoadFirstCrossTime = {}
    j = 0
    for i in LisCross:
        LisUpLoadFirstCrossTime['%d'%j] = i[0][2]
        j += 1
    return LisUpLoadFirstCrossTime

#LisUpLoadFirstCrossTime = CALCupLoadFirstCrossTime(LisCross)#各个上货点到第一个交汇点的时间

#计算各个上货点的初始上货时间
def CALCupLoadTime():
    LisCrossTime = CALCupLoadFirstCrossTime(LisCross)
    LisCrossTime = sorted(LisCrossTime.items(), key=lambda item:item[1], reverse = True) #按照 value 倒序排序
    #LisCrossTime =  sorted(LisCrossTime,reverse=True)
    upLoadNum = len(LisCrossTime)
    upLoadFre = CALCupLoadFre(lostTime,upLoadNum)
    #LisupLoadStartTime = LisCrossTime
    LisupLoadStartTime = []
    #print(LisCrossTime)
    for i in range(upLoadNum):
        #print('i',i)
        if(i==0):
            LisupLoadStartTime.append(0)
        else:
            time_t = (LisCrossTime[i-1][1] + (i) * lostTime) - LisCrossTime[i][1]
            if(time_t <  upLoadFre):
                LisupLoadStartTime.append(time_t)
            else:
                LisupLoadStartTime.append(time_t % upLoadFre)
    dir = {}
    for i in range(upLoadNum):
        dir['%s'%(LisCrossTime[i][0])] = LisupLoadStartTime[i]
    tuple = sorted(dir.items(),key=lambda x:x[0]) #按照key的值正序排序
    LisupLoadStartTime = []
    for i in range(upLoadNum):
        LisupLoadStartTime.append(tuple[i][1])
    return LisupLoadStartTime 

#根据资产类型判断 x箱一垛，返回x
def CALCmod(type):
    if(type == '11' or type == '15' or type == '16' or type == '10' or type == '17' or type == '18' or type == '19'):
        return 5
    elif(type == '12' or type == '13' or type == '14' ):
        return 3
    else:
        print("CALCmod type Error!","type",type)
        return 3
    pass

#上货点分配任务量
def CALCupLoadGoodsNum(upLoadNum,LisGoodsNum):
    global DirEnterTypeNum
    LisupLoadGoodsNum = []
    LisTemp = []
    #按照上货点数量对列表进行分割
    for i in range(upLoadNum):
        LisupLoadGoodsNum.append([])
    #获取每种资产的上货数量
    for i in LisGoodsNum[0]:
        #print(LisGoodsNum[0][i])
        mod = CALCmod(i)
        LisTemp.append(LisGoodsNum[0][i] * mod)
        DirEnterTypeNum[i] = LisGoodsNum[0][i] * mod
    #针对每种类型的上货资产，在上货点出进行分割
    LisNum = [0]
    upLoadIndex = 0
    
    for j in LisTemp:#第 j 次分割
        LisNum  = []
        LisNum = CALCeachUpLoadNum(upLoadNum=upLoadNum,GoodsNum=j)
        for i in range(upLoadNum):
            LisupLoadGoodsNum[upLoadIndex].append(LisNum[i][0])
            upLoadIndex += 1
            if(upLoadIndex == upLoadNum):
                upLoadIndex = 0
        upLoadIndex = LisNum[len(LisNum)-1]
    #print(LisupLoadGoodsNum)
    return LisupLoadGoodsNum

#根据上货点数量和货物数量对每个上货点的上货量进行分割
def CALCeachUpLoadNum(upLoadNum,GoodsNum):
    LisNum = []
    for i in range(upLoadNum):
        LisNum.append([])
    upLoadIndex = 0#记录开始上货点的标号
    eachNum = int(GoodsNum/upLoadNum)
    temp = GoodsNum%upLoadNum
    
    for i in range(upLoadNum):
        LisNum[i].append(eachNum)
    if(temp == 0): #如果可以平均分
        LisNum.append(upLoadIndex)
        return LisNum
    else:     #不能平均分  
        for i in range(upLoadNum):
            if(temp==0):
                LisNum.append(upLoadIndex)
                return LisNum
            #temp = GoodsNum%upLoadNum 
            LisNum[upLoadIndex][0] = eachNum + 1
            upLoadIndex += 1
            temp -= 1
    # LisNum.append(upLoadIndex)        
    # return LisNum
    

#做出一个列表 数据结构为 [[startTime,fre,time1,time2],...,]
def CALCupLoadParm(LisCross):
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    upLoadFre = CALCupLoadFre(lostTime,upLoadNum)
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadParm = []
    for i in LisupLoadStartTime:
        LisupLoadParm.append([])
    for i in range(upLoadNum):
        LisupLoadParm[i].append(int(LisupLoadStartTime[i]))
        LisupLoadParm[i].append(upLoadFre)
        for j in LisCross[i]:
            LisupLoadParm[i].append(j[2])
    return LisupLoadParm

#货物到达叠箱机的时间序列（按照上货点以及资产类型区分）
def CALCupLoadTimeLis():
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum)
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisupLoadTimeLis = []
    #创造出与货物类型区分开的列表的数据结构
    for i in range(len(LisupLoadGoodsNum)):
        LisupLoadTimeLis.append([])
        for j in range(len(LisupLoadGoodsNum[i])):
            LisupLoadTimeLis[i].append([])
    for i in range(len(LisupLoadGoodsNum)):
        time = 0
        index = 0
        for n in LisupLoadGoodsNum[i]:
            #k = len((LisupLoadGoodsNum[i]))
            for j in range(n):
                time +=  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
                LisupLoadTimeLis[i][index].append(time)
            index += 1
    #print(LisupLoadParm)
    return LisupLoadTimeLis

#货物到达叠箱机的时间序列(总时间序列)
def CALCupLoadAllTimeLis():
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum)
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisupLoadTimeLis = []
    for i in range(len(LisupLoadGoodsNum)):
        #遍历两个上货点
        time = 0
        index = 0
        upLoadTotalNum = 0
        for j in LisupLoadGoodsNum[i]:
            upLoadTotalNum += j
        for j in range(upLoadTotalNum):
            time =  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
            time = round(time,3)
            LisupLoadTimeLis.append(time)
        # for n in LisupLoadGoodsNum[i]:
        #     #k = len((LisupLoadGoodsNum[i]))
        #     for j in range(n):
        #         #何时上货： 1:LisupLoadParm[i][0]  2:LisupLoadParm[i][0] + LisupLoadParm[i][1] 3:LisupLoadParm[i][0] + 2*LisupLoadParm[i][1]
        #         time =  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
        #         LisupLoadTimeLis.append(time)
        #     index += 1
        
    #print(LisupLoadParm)
    LisupLoadTimeLis = sorted(LisupLoadTimeLis)
    return LisupLoadTimeLis
###




def getLine():
    global rrr
    global ans
    ans = set()
    rs = [];

    #取出所有货架编号
    for i in range(0,len(CargoNow)):
        ans.add(CargoNow[i]['line']);
    #取出集合所有元素放入list
    for i in ans:
        rs.append(i);
    #list排序
    # rs=[3,4,5,6,7,8,9,10,11,12,13,14,16];
    rs.sort()
    # print("%%%%%%%%%%%%%%")
    # print(rs)
    # print("%%%%%%%%%%%%%%")
    # rs=[1,3,4,5,7,9,11,12,13]

    le = len(rs)
    i=0;
    while(i < le):
        if(i==le-1):
            rrr.append([rs[i]])
            i+=1;
            continue;
        if(rs[i] + 1 == rs[i+1]):
            rrr.append([rs[i],rs[i+1]]);
            i+=2;
        else:
            rrr.append([rs[i]])
            i+=1;

    return rrr;


# global r
# r=set()
def cal(LisCode, n=5):
    global LineTimeList
    global ans
    ans = set()
    #取出所有货架编号
    for i in range(0,len(CargoNow)):
        ans.add(CargoNow[i]['line']);
    LisupLoadTimeLis = CALCupLoadAllTimeLis()  # 上货点到叠箱机
    #print("LisupLoadTimeLis", LisupLoadTimeLis)
    dList = {};
    line = list(ans)
    line.sort()
    global r
    global dr
    
    if (len(r) == 0 or len(dr) == 0):
        for i in range(0, len(CargoNow)):
            if (CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0):
                r.add(CargoNow[i]['item'])
                # r[res[i]['item']]=int(res[i]['type']);
                dr[CargoNow[i]['item']] = int(CargoNow[i]['line']);

    rTot = [];
    for i in LisCode:
        if (i in r):
            rTot.append(i);

    # 检验箱之间安全间隔时间是否满足
    nn = n;
    for i in range(1, len(LisupLoadTimeLis)):
        diff = LisupLoadTimeLis[i] - LisupLoadTimeLis[i - 1];
        tem = (i + 1) % nn;
        if (tem == 0):
            if (diff < 4):
                LisupLoadTimeLis[i] = LisupLoadTimeLis[i - 1] + 4;
                continue;
        if (diff < 9):
            LisupLoadTimeLis[i] = LisupLoadTimeLis[i - 1] + 9;

    # 处理list
    LineTimeList.reverse();
    LineTimeList.append(LineTimeList[-1]);
    # 在sort后获取line
    for i in range(0, len(line)):
        dList[line[i]] = LineTimeList[i];
    rres = [];
    le = len(LisupLoadTimeLis);
    rest = le % n;
    cnt = 0;
    temp_i = 0
    global lineToDdj
    if(len(lineToDdj)==0):
        if(len(rrr) == 0):
            getLine()
        for i in range(0,len(rrr)):
            for j in range(0,len(rrr[i])):
                lineToDdj[rrr[i][j]] = (i+1);
    for i in range(4, le, 5):
        rres.append({})
        ttem = LisupLoadTimeLis[i] + dList[dr[rTot[cnt]]];
        rres[temp_i]['%d'%(lineToDdj[dr[rTot[cnt]]])] = round(ttem,3)
        cnt += 1;
        temp_i += 1
    # 保留小数点后两位
    # for i in range(len(rres)):
    #     rres[i] = round(rres[i], 3)
    #这里得改下，rres是个字典,rres[时间]=堆垛机编号
    # 最后的不满5箱的
    # if(rest!=0):
    #print(RefResolutionError)
    temp = []
    for i in range(len(rres)):
        for j in rres[i]:
            temp.append(int(j))
    temp = DelList(temp)
    temp2 = []
    for i in range(len(temp)):
        temp2.append([])
    for i in range(len(rres)):
        for j in rres[i]:
            temp2[int(j)-1].append(rres[i])
    #print(temp2)
    rres = temp2
    # ddj = 1
    # print(rres[ddj-1][0].get('%d'%(ddj)))
    return rres;

def FoldToDdj():
    global LineTimeList
    global DirEnterTypeNum
    global LisTypeOrder
    #DirEnterTypeNum['16'] = 352#test
    LineTimeList = sorted(LineTimeList,reverse=True)
    LisupLoadTimeLis = CALCupLoadAllTimeLis()
    typeNum = 0
    LisTypeOrder = []
    for i in DirEnterTypeNum:
        typeNum += 1
        LisTypeOrder.append(i)
    LisToDdj = []
    k = 1
    typeYet = 0#已经读取的类型数量
    mod =  CALCmod(LisTypeOrder[typeYet])#3箱或者5箱一垛
    for i in range(len(LisupLoadTimeLis)):
        if k > DirEnterTypeNum['%s'%LisTypeOrder[typeYet]]:
            typeYet += 1
            mod = CALCmod(LisTypeOrder[typeYet])
            k = 1
        if k%mod == 0:#根据当前数量
            LisToDdj.append(LisupLoadTimeLis[i])
        k += 1
    for i in range(len(LisToDdj)):
        # if(i<11):
        #     LisToDdj[i] +=  LineTimeList[i]
        # else:
        LisToDdj[i] += LineTimeList[i%11]
        LisToDdj[i] = round(LisToDdj[i],3)
    LisToDdjX = [[],[],[],[],[],[]]
    for i in range(len(LisToDdj)):
        if i%11 == 0 or i%11 == 1:
            LisToDdjX[0].append(LisToDdj[i])
        elif i%11 == 2 or i%11 == 3:
            LisToDdjX[1].append(LisToDdj[i])
        elif i%11 == 4 or i%11 == 5:
            LisToDdjX[2].append(LisToDdj[i])
        elif i%11 == 6 or i%11 == 7:
            LisToDdjX[3].append(LisToDdj[i])
        elif i%11 == 8 or i%11 == 9:
            LisToDdjX[4].append(LisToDdj[i])
        elif i%11 == 10:
            LisToDdjX[5].append(LisToDdj[i])
    return LisToDdjX


####model_4 over


#####model_1####

#判断编码属于的堆垛机序号




def CALCStacker(id):
    global rrr
    global lineToDdj
    global idToL
    #rrr是否为空
    if(len(rrr)==0):
        getLine();
    #lineToDdj是否为空
    if(len(lineToDdj)==0):
        for i in range(0,len(rrr)):
            for j in range(0,len(rrr[i])):
                lineToDdj[rrr[i][j]] = (i+1);

    #idToL是否为空
    if(len(idToL)==0):
        for i in range(0, len(CargoNow)):
            idToL[CargoNow[i]['item']] = CargoNow[i]['line']
        # dat({},{},{},{},set(),0);    
        for i in idToL:
            tem = lineToDdj[idToL[i]];
            idToL[i] = tem;

    if(id==-1):
        return 0
    
    return idToL[id];


def getLisDdjCode(rdLi):
    Nddj=len(getLine());
    
    # if(len(rdLi)==0):
    #     r = {}
    #     h = {}
    #     s = {}
    #     c = {}
    #     # 获取字典 r,h,s,c
    #     tt=set();#无用
    #     dd={};#wuyo
    #     n = dat(r, h, s, c,dd,tt);
    #     rdLi = rdCode(len(n));
    # print(rdLi)
    # print(Nddj)
    output = [];
    for i in range(0,Nddj):
        output.append([]);
    for i in rdLi:
        dN = CALCStacker(i);
        output[dN-1].append(i);

    return output;


#######
#global inspectIndex #已检定个数

#去重
def DelList(L):
    L1 = []
    for i in L:
        if i not in L1:
            L1.append(i)
    return L1

#判断编码类型函数
def CALCjudgeType(p):
    type = '0'
    if(CargoNow[p-1]['s1'] == 0 and CargoNow[p-1]['s2'] == 0):
        type = 'R'
    elif(CargoNow[p-1]['s1'] == 0 and CargoNow[p-1]['s2'] == 1):
        type = 'S'
    elif(CargoNow[p-1]['s1'] == 1 and CargoNow[p-1]['s2'] == 0):
        type = 'H'
    elif(CargoNow[p-1]['s1'] == 1 and CargoNow[p-1]['s2'] == 1):
        type = 'C'
    else:
        print("CALCjudgeType error!")
    return type

#编码处理，送检在回库之前
#编码按照堆垛机分开
#LisDdjCode = [[39, 59, 12, 64, 68, 45, 31, 29, 84, 61, 50, 37, 77, 81, 47], [8, 71, 65, 51, 34, 28, 56, 6, 69, 43, 1, 42, 3, 57], [9, 75, 55, 11, 5, 41, 67, 53, 78, 21], [76, 60, 58, 80, 83, 24, 46, 35, 44], [70, 30, 74, 54, 48, 36, 66, 73, 49, 79, 18, 72, 52, 19, 40, 62, 32, 63], [2, 14, 22, 82, 4, 20, 13, 26, 33, 15, 10, 27, 23, 38, 25, 16, 17, 7]]

#将送检和回库编码取出，按照堆垛机,并将送检编码提前到相对应的回库编码之前
def GetS_H(LisDdjCode):
    #
    # c = 0
    # for i in range(len(LisDdjCode)):
    #     for j in range(len(LisDdjCode[i])):
    #         c += 1
    # print("c",c)
    # print("R+S+H+C",R+S+H+C)
    # print("len(Cargo)",len(CargoNow))
    
    #
    global LisReturnTime
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                for k in range(len(LisDdjCode[i])):
                    if((LisDdjCode[i][j]-S) == LisDdjCode[i][k]):
                        if(k<j):
                            temp = LisDdjCode[i][j]
                            LisDdjCode[i][j] = LisDdjCode[i][k]
                            LisDdjCode[i][k] = temp
    LisS_H = []
    for i in range(len(LisDdjCode)):
        LisS_H.append([])
        LisS_H[i].append([])
        LisS_H[i].append([])
    LisTemp_S = []
    x = 0
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                x += 1
                LisTemp_S.append(LisDdjCode[i][j])
                LisS_H[i][0].append(LisDdjCode[i][j])
            elif(CALCjudgeType(LisDdjCode[i][j]) == 'H'):
                LisS_H[i][1].append(LisDdjCode[i][j])
    print("x",x)
    print("S",S)
    for i in range(S):
        LisReturnTime.append([])
        LisReturnTime[i] = {}
    #初始化LisReturn
    for i in range(len(LisReturnTime)):
        LisReturnTime[i]['%d'%(LisTemp_S[i])] = float('inf') 
    #print(LisDdjCode)
    #print(LisS_H)
    #print(LisReturnTime)
    return LisS_H
#GetS_H(LisDdjCode)



#堆垛机行走时间
def CALCWalkTime(x,y):
    v1 = 0.5  #堆垛机垂直移动速度
    v2 = 10   #堆垛机水平移动速度
    HighRoad = 0  #垂直移动的距离
    LongRoad = 0  #水平移动的距离
    TimeHighRoad = 0 #垂直移动的时间
    TimeLongRoad = 0 #水平移动的时间
    TimeRunRoad = 0  #堆垛机移动的时间
    HighRoad = y 
    LongRoad = x
    TimeHighRoad = y / v1  #计算垂直移动的时间
    TimeLongRoad = x / v2  #计算水平移动的时间
    TimeRunRoad = max(TimeHighRoad,TimeLongRoad)  #计算堆垛机的时间
    return TimeRunRoad


#根据编码，获得堆垛机的上货点的坐标
def GetEnterXY(p):
    ddj = CALCStacker(p)
    LisEnterXY = DdjEnterXYZ[ddj-1]
    
    return LisEnterXY 
'''
    "floor2": [ 11, 17, 13 ],
    "floor3": [ 10 ],
    "floor4": [ 10, 14 ],
    "floor5": [ 11, 11 ]
'''


#处理数据
def AddLisInspect():
    global LisInspect
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    for i in range(len(LisInspect)):
        L = list(LisInspect[i].values())
        for j in range(len(L[0])):
            if(L[0][j] == 11):
                LisInspect[i]['%d'%(LF[i])].append(15)
                LisInspect[i]['%d'%(LF[i])].append(16)
    for i in range(len(LisInspect)):
        L = list(LisInspect[i].values())
        for j in range(len(L[0])):
            LisInspect[i]['%d'%(LF[i])] = DelList(LisInspect[i]['%d'%(LF[i])] )
    return LisInspect
# LisInspect = AddLisInspect(LisInspect)
#print("LisInspect",LisInspect)
#根据楼层划分资产类型
def CALCDayInspectFloor():
    global LisInspect
    LisInspect = AddLisInspect()
    LisT = []
    LisF = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            LisT.append(CargoNow[i]['type'])
    LisT = DelList(LisT)
    L = []
    for i in range(len(LisInspect)):
        LisF.append([])
        LisF[i] = {}
        L1 = LisInspect[i].keys()
        L1 = list(L1)
        L.append(int(L1[0]))
        LisF[i]['%d'%(L[i])] = []
        L1 = LisInspect[i].values()
        L1 = list(L1)
        for k in range(len(LisT)):
            for j in L1[0]:
                #print(LisT[k])
                if LisT[k] == j:
                    LisF[i]['%d'%(L[i])].append(j)  
        for j in range(len(LisF[i]['%d'%(L[i])])):
            LisF[i]['%d'%(L[i])].append(100/len(LisF[i]['%d'%(L[i])])) 
    LisTemp = []
    index = 0
    for i in LisF:
        for j in i:
            #print(i['%s'%(j)])
            if i['%s'%(j)]:
                pass
            else:
                LisTemp.append(index)
        index += 1
    count = 0
    if len(LisTemp) > 0:
        for i in range(len(LisTemp)):
            
            del LisF[LisTemp[i] - count]
            #print("yes")
            count += 1
    #print("LisF",LisF)  #计算当日送检楼层实际检定的资产型号序列
    return LisF
# LisF = CALCDayInspectFloor()

#根据类型划分楼层
def CALCDayInspectType():
    global LisInspect
    List = []
    LisT = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            List.append(CargoNow[i]['type'])
    List = DelList(List)
    #print(List)
    #准备好字典
    for i in range(len(List)):
        LisT.append([])
        LisT[i] = {}
        LisT[i]['%d'%(List[i])] = []
    #print(LisT)
    #获取所有楼层
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    #print(LF)
    #计算当日送检资产型号的楼层序列
    for i in range (len(List)):
        for j in range(len(LisInspect)):
            for k in LisInspect[j]['%d'%(LF[j])]:
                if k == List[i]:
                    LisT[i]['%d'%(List[i])].append(LF[j])
    #print("LisT",LisT)
    return LisT
#LisT = CALCDayInspectType()
#print(LisT)
#dirInspect = {'10':8,'15':6}
#分配当日送检资产的楼层权重：
def CALCDayInspectIW():
    global InspectTypeFloorNum 
    LisF = CALCDayInspectFloor()
    LisT = CALCDayInspectType()
    global LisInspect
    List  = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            List.append(CargoNow[i]['type'])
    List = DelList(List)
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    L = []
    for i in range(len(LisF)):
        L.append([])
        L[i] = {}
        try:
            L[i]['%d'%(LF[i])] = LisF[i]['%d'%(LF[i])][-1]
        except  KeyError:
            pass
        #print(LisF[i]['%d'%(LF[i])][-1])
    LisT_GoodNUm =  copy.deepcopy(LisT)
    for i in range(len(LisT)):
        for j in range(len(LisT[i]['%d'%(List[i])])):
                temp = LisT[i]['%d'%(List[i])][j]
                LisT[i]['%d'%(List[i])][j] = {}
                LisT[i]['%d'%(List[i])][j]['%d'%(temp)] = 0
                
    # print("LisT_GoodNUm",LisT_GoodNUm)        
    # print("LisT",LisT)
    # temp = LisT[0].get('10')[0] 
    # LisT[0].get('10')[0]  = {}
    # LisT[0].get('10')[0]['%d'%(temp)] = 0
    # print(LisT[0].get('10'))
    
    for i in range(len(LisT_GoodNUm)):
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            for m in range(len(LisF)):
                for k in L[m]:
                    # print("LisT[i]['%d'%(List[i])][j]",LisT[i]['%d'%(List[i])][j])
                    # print("k",k)
                    if( int(k) == int(LisT_GoodNUm[i]['%d'%(List[i])][j])):
                        LisT_GoodNUm[i]['%d'%(List[i])][j] = int(L[m].get('%s'%(k)))
    #print("LisT_k",LisT_GoodNUm)
    LisNum = []
    for i in range(len(List)):
        temp = 0
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            temp += LisT_GoodNUm[i]['%d'%(List[i])][j]
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            LisT_GoodNUm[i]['%d'%(List[i])][j] = LisT_GoodNUm[i]['%d'%(List[i])][j] / temp
            LisT_GoodNUm[i]['%d'%(List[i])][j] = round(LisT_GoodNUm[i]['%d'%(List[i])][j] * dirInspect.get('%d'%(List[i])))
            LisNum.append(LisT_GoodNUm[i]['%d'%(List[i])][j])
    #LisNum = [1,2,3,4]
    #print("LisNum",LisNum)
    Num_p = 0
    for i in range(len(LisT)):
        for k in range(len(LisT[i].get('%d'%(List[i])))):
            for u in LisT[i].get('%d'%(List[i]))[k]:
                LisT[i].get('%d'%(List[i]))[k]['%d'%(int(u))] = LisNum[Num_p]
                Num_p += 1
    global ReadInspectTypeNum
    ReadInspectTypeNum = {}
    for i in range(len(LisT)):
        ReadInspectTypeNum['%d'%(List[i])] = 0
    for i in range(len(LisT)):
        Len = len(LisT[i].get('%d'%(List[i])))
        for j in range(Len):
            if len(LisT[i].get('%d'%(List[i]))) == 1:
                break
            LisT[i].get('%d'%(List[i]))[0] = dict(LisT[i].get('%d'%(List[i]))[0],**LisT[i].get('%d'%(List[i]))[j])
        while True:
            if(len(LisT[i].get('%d'%(List[i])))>1):
                del(LisT[i].get('%d'%(List[i]))[-1])
            else:
                break
            
    #print(ReadInspectTypeNum)
    #print(LisT)
    # print("L",L)
    #print("LisT_GoodNUm",LisT_GoodNUm)
    InspectTypeFloorNum = LisT
    return LisT
#LisT = CALCDayInspectIW() 
#根据堆垛机编码和楼层号，返回堆垛机的送检/回库口
def GetLisInspectXY(ddj,floor):
    #global DdjInspectXYZ  #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
    #print(DdjInspectXYZ[floor-2][ddj-1])
    return DdjInspectXYZ[floor-2][ddj-1]


# #根据编码，获得堆垛机送检口的坐标
# def GetInspectXY(p,Flag):
#     global DirReturnXYZ
#     global InspectTypeFloorNum
#     global ReadInspectTypeNum
#     if(CALCjudgeType(p) == 'H'):
#         return DirReturnXYZ['%d'%(p+S)]
#     elif(Flag == False):
#         return DirReturnXYZ['%d'%(p)]
#     type_p = CALCjudgeType(p)
#     if(len(InspectTypeFloorNum) == 0):
#         CALCDayInspectIW() 
#     # print("DdjInspectXYZ",DdjInspectXYZ)
#     # print("InspectTypeFloorNum",InspectTypeFloorNum)
#     ddj = CALCStacker(p)
#     LisInspectXY = [1000,1000]
#     Model = CargoNow[p-1]['type']
#     p_Floor = 0
    
#     # for i in range(len(InspectTypeFloorNum)):
#     #     for j in InspectTypeFloorNum[i]:
#     #         if int(j) == int(Model):
                
#     #             InspectTypeFloorNum[i].get('%d'%(int(j)))
#     #             print(InspectTypeFloorNum[i].get('%d'%(int(j))))
#     for i in range(len(InspectTypeFloorNum)):
#         for j in InspectTypeFloorNum[i]:
#             if int(j) == int(Model):
#                 temp = InspectTypeFloorNum[i].get('%d'%(int(j)))
#     presentNum = 0
#     for i in temp[0]:
#         Num = ReadInspectTypeNum.get('%d'%(Model)) 
#         #print(temp[0])
#         if(Num - presentNum < temp[0].get('%d'%(int(i)))):
#             p_Floor = int(i)
#             Num += 1
#             ReadInspectTypeNum['%d'%(Model)] = Num
#             break
#         else:
#             presentNum = temp[0].get('%d'%(int(i)))
#     if(Flag == False):
#         tempNum = ReadInspectTypeNum['%d'%(Model)]
#         tempNum -= 1
#         ReadInspectTypeNum['%d'%(Model)] = tempNum
#     LisInspectXY = GetLisInspectXY(ddj,p_Floor)
#     #print("temp",temp)
#     if(type_p == 'S' and Flag == True):
#         DirReturnXYZ['%d'%(p)] = LisInspectXY
#     return LisInspectXY
#根据编码，获得堆垛机送检口的坐标
def GetInspectXY(p,Flag):
    # global DirReturnXYZ
    # global InspectTypeFloorNum
    # global ReadInspectTypeNum
    # if(CALCjudgeType(p) == 'H'):
    #     return DirReturnXYZ['%d'%(p+S)]
    # elif(Flag == False):
    #     return DirReturnXYZ['%d'%(p)]
    # type_p = CALCjudgeType(p)
    # if(len(InspectTypeFloorNum) == 0):
    #     CALCDayInspectIW() 
    # # print("DdjInspectXYZ",DdjInspectXYZ)
    # # print("InspectTypeFloorNum",InspectTypeFloorNum)
    # ddj = CALCStacker(p)
    # LisInspectXY = [1000,1000]
    # Model = CargoNow[p-1]['type']
    # p_Floor = 0
    
    # # for i in range(len(InspectTypeFloorNum)):
    # #     for j in InspectTypeFloorNum[i]:
    # #         if int(j) == int(Model):
                
    # #             InspectTypeFloorNum[i].get('%d'%(int(j)))
    # #             print(InspectTypeFloorNum[i].get('%d'%(int(j))))
    # for i in range(len(InspectTypeFloorNum)):
    #     for j in InspectTypeFloorNum[i]:
    #         if int(j) == int(Model):
    #             temp = InspectTypeFloorNum[i].get('%d'%(int(j)))
    # presentNum = 0
    # for i in temp[0]:
    #     Num = ReadInspectTypeNum.get('%d'%(Model)) 
    #     #print(temp[0])
    #     if(Num - presentNum < temp[0].get('%d'%(int(i)))):
    #         p_Floor = int(i)
    #         Num += 1
    #         ReadInspectTypeNum['%d'%(Model)] = Num
    #         break
    #     else:
    #         presentNum = temp[0].get('%d'%(int(i)))
    # if(Flag == False):
    #     tempNum = ReadInspectTypeNum['%d'%(Model)]
    #     tempNum -= 1
    #     ReadInspectTypeNum['%d'%(Model)] = tempNum
    #LisInspectXY = GetLisInspectXY(ddj,p_Floor)
    # #print("temp",temp)
    # if(type_p == 'S'  and Flag == True):
    #     DirReturnXYZ['%d'%(p)] = LisInspectXY
    global DirReturnXYZ
    global InspectFloor
    type_p = CALCjudgeType(p)
    if(CALCjudgeType(p) == 'H'):
        return DirReturnXYZ['%d'%(p+S)]
    elif(Flag == False):
        return DirReturnXYZ['%d'%(p)]
    if len(InspectFloor) == 0:
        InspectFloor = DistributeCollection(CargoNow)
    #获取所在送检编码的楼层
    p_type = CargoNow[p - 1]['type']
    if (p_type == 11 or p_type == 15 or p_type == 16):
        LisFloorNum = [0,4,5]
    elif (p_type == 10):
        LisFloorNum = [1,2]
    elif (p_type == 12 or p_type == 14):
        LisFloorNum = [3]
    else:
        print("GetInspectXY p_type Error!")
        LisFloorNum = 'inf'
    for i in LisFloorNum:
        for j in range(len(InspectFloor[i])):
            if p == InspectFloor[i][j]:
                if (i == 0):
                    FloorNum = 2# 送检编码所在楼层已确定
                elif (i == 4 or i == 5):
                    FloorNum = 5
                elif (i == 1):
                    FloorNum = 3
                elif(i == 3 or i == 2):
                    FloorNum = 4
                else:
                    print("LisFloorNum i Error!")
    ddj = CALCStacker(p)
    LisInspectXY = GetLisInspectXY(ddj,FloorNum)
    if(type_p == 'S'  and Flag == True):
        DirReturnXYZ['%d'%(p)] = LisInspectXY
    return LisInspectXY
#根据两个编码判断送检/回库口是否相同
def GetSameFlag(p,second_p,flag):
    # if(CALCjudgeType(p) == 'H'):
    #     for i in LisReturnTime[0]:
    #         p = int(i)
    #     for i in LisReturnTime[1]:
    #         second_p = int(i)
    LisP = GetInspectXY(p,flag)
    LisSecond_P = GetInspectXY(second_p,flag)
    if(LisP[1] == LisSecond_P[1]):
        SameFlag = True
    else:
        SameFlag = False
    
    return SameFlag

#根据编码，获得堆垛机的出库坐标
def GetOutXY(p):
    ddj = CALCStacker(p)
    LisOutXY = DdjOutXYZ[ddj-1]    
    return LisOutXY
#根据编码计算检定时间
"""
单相表:30min --- 1800
三相表:3h45min --- 10800 + 2700 = 13500
互感器:30min --- 1800
采集终端:4h --- 14400
HPLC:15min --- 900
"""
def GetInspectTime(p):
    if(CargoNow[p-1]['type'] == 11 or CargoNow[p-1]['type'] == 15 or CargoNow[p-1]['type'] == 16):#三相表
        inspectTime = 13500
    elif(CargoNow[p-1]['type'] == 10):#单相表
        inspectTime = 1800
    elif(CargoNow[p-1]['type'] == 13):#互感器
        inspectTime = 1800
    elif(CargoNow[p-1]['type'] == 12):#集中器
        inspectTime = 14400
    elif(CargoNow[p-1]['type'] == 14):#采集终端
        inspectTime = 14400
    elif(CargoNow[p-1]['type'] == 17 or CargoNow[p-1]['type'] == 18 or CargoNow[p-1]['type'] == 19):#HPLC
        inspectTime = 900
    #elif()
    else:
        print("GetInspectTime Error!")
        
        print("Days",Days," p",p," type",CargoNow[p-1]['type'])
        inspectTime = 900
    return inspectTime

#回库编码的排序
def sortReturnCode():
    global LisReturnTime
    for i in range(0,len(LisReturnTime)):
        for j in range(0,len(LisReturnTime)-i-1):
            if round(list(LisReturnTime[j].values())[0],3) > round(list(LisReturnTime[j+1].values())[0],3):
                temp = LisReturnTime[j+1]
                LisReturnTime[j+1] = LisReturnTime[j]
                LisReturnTime[j] = temp

#计算回库编码的等待时间
def CALCReturnWaitTime(p,TI):
    global LisReturnTime
    waitTime = 0
    returnTime = 0
    # tempI = 0
    # temp = 0
    # for i in range(len(LisReturnTime)):
    #     for j in LisReturnTime[i]:
    #         #print(j)
    #         if(p+S == int(j)):
    #             temp = int(j)
    #             tempI = i
    #             break
    #     if(temp > 0):
    #         break
    # print(LisReturnTime[i])
    # print(LisReturnTime[i].get('%d'%(temp)))
    #returnTime = int(LisReturnTime[i].get('%d'%(temp)))
    returnTime = round(list(LisReturnTime[0].values())[0],3)
    LisReturnTime[0] = {}
    LisReturnTime[0]['已读'] = float('inf') 
    sortReturnCode()
    if(returnTime > int(TI)):
        waitTime = returnTime - TI
    else:
        waitTime = 0
    return waitTime
###任务流新增函数
def GetDdjTaskType(type):
    if(type == 'R'):
        return 0
    elif(type == 'H'):
        return 1
    elif(type == 'S'):
        return 2
    elif(type == 'C'):
        return 3
    else:
        print("GetDdjTaskType Error!")
        return -1
#根据y坐标，计算楼层
def CALCFloor(y):
    if(y>5 and y <9):
        return '二楼取放货点'
    elif(y>9 and y <14):
        return '三楼取放货点'
    elif(y>14 and y <16):
        return '四楼取放货点'
    elif(y>17 and y<20):
        return '五楼取放货点'
    else:
        print(" CALCFloor Error!")
        return '二楼取放货点'
    
def GetFloorNum(y):
    if(y>5 and y <9):
        return 2
    elif(y>9 and y <14):
        return 3
    elif(y>14 and y <16):
        return 4
    elif(y>17 and y<20):
        return 5
    else:
        print("GetFloorNum Error!")
        return 2

###




#计算入库的等待时间
def GetEnterWaitTime(p,TI):
    global upEnterType
    global nowEnterType
    global EnterTypeNum
    global LisEnterTime
    
    ddj = CALCStacker(p)
    nowEnterType = int(CargoNow[p - 1]['type'])
    if upEnterType > 0:
        if nowEnterType == upEnterType:
            enterTime = LisEnterTime[ddj-1][0] + EnterTypeNum * 600
        else:
            EnterTypeNum += 1
            enterTime = LisEnterTime[ddj-1][0] + EnterTypeNum * 600
    else:
        enterTime = LisEnterTime[ddj-1][0]
    upEnterType = nowEnterType
    try:
        del LisEnterTime[ddj-1][0] 
    except IndexError:
        print("IndexError")
        return 600
        pass
    # if(LisEnterTime[ddj-1] == None):
    #     pass
    # else:
    #     del LisEnterTime[ddj-1][0] 
    if(enterTime > TI):
        return enterTime - TI + 200
    else:
        return 0
#读码函数
def ReadCode(TI,TDI,p,second_p,third_p):
    global DirInspectCodeTime
    global DdjTotalTask
    global LisReturnTime
    #编码类型
    p_type = '0'
    second_p_type = '0'
    third_p_type = '0'
    
    TwoFlag = False #是否一次取两垛
    SameFlag = False #送检/回库 口 是否相同
    
    ddj = 0  # 堆垛机序号
    
    waitTime = 0    #堆垛机等待时长
    grabTime = 20  #取货时长
    placeTime = 20 #卸货时长
    walkTime1 = 0   #行走时长1
    walkTime2 = 0   #行走时长2
    walkTime3 = 0   #行走时长3
    walkTime4 = 0   #行走时长4
    
    
    p_type = CALCjudgeType(p) #获取编码p的类型
    second_p_type = CALCjudgeType(second_p) #获取编码second_p的类型
    #回库编码的变化
    if(p_type == 'H'):
        if(second_p_type == 'H'):
            for i in LisReturnTime[0]:
                p = int(i) - S
            for i in LisReturnTime[1]:
                second_p = int(i) - S
        else:
            for i in LisReturnTime[0]:
                p = int(i) - S
    p_type = CALCjudgeType(p) #获取编码p的类型
    second_p_type = CALCjudgeType(second_p) #获取编码second_p的类型
    third_p_type = CALCjudgeType(third_p)   #获取编码third_p的类型
    ddj = CALCStacker(p)    #获取编码p的堆垛机序号
    
    if(second_p > 0 and third_p == -1): #第三个编码为-1，前两个为一般编码
        third_p_type = 'R'
    elif(second_p == -1 and third_p == -1):#后两个编码都为-1
        second_p_type = -1
        third_p_type = 'R'
        pass
    #判断p与second_p是否为同种类型
    if(p_type == second_p_type):
        #一次作业两垛资产 类型相同
        TwoFlag = True
        if(p_type=='R'):
            #入库 放两垛资产
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
            
            second_x = CargoNow[second_p-1]['x']
            second_y = CargoNow[second_p-1]['y']
        elif(p_type=='S'):
            SameFlag = GetSameFlag(p,second_p,True)
            if(SameFlag == True):
                #送检口相同
                #去第二个货位取货
                first_x = CargoNow[second_p-1]['x']
                first_y = CargoNow[second_p-1]['y']
                #送检口
                LisInspectXY = GetInspectXY(p,False)
                LisInspectXY2 = GetInspectXY(second_p,False)
                if(LisInspectXY != LisInspectXY2):
                    print("LisInspectXY2 Error!")
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                second_x = inspectX
                second_y = inspectY 
                pass
            else:
                #送检口不同
                #去第二个货位取货
                first_x = CargoNow[second_p-1]['x']
                first_y = CargoNow[second_p-1]['y']
                #p的送检口
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                second_x = inspectX
                second_y = inspectY 
                #second_p的送检口
                LisInspectXY = GetInspectXY(second_p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                third_x = inspectX
                third_y = inspectY
                pass
            pass
        elif(p_type == 'H'):
            SameFlag = GetSameFlag(p,second_p,False)
            if(SameFlag == True):
                #回库口相同，当前堆垛机处于回库口，取两垛货物，从回库口移动到货位1，放一垛货
                first_x = CargoNow[p-1]['x']
                first_y = CargoNow[p-1]['y']
                #堆垛机从货位1移动到货位2，放一垛货
                second_x = CargoNow[second_p-1]['x']
                second_y = CargoNow[second_p-1]['y']
                pass
            else:
                #回库口不同，当前堆垛机处于第一个回库口，取一垛货物，之后从回库口1移动到回库口2
                #获取回库口2的坐标
                LisInspectXY = GetInspectXY(second_p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                first_x = inspectX
                first_y = inspectY
                #回库口2取一垛货，之后移动到货位1
                second_x = CargoNow[p-1]['x']
                second_y = CargoNow[p-1]['y']
                #在货位1放一垛货，之后移动到货位2
                third_x = CargoNow[second_p-1]['x']
                third_y = CargoNow[second_p-1]['y']
                pass
            pass
        elif(p_type == 'C'):
            #堆垛机当前位于货位1，取一垛货，移动到货位2
            first_x = CargoNow[second_p-1]['x']
            first_y = CargoNow[second_p-1]['y']
            #堆垛机从货位2移动到出库口
            LisOutXY = GetOutXY(p)
            outX = LisOutXY[0]
            outY = LisOutXY[1]
            second_x = outX
            second_y = outY
        else:
            print("ReadCode p_type TwoFlag = True Error!")
    else:
        TwoFlag = False
        if(p_type == 'R'):
            #入库 堆垛机当前在入库口，取一垛资产
            #堆垛机从入库口移动到货位1，放一垛货
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
        elif(p_type == 'S'):
            #送检，堆垛机当前在货位，取一垛货，移动到送检口放货
            LisInspectXY = GetInspectXY(p,True)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            first_x = inspectX
            first_y = inspectY
        elif(p_type == 'H'):
            #回库，堆垛机当前在回库口，取一垛货，移动到货位放货
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
        elif(p_type == 'C'):
            #出库，当前在货位，需要移动到出库口
            LisOutXY = GetOutXY(p)
            outX = LisOutXY[0]
            outY = LisOutXY[1]
            first_x = outX
            first_y = outY
        else:
            print("ReadCode p_type TwoFlag = False Error!")
            
    #判断最后一个编码的类型，确定堆垛机最后一步要移动到的位置
    if(TwoFlag == False):
        third_p = second_p
        third_p_type = second_p_type
    if(third_p_type == 'R'):
        LisEnterXY = GetEnterXY(third_p)
        enterX = LisEnterXY[0]
        enterY = LisEnterXY[1]
        last_x = enterX
        last_y = enterY
    elif(third_p_type == "S" or third_p_type == 'C'):
        last_x = CargoNow[third_p-1]['x']
        last_y = CargoNow[third_p-1]['y']
    elif(third_p_type == 'H'):
        LisInspectXY = GetInspectXY(third_p,False)
        inspectX = LisInspectXY[0]
        inspectY = LisInspectXY[1]
        last_x = inspectX
        last_y = inspectY  
    elif(third_p_type == -1):
        LisEnterXY = GetEnterXY(p)
        enterX = LisEnterXY[0]
        enterY = LisEnterXY[1]
        last_x = enterX
        last_y = enterY
    else:
        print("ReadCode third_x Error!")
    #读码
    if(p_type=='R'):
        #判断入库口的堵塞问题
        # if(CargoNow[p-1]['flag'] == 'A'):
        #     firstFlag = 0
        # elif(CargoNow[p-1]['flag'] == 'B'):
        #     firstFlag = 1
        if(TwoFlag == True):
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null            
            #TaskFlow['runTime'] = TI
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = GetDdjTaskType(p_type)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = '一楼取放货点'
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getDirection1'] = CargoNow[p-1]['flag']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getDirection2'] = CargoNow[second_p-1]['flag']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
            if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[second_p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[p-1]['type']
                    pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
                    pass
            else:
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putPosition'] = CargoNow[second_p-1]['id']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putAssertType2'] = CargoNow[second_p-1]['type']
            if(p == second_p):
                #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                #print("p:",p,"second_p:",second_p)
            
            #一次入库两垛
            #放到货位1上
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #放到货位2上
            walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
            #根据third编码类型，移动到初始位置
            walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
            #计算时间
            waitTime1 = GetEnterWaitTime(p,TI)
            waitTime2 = GetEnterWaitTime(second_p,TI)
            waitTime = max(waitTime1 , waitTime2)
            
            TaskFlow['runTime'] = TI + waitTime + 80
            CreatJson()
            
            TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
        else:
            #只入库一垛
            
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            #TaskFlow['runTime'] = TI
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = GetDdjTaskType(p_type)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = '一楼取放货点'
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getDirection1'] = CargoNow[p-1]['flag']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            #入库口移动到货位
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #货位移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            waitTime = GetEnterWaitTime(p,TI)
            
            TaskFlow['runTime'] = TI + waitTime + 80
            CreatJson()
            
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
    elif(p_type=='S'):
        global LisInspectTaskTime
        global inspectIndex
        global LisInspectTaskNum
        if(TwoFlag == True):
            if(SameFlag == True):
                initJson()
                DdjTotalTask[ddj-1] += 1 
                #入库任务流为空
                TaskFlow['data']['taskContent']['loadPointTask'] = null
                TaskFlow['version'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
                if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
                    if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[second_p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[second_p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[p-1]['type']
                        pass
                    else:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
                        pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getAssertType2'] = CargoNow[second_p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CALCFloor(second_y)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
                #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                TaskFlow['runTime'] = TI
                CreatJson()
                
                #当前堆垛机已在资产p位置上，首先是取货，之后移动到second_p的货位上
                walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
                #送检口相同,从货位2走到送检口，放货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从送检口走到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                #保留回库时间
                
                inspectTime = GetInspectTime(p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime3  + inspectTime),3)
                inspectIndex += 1
                inspectTime = GetInspectTime(second_p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(second_p)] = round((TI - walkTime3 + inspectTime + 1),3)
                inspectIndex += 1
                #对回库时间排序
                sortReturnCode()
                #检定楼层
                FloorNum = GetFloorNum(second_y)
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3))
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3 + inspectTime))
                LisInspectTaskNum[FloorNum - 2] += 1
                LisInspectTaskNum[FloorNum - 2] += 1
                pass
            else:
                initJson()
                DdjTotalTask[ddj-1] += 1 
                #入库任务流为空
                TaskFlow['data']['taskContent']['loadPointTask'] = null
                TaskFlow['version'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
                if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
                    if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[second_p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[second_p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[p-1]['type']
                        pass
                    else:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
                        pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getAssertType2'] = CargoNow[second_p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CALCFloor(second_y)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putPosition'] = CALCFloor(third_y)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putAssertType2'] = CargoNow[second_p-1]['type']
                TaskFlow['runTime'] = TI
                CreatJson()
                #当前堆垛机已在资产p位置上，首先是取货，之后移动到second_p的货位上
                walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
                #送检口不同
                #送检口不同,从货位2走到送检口1，放货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #送检口不同，从送检口1走到送检口2，放货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #从送检口2走到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                #global inspectIndex
                inspectTime = GetInspectTime(p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime4 - walkTime3  + inspectTime),3)
                inspectIndex += 1
                inspectTime = GetInspectTime(second_p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(second_p)] = round((TI - walkTime4 + inspectTime),3)
                inspectIndex += 1
                #对回库时间排序
                sortReturnCode()
                #检定楼层
                FloorNum = GetFloorNum(second_y)
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3,3))
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3 + inspectTime,3))
                LisInspectTaskNum[FloorNum - 2] += 1
                FloorNum = GetFloorNum(third_y)
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3,3))
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3 + inspectTime,3))
                LisInspectTaskNum[FloorNum - 2] += 1
                pass
            pass
        else:
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CALCFloor(first_y)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
            TaskFlow['runTime'] = TI
            CreatJson()
            #当前位置在货位，移动到送检口
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #从送检口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            waitTime = 0
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            inspectTime = GetInspectTime(p)
            LisReturnTime[inspectIndex] = {}
            LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime2 + inspectTime),3)
            inspectIndex += 1
            #对回库时间排序
            sortReturnCode()
            #检定楼层
            FloorNum = GetFloorNum(first_y)
            LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3,3))
            LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3 + inspectTime,3))
            LisInspectTaskNum[FloorNum - 2] += 1
            pass
        #print()
    elif(p_type=='H'):
        if(TwoFlag == True):
            if(SameFlag == True):
                #获取堆垛机当前的位置，取两垛货
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                #等待时间
                waitTime1 = CALCReturnWaitTime(p,TI)
                waitTime2 = CALCReturnWaitTime(second_p,TI)
                waitTime = max(waitTime1 , waitTime2)
                ###回库创建资产
                initJson()
                FloorNum = GetFloorNum(inspectY)
                TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['stackerMachines'] = null
                TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[p-1]['factory']#deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[p-1]['batchNum']#deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[p-1]['bidBatch']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[p-1]['num']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] =str(CALCStacker(p) + 2) + ',' + 'B' #deal
                TaskFlow['runTime'] = TI + waitTime - returnOutTime
                CreatJson()
                
                initJson()
                FloorNum = GetFloorNum(inspectY)
                TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['stackerMachines'] = null
                TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[second_p-1]['type']
                TaskFlow['runTime'] = TI + waitTime - returnOutTime + 10
                TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[second_p-1]['factory']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[second_p-1]['batchNum']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[second_p-1]['bidBatch']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[second_p-1]['num']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(second_p) + 2) + ',' + 'B'  # deal
                CreatJson()
                ###
                initJson()
                DdjTotalTask[ddj-1] += 1 
                #入库任务流为空
                TaskFlow['data']['taskContent']['loadPointTask'] = null
                TaskFlow['version'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 2
                TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CALCFloor(inspectY)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
                #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
                if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                    if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[second_p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[second_p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[p-1]['type']
                        pass
                    else:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
                        pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putAssertType2'] = CargoNow[second_p-1]['type']
                if(p == second_p):
                    #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                    #print("p:",p,"second_p:",second_p)
                #连续取两垛，回库口相同
                
                #堆垛机从当前位置移动到货位1，放一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #从货位1移动到货位2，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从货位2移动到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                
                
                TaskFlow['runTime'] = TI + waitTime
                CreatJson()
                
                TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                pass
            else:
                #回库口不同
                #获取堆垛机当前位置，取一垛货
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                
                waitTime1 = CALCReturnWaitTime(p,TI)
                waitTime2 = CALCReturnWaitTime(second_p,TI)
                waitTime = max(waitTime1 , waitTime2)
                
                initJson()
                FloorNum = GetFloorNum(inspectY)
                TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
                # if(FloorNum == 4):
                #     print('error!',p)
                TaskFlow['data']['taskContent']['stackerMachines'] = null
                TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[p-1]['factory']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[p-1]['batchNum']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[p-1]['bidBatch']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[p-1]['num']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(p) + 2) + ',' + 'B'  # deal
                TaskFlow['runTime'] = TI + waitTime - returnOutTime
                CreatJson()
                
                initJson()
                FloorNum = GetFloorNum(first_y)
                TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['stackerMachines'] = null
                TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[second_p-1]['type']
                TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[second_p-1]['factory']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[second_p-1]['batchNum']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[second_p-1]['bidBatch']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[second_p-1]['num']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(second_p) + 2) + ',' + 'B'  # deal
                TaskFlow['runTime'] = TI + waitTime - returnOutTime + 20
                CreatJson()
                
                initJson()
                DdjTotalTask[ddj-1] += 1 
                #入库任务流为空
                TaskFlow['data']['taskContent']['loadPointTask'] = null
                TaskFlow['version'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 2
                TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CALCFloor(inspectY)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getPosition'] = CALCFloor(first_y)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getAssertType2'] = CargoNow[second_p-1]['type']
                if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                    if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[second_p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[second_p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[p-1]['type']
                        pass
                    else:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
                        pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putAssertType2'] = CargoNow[second_p-1]['type']
                if(p == second_p):
                    #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                    #print("p:",p,"second_p:",second_p)
                #堆垛机从当前位置移动到回库口2，取一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #堆垛机从回库口2移动到货位1，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #堆垛机从货位1移动到货位2，放一垛货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #堆垛机从货位2移动到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                
                
                TaskFlow['runTime'] = TI + waitTime
                CreatJson()
                
                TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                pass
        else:
            #堆垛机当前位于回库口，取一垛货，移动到货位1，放一垛货
            LisInspectXY = GetInspectXY(p,False)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            
            waitTime = CALCReturnWaitTime(p,TI)
            
            initJson()
            FloorNum = GetFloorNum(inspectY)
            TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
            TaskFlow['data']['taskContent']['stackerMachines'] = null
            TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
            TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[p - 1]['factory']  # deal
            TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[p - 1]['batchNum']  # deal
            TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[p - 1]['bidBatch']  # deal
            TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[p - 1]['num']  # deal
            TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(p) + 2) + ',' + 'B'  # deal
            TaskFlow['runTime'] = TI + waitTime - returnOutTime
            CreatJson()
        
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 2
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CALCFloor(inspectY)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
            walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
            #从货位1移动到下个编码起始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TaskFlow['runTime'] = TI + waitTime
            CreatJson()
            
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
    elif(p_type=='C'):
        if(TwoFlag == True):
            
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            #TaskFlow['runTime'] = TI
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = GetDdjTaskType(p_type)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
                if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[second_p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[p-1]['type']
                    pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
                    pass
            else:
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getPosition'] = CargoNow[second_p-1]['id']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getAssertType2'] = CargoNow[second_p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = '一楼出库放货点'
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putDirection1'] = CargoNow[p-1]['flag']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putDirection2'] = CargoNow[second_p-1]['flag']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] 
            TaskFlow['runTime'] = TI
            CreatJson()
            
            #出两垛货
            #堆垛机当前在货位1，取一垛货之后，移动到货位2
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机在货位2取一垛货，移动到出库口，放两垛货
            walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
            #堆垛机移动到下一个编码的起始位置
            walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
            #计算时间
            TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            pass
        else:
            
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            #TaskFlow['runTime'] = TI
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = GetDdjTaskType(p_type)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] 
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = '一楼出库放货点'
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putDirection1'] = CargoNow[p-1]['flag']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
            
            TaskFlow['runTime'] = TI
            CreatJson()
            #堆垛机当前位于货位，取一垛货，移动到出库口放货
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机从出库口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
        pass
    else:
        print("ReadCode p_type error!")
    return TI


def Read(LisDdjCode):
    DdjNum = len(LisDdjCode)
    for i in range(DdjNum):
        LisDdjTime.append(0)
        LisDdjTimeD.append(0)
        # LisDdjTimeD[i] = 0
        # LisDdjTime[i] = 0
    # print(LisDdjCode)
    # print(LisDdjCode[3][1])
    # print(LisDdjCode[3][2])
    # print(LisDdjCode[3][3])
    for i in range(DdjNum):
        global upEnterType
        global nowEnterType
        global EnterTypeNum
        k = 0
        for j in range(len(LisDdjCode[i])):
            upEnterType = 0
            nowEnterType = 0
            EnterTypeNum = 0
            if(k+3 <= len(LisDdjCode[i])):
                LisDdjTime[i] =round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],LisDdjCode[i][k+1],LisDdjCode[i][k+2]),3)
            elif(k+2 == len(LisDdjCode[i])):
                LisDdjTime[i] = round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],LisDdjCode[i][k+1],-1),3)
            elif(k+1 == len(LisDdjCode[i])):
                LisDdjTime[i] = round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],-1,-1),3)
            elif(k == len(LisDdjCode[i])):
                break
            if(k+1 == len(LisDdjCode[i])):
                break
            if(CALCjudgeType(LisDdjCode[i][k]) == CALCjudgeType(LisDdjCode[i][k+1])):
                k += 1
            k += 1
# GetS_H(LisDdjCode)
# Read(LisDdjCode)
#print(LisReturnTime)
# print(LisDdjTime)

#获得堆垛机所需数据，主要是坐标

def GetDdjDataXYZ(DdjData):
    global DdjEnterXYZ
    global DdjOutXYZ
    global DdjInspectXYZ
    #DdjData = ddjData_sql.getStacks()
    Lisfloor = []
    for i in range(len(DdjData)):
        for j in DdjData[i]:
            if '放货点' in j:
                Lisfloor.append(j)
    Lisfloor = DelList(Lisfloor)
    inspectFloorNum = len(Lisfloor) - 2
    for i in range(inspectFloorNum):
        DdjInspectXYZ.append([])
    for i in range (len(DdjData)):
        for j in DdjData[i]:
            if '一楼取放货点' in j:
                DdjEnterXYZ.append(DdjData[i].get('%s'%(j)))
            if '一楼出库放货点' in j:
                DdjOutXYZ.append(DdjData[i].get('%s'%(j)))
            if '二楼取放货点' in j:
                DdjInspectXYZ[0].append(DdjData[i].get('%s'%(j)))
            if '三楼取放货点' in j:
                DdjInspectXYZ[1].append(DdjData[i].get('%s'%(j)))
            if '四楼取放货点' in j:
                DdjInspectXYZ[2].append(DdjData[i].get('%s'%(j)))
            if '五楼取放货点' in j:
                DdjInspectXYZ[3].append(DdjData[i].get('%s'%(j)))
                


### 计划推演报文
def initReportJson():
    global Report
    Report = {
    "version": 0.2,
    "system": "Dynamitic_Digitaltwin",
    "stage": "ResponseReport",
    "time": "2021-11-19-16-51",
    "runTime": 0,
    "data": {
        "responseCode": -101,
        "userName": "admin",
        "reports": [
            {
                "planName": "nam1",
                "reportContent": {
                    "original_plan": {
                        "summary": {
                            "efficiency": 128,
                            "line_usage": 74,
                            "cargo_usage": 85,
                            "ave_work_hour": 585
                        },
                        "detail": [
                            {
                                "date": "2022-01-02",
                                "cargo_usage": 85,
                                "modules": [
                                    {
                                        "type": "module1",
                                        "R": 500,
                                        "arrivedBatch": "2621212128223",
                                        "bidBatch": "2020第二批",
                                        "S": 500,
                                        "H": 500,
                                        "C": 500,
                                        "distributionArea": "廊坊"
                                    }
                                ],
                                "handling_capacity": 700,
                                "cargo_status": {
                                    "newCount": 400,
                                    "oldCount": 350
                                },
                                "lineInfo": [
                                    {
                                        "lineName": "2楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "3楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "4楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "5楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                ],
                                "stacker_work_time": [
                                    {
                                        "stacker_id": 1,
                                        "normal_time": 7000,
                                        "ex_work_time": 996
                                    }
                                ]
                            }
                        ],
                        "risks": [
                            "content1",
                            "content2",
                            "content3"
                        ]
                    },
                    "optimized_plan": {
                        "summary": {
                            "efficiency": 128,
                            "line_usage": 74,
                            "cargo_usage": 85,
                            "ave_work_hour": 585
                        },
                        "detail": [
                            {
                                "date": "2022-01-02",
                                "cargo_usage": 85,
                                "modules": [
                                    {
                                        "type": "module1",
                                        "R": 999,
                                        "arrivedBatch": "2621212128223",
                                        "bidBatch": "2020第二批",
                                        "S": 999,
                                        "H": 500,
                                        "C": 500,
                                        "distributionArea": "廊坊"
                                    }
                                ],
                                "handling_capacity": 700,
                                "cargo_status": {
                                    "newCount": 400,
                                    "oldCount": 350
                                },
                                "lineInfo": [
                                    {
                                        "lineName": "2楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "3楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "4楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "5楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                ],
                                "stacker_work_time": [
                                    {
                                        "stacker_id": 1,
                                        "normal_time": 7000,
                                        "ex_work_time": 996
                                    }
                                ]
                            }
                        ],
                        "risks": [
                            "content1",
                            "content2",
                            "content3"
                        ]
                    }
                }
            }
        ]
    }
}
    return Report

def CreatReportJson():
    fp = codecs.open('outputReport.json', 'w+', 'utf-8')
    fp.write(json.dumps(Report,ensure_ascii=False,indent=4))
    fp.close()

#获取所有类型
def CALCOriginalType():
    global CargoNow
    #CargoNow =[{'x': 1868.62036, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 1, 'type': 10, 'id': 'A-5-1-1', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1901.27039, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 52, 'type': 10, 'id': 'B-6-52-1', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1894.86646, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 42, 'type': 10, 'id': 'A-7-42-1', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1896.14722, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 44, 'type': 10, 'id': 'B-8-44-1', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1891.02551, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 36, 'type': 10, 'id': 'A-9-36-1', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1883.98486, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 25, 'type': 10, 'id': 'B-10-25-1', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1877.58582, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 15, 'type': 10, 'id': 'A-11-15-2', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1873.74841, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 9, 'type': 10, 'id': 'B-12-9-1', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1883.3446, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 24, 'type': 11, 'id': 'A-13-24-1', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1887.82837, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 31, 'type': 11, 'id': 'B-14-31-1', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1898.70679, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 48, 'type': 11, 'id': 'A-15-48-1', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1869.26843, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 2, 'type': 11, 'id': 'A-5-2-1', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1900.63, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 51, 'type': 11, 'id': 'B-6-51-1', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1885.26343, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 27, 'type': 11, 'id': 'A-7-27-1', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1898.0625, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 47, 'type': 13, 'id': 'B-8-47-1', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1871.82764, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 6, 'type': 13, 'id': 'A-9-6-1', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1881.42786, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 21, 'type': 13, 'id': 'B-10-21-1', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1885.90771, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 28, 'type': 13, 'id': 'A-11-28-2', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1886.54578, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 29, 'type': 13, 'id': 'B-12-29-1', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1901.27039, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 52, 'type': 13, 'id': 'A-13-52-1', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1875.66882, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 12, 'type': 15, 'id': 'B-14-12-1', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1895.50488, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 43, 'type': 15, 'id': 'A-15-43-1', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1889.10876, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 33, 'type': 15, 'id': 'A-5-33-1', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1899.98157, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 50, 'type': 15, 'id': 'B-6-50-1', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1883.3446, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 24, 'type': 15, 'id': 'A-7-24-1', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1873.74841, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 9, 'type': 15, 'id': 'B-8-9-1', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1887.192, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 30, 'type': 15, 'id': 'A-9-30-2', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1879.50464, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 18, 'type': 16, 'id': 'B-10-18-1', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1898.70679, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 48, 'type': 16, 'id': 'A-11-48-2', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1894.2262, 'y': 3.84524536, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 5, 'column': 41, 'type': 16, 'id': 'B-12-41-5', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1898.0625, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 47, 'type': 16, 'id': 'A-13-47-1', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1869.90466, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 3, 'type': 16, 'id': 'B-14-3-1', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1891.65967, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 37, 'type': 16, 'id': 'A-15-37-1', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1869.90466, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 3, 'type': 16, 'id': 'A-5-3-1', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1880.78748, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 20, 'type': 16, 'id': 'B-6-20-1', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1869.26843, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 2, 'type': 16, 'id': 'A-7-2-1', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1876.94336, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 14, 'type': 16, 'id': 'B-8-14-1', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1899.34912, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 49, 'type': 16, 'id': 'A-9-49-2', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1876.94336, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 2, 'column': 14, 'type': 16, 'id': 'B-10-14-2', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 40}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 41}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 1, 's2': 0, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 42}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 43}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 44}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 45}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 47}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 48}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 49}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 50}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 51}, 
                # {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 52}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 53}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 54}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 55}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 0, 's2': 1, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 56}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 57}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 58}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 59}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 61}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 62}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 63}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 64}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 65}, {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 66}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 67}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 68}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 69}, {'x': 1901.27039, 'y': 8.452438, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 11, 'column': 52, 'type': 10, 'id': 'A-11-52-11', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 70}, {'x': 1901.27039, 'y': 6.916702, 'z': 44.90394, 's1': 1, 's2': 1, 'flag': 'B', 'line': 10, 'row': 9, 'column': 52, 'type': 11, 'id': 'B-10-52-9', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1901.27039, 'y': 6.916702, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 9, 'column': 52, 'type': 11, 'id': 'A-13-52-9', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1901.27039, 'y': 11.5238724, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 15, 'column': 52, 'type': 11, 'id': 'A-7-52-15', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1901.27039, 'y': 11.5238724, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 15, 'column': 52, 'type': 11, 'id': 'B-6-52-15', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 74}, {'x': 1901.27039, 'y': 13.8274679, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 18, 'column': 52, 'type': 11, 'id': 'B-14-52-18', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 75}, {'x': 1901.27039, 'y': 4.613105, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 6, 'column': 52, 'type': 11, 'id': 'B-12-52-6', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 77}, {'x': 1898.70679, 'y': 0.7738123, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 1, 'column': 48, 'type': 13, 'id': 'A-9-48-1', 'bidBatch': '2019年第二批', 'factory': '宁波三星', 'num': 78}, {'x': 1898.70679, 'y': 0.7738123, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 1, 'column': 48, 'type': 13, 'id': 'B-6-48-1', 'bidBatch': '2019年第二批', 'factory': '宁夏隆基', 'num': 79}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 80}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 81}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 82}, {'x': 1901.27039, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 52, 'type': 15, 'id': 'A-13-52-3', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1901.27039, 'y': 13.8274679, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 18, 'column': 52, 'type': 15, 'id': 'A-7-52-18', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 84}]
    CargoNow = CargoOriginal[Days]
    LisType = []
    for i in CargoNow:
        LisType.append(int(i['type']))
    LisType = delList(LisType)
    LisType = sorted(LisType)
    return LisType
#原计划批次号
def OriginalBatch():
    global Report
    indexModules = 0
    type = 0
    with open('D:/月原计划/实际出库计划.json', 'r', encoding='gb2312') as load_f:
        OutData = json.load(load_f)
    with open('D:/月原计划/实际入库计划.json', 'r', encoding='gb2312') as load_f:
        EnterData = json.load(load_f)
    with open('D:/月原计划/实际检定计划.json', 'r', encoding='gb2312') as load_f:
        InspectData = json.load(load_f)
    Days = 0
    for Days in range(len(OutData['采集终端'])):
        indexModules = 0
        for i in OutData:
            if(i == '采集终端'):
                type = 14
            elif(i == '单相表'):
                type = 10
            elif(i == '集中器'):
                type = 12
            elif(i == '电能表'):
                type = 13
            elif(i == '三相表（1级）'):
                type = 11
            elif(i == '三相表（0.5S级）'):
                type = 15
            elif(i == '三相表（0.2S级）'):
                type = 16
            #if EnterData[i][29]:
            #print(InspectData[i][26])
            if OutData[i][Days]:
                #print(i,Days)
                for j in range(len(OutData['%s'%(i)][Days])):
                    try:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    except IndexError:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = OutData['%s'%(i)][Days][j][4]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = OutData['%s'%(i)][Days][j][5]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = OutData['%s'%(i)][Days][j][1]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = OutData['%s'%(i)][Days][j][2]
                    #if(j+1 < len(OutData['%s'%(i)][Days])):
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                    indexModules += 1
            else:
                pass
            if EnterData[i][Days]:
                
                for j in range(len(EnterData['%s'%(i)][Days])):
                    if EnterData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == EnterData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == EnterData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["R"] = EnterData['%s'%(i)][Days][j][4]
                    else:
                        try:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = EnterData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = EnterData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = EnterData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = EnterData['%s'%(i)][Days][j][2]
                        #if(j+1 < len(EnterData['%s'%(i)][Days])):
                        #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass
            if InspectData[i][Days]:
                for j in range(len(InspectData['%s'%(i)][Days])):
                    if InspectData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == InspectData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == InspectData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["H"] = InspectData['%s'%(i)][Days][j][4]
                    else:   
                        try:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = InspectData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = InspectData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = InspectData['%s'%(i)][Days][j][2]
                        # if(j+1 < len(InspectData['%s'%(i)][Days])):
                        #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass
#优化计划批次号
def OptimizedBatch():
    global Report
    indexModules = 0
    type = 0
    with open('D:/月优化计划/月度出库计划.json', 'r', encoding='gb2312') as load_f:
        OutData = json.load(load_f)
    with open('D:/月优化计划/月度入库计划.json', 'r', encoding='gb2312') as load_f:
        EnterData = json.load(load_f)
    with open('D:/月优化计划/月度检定计划.json', 'r', encoding='gb2312') as load_f:
        InspectData = json.load(load_f)
    Days = 0
    for Days in range(len(OutData['采集终端'])):
        indexModules = 0
        for i in OutData:
            if(i == '采集终端'):
                type = 14
            elif(i == '单相表'):
                type = 10
            elif(i == '集中器'):
                type = 12
            elif(i == '电能表'):
                type = 13
            elif(i == '三相表（1级）'):
                type = 11
            elif(i == '三相表（0.5S级）'):
                type = 15
            elif(i == '三相表（0.2S级）'):
                type = 16
            #if EnterData[i][29]:
            #print(InspectData[i][26])
            if OutData[i][Days]:
                #print(i,Days)
                for j in range(len(OutData['%s'%(i)][Days])):
                    try:
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    except IndexError:
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][0])
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["C"] = OutData['%s'%(i)][Days][j][4]
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = OutData['%s'%(i)][Days][j][0]
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = OutData['%s'%(i)][Days][j][1]
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = OutData['%s'%(i)][Days][j][2]
                    #if(j+1 < len(OutData['%s'%(i)][Days])):
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                    indexModules += 1
            else:
                pass
            if EnterData[i][Days]:
                
                for j in range(len(EnterData['%s'%(i)][Days])):
                    if EnterData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == EnterData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == EnterData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["R"] = EnterData['%s'%(i)][Days][j][4]
                    else:
                        try:
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["R"] = EnterData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = EnterData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = EnterData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = EnterData['%s'%(i)][Days][j][2]
                        #if(j+1 < len(EnterData['%s'%(i)][Days])):
                        #Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                        #Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass
            if InspectData[i][Days]:
                for j in range(len(InspectData['%s'%(i)][Days])):
                    if InspectData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == InspectData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == InspectData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["H"] = InspectData['%s'%(i)][Days][j][4]
                    else:   
                        try:
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["H"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = InspectData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = InspectData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = InspectData['%s'%(i)][Days][j][2]
                        # if(j+1 < len(InspectData['%s'%(i)][Days])):
                        #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                        #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass

#报文函数
def GetOriginalReport():
    global Report
    if Days > 0:
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'].append([])
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][0])
    if(CargoOriginal[Days]):
        pass
    else:
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days] = null
        return 0
    global LisInspectTaskTime
    global CargoNow
    
    # CargoNow =[{'x': 1868.62036, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 1, 'type': 10, 'id': 'A-5-1-1', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1901.27039, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 52, 'type': 10, 'id': 'B-6-52-1', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1894.86646, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 42, 'type': 10, 'id': 'A-7-42-1', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1896.14722, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 44, 'type': 10, 'id': 'B-8-44-1', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1891.02551, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 36, 'type': 10, 'id': 'A-9-36-1', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1883.98486, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 25, 'type': 10, 'id': 'B-10-25-1', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1877.58582, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 15, 'type': 10, 'id': 'A-11-15-2', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1873.74841, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 9, 'type': 10, 'id': 'B-12-9-1', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1883.3446, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 24, 'type': 11, 'id': 'A-13-24-1', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1887.82837, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 31, 'type': 11, 'id': 'B-14-31-1', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1898.70679, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 48, 'type': 11, 'id': 'A-15-48-1', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1869.26843, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 2, 'type': 11, 'id': 'A-5-2-1', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1900.63, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 51, 'type': 11, 'id': 'B-6-51-1', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1885.26343, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 27, 'type': 11, 'id': 'A-7-27-1', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1898.0625, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 47, 'type': 13, 'id': 'B-8-47-1', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1871.82764, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 6, 'type': 13, 'id': 'A-9-6-1', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1881.42786, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 21, 'type': 13, 'id': 'B-10-21-1', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1885.90771, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 28, 'type': 13, 'id': 'A-11-28-2', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1886.54578, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 29, 'type': 13, 'id': 'B-12-29-1', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1901.27039, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 52, 'type': 13, 'id': 'A-13-52-1', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1875.66882, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 12, 'type': 15, 'id': 'B-14-12-1', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1895.50488, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 43, 'type': 15, 'id': 'A-15-43-1', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1889.10876, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 33, 'type': 15, 'id': 'A-5-33-1', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1899.98157, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 50, 'type': 15, 'id': 'B-6-50-1', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1883.3446, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 24, 'type': 15, 'id': 'A-7-24-1', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1873.74841, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 9, 'type': 15, 'id': 'B-8-9-1', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1887.192, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 30, 'type': 15, 'id': 'A-9-30-2', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1879.50464, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 18, 'type': 16, 'id': 'B-10-18-1', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1898.70679, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 48, 'type': 16, 'id': 'A-11-48-2', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1894.2262, 'y': 3.84524536, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 5, 'column': 41, 'type': 16, 'id': 'B-12-41-5', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1898.0625, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 47, 'type': 16, 'id': 'A-13-47-1', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1869.90466, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 3, 'type': 16, 'id': 'B-14-3-1', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1891.65967, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 37, 'type': 16, 'id': 'A-15-37-1', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1869.90466, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 3, 'type': 16, 'id': 'A-5-3-1', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1880.78748, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 20, 'type': 16, 'id': 'B-6-20-1', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1869.26843, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 2, 'type': 16, 'id': 'A-7-2-1', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1876.94336, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 14, 'type': 16, 'id': 'B-8-14-1', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1899.34912, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 49, 'type': 16, 'id': 'A-9-49-2', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1876.94336, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 2, 'column': 14, 'type': 16, 'id': 'B-10-14-2', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 40}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 41}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 1, 's2': 0, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 42}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 43}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 44}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 45}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 47}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 48}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 49}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 50}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 51}, 
    #                 {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 52}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 53}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 54}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 55}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 0, 's2': 1, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 56}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 57}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 58}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 59}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 61}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 62}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 63}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 64}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 65}, {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 66}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 67}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 68}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 69}, {'x': 1901.27039, 'y': 8.452438, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 11, 'column': 52, 'type': 10, 'id': 'A-11-52-11', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 70}, {'x': 1901.27039, 'y': 6.916702, 'z': 44.90394, 's1': 1, 's2': 1, 'flag': 'B', 'line': 10, 'row': 9, 'column': 52, 'type': 11, 'id': 'B-10-52-9', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1901.27039, 'y': 6.916702, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 9, 'column': 52, 'type': 11, 'id': 'A-13-52-9', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1901.27039, 'y': 11.5238724, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 15, 'column': 52, 'type': 11, 'id': 'A-7-52-15', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1901.27039, 'y': 11.5238724, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 15, 'column': 52, 'type': 11, 'id': 'B-6-52-15', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 74}, {'x': 1901.27039, 'y': 13.8274679, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 18, 'column': 52, 'type': 11, 'id': 'B-14-52-18', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 75}, {'x': 1901.27039, 'y': 4.613105, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 6, 'column': 52, 'type': 11, 'id': 'B-12-52-6', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 77}, {'x': 1898.70679, 'y': 0.7738123, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 1, 'column': 48, 'type': 13, 'id': 'A-9-48-1', 'bidBatch': '2019年第二批', 'factory': '宁波三星', 'num': 78}, {'x': 1898.70679, 'y': 0.7738123, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 1, 'column': 48, 'type': 13, 'id': 'B-6-48-1', 'bidBatch': '2019年第二批', 'factory': '宁夏隆基', 'num': 79}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 80}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 81}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 82}, {'x': 1901.27039, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 52, 'type': 15, 'id': 'A-13-52-3', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1901.27039, 'y': 13.8274679, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 18, 'column': 52, 'type': 15, 'id': 'A-7-52-18', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 84}]
    CargoNow = CargoOriginal[Days]
    #initCode(PlanFlag)
    #initReportJson()
    LisType = CALCOriginalType()
    #print(len(LisType))
    #获取所有类型
    # for i in range(len(LisType)-1):
    #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append({})
    #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i])
    #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i]['type'] = str(LisType[i])
    #     if(i == len(LisType)-2):
    #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i+1]['type'] = str(LisType[i+1])

    #获取所有类型及数量
    # dirType = {}
    # LisNum = [0,0,0,0]
    r = 0
    s = 0
    h = 0
    c = 0
    for i in range(len(LisType)):
        r = 0
        s = 0
        h = 0
        c = 0
        for j in CargoNow:
            if(int(j['type']) == LisType[i]):
                if(j['s1'] == 0 and j['s2'] == 0):
                    r += 1
                elif(j['s1'] == 0 and j['s2'] == 1):
                    s += 1
                elif(j['s1'] == 1 and j['s2'] == 0):
                    h += 1
                elif(j['s1'] == 1 and j['s2'] == 1):
                    c += 1
                else:
                    print("GetReport CargoNow error!")
        #原计划
        # for k in range(len(LisType)):
        #     if(LisType[i] ==  int(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['type'])):
        #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['R'] = r
        #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['S'] = s
        #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['H'] = h
        #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['C'] = c
        #         break
    #print(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'])
    #各个堆垛机的时间
    for i in range(len(LisDdjTime)-1):
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'].append({})
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i])
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['stacker_id'] = i+1
        if(i == len(LisDdjTime)-2):
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['stacker_id'] = i+2
            if(LisDdjTime[i+1] > 28800):
                Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['normal_time'] = 28800
                Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['ex_work_time'] =round(LisDdjTime[i+1] - 28800,3)
            else:
                Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['normal_time'] = LisDdjTime[i+1]
                Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['ex_work_time'] = 0
        if(LisDdjTime[i] > 28800):
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['normal_time'] = 28800
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['ex_work_time'] =round(LisDdjTime[i] - 28800,3)
        else:
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['normal_time'] = LisDdjTime[i]
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['ex_work_time'] = 0

    #方案综述
    totalTime = 0
    for i in LisDdjTime:
        totalTime += i
    Report['data']['reports'][0]['reportContent']['original_plan']['summary']['ave_work_hour'] = round(totalTime/len(LisDdjTime),3)
    Report['data']['reports'][0]['reportContent']['original_plan']['handling_capacity'] = len(CargoNow)
    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['cargo_status']['newCount'] = 4327 - S + R
    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['cargo_status']['oldCount'] = 8041 - C + H
    #print(LisInspect)
    # LisInspectTaskTime = [[],[],[],[]]
    # LisInspectTaskNum = [0,0,0,0]
    LisInspectTimeX = [0,0,0,0]
    for i in range(len(LisInspectTaskTime)):
        if LisInspectTaskTime[i]:
            LisInspectTaskTime[i] = sorted(LisInspectTaskTime[i])
            LisInspectTimeX[i] = abs(LisInspectTaskTime[i][0] - LisInspectTaskTime[i][-1])
    for i in range(len(LisInspect)):
        typeLis = []
        for j in LisInspect[i]:
            typeLis = LisInspect[i].get('%d'%(int(j)))
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['assertType'] = typeLis
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['checkCount'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['backStorage'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['inStorage'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['humanTime'] = "03:49:24"
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['useRate'] = round(LisInspectTaskNum[i] / 60,3)
        if(LisInspectTimeX[i] > 28800):
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['workTime'] = strftime("%H:%M:%S", gmtime(28800))
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['overTime'] = strftime("%H:%M:%S", gmtime(abs(LisInspectTimeX[i] - 28800)))
        else:
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['workTime'] = strftime("%H:%M:%S", gmtime(LisInspectTimeX[i]))
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['overTime'] = strftime("%H:%M:%S", gmtime(0))
            
        pass
    if Days > 0:
        for i in range(len(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'])):
            try:
                if Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]:
                    pass
                else:
                    del Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][-1]
            except IndexError:
                del Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][-1]
                # print(i)
                # print("original_plan stacker_work_time IndexError")
                pass
        # for i in range(len(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'])):
        #     try:
        #         if Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i]:
        #             pass
        #         else:
        #             del Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][-1]
        #     except IndexError:
        #         del Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][-1]
        #         # print(i)
        #         # print("original_plan modules IndexError")
        #         pass
        #日期
    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['date'] = str(datetime.date(2022, 4, Days+1))
    #立库利用效率
    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['cargo_usage'] = len(CargoNow)/10
    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'] = delList(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'])
    lineCount = 0
    cargoCount = 0
    line_usage = 0
    cargo_usage = 0
    ddj_count = 0
    ddj_usage = 0
    ddj_time = 0
    #方案综述：最终计算
    if(Days == (len(CargoOptimized)-1)):
        OriginalBatch()
        for i in range(Days):
            for j in range(len(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'])):
                lineCount += 1
                line_usage += Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][j]['useRate']
            cargo_usage += Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['cargo_usage']
            for k in range(len(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'])):
                ddj_count += 1
                ddj_time += int(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][k]['normal_time']) + int(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][k]['ex_work_time'])
        Report['data']['reports'][0]['reportContent']['original_plan']['summary']['line_usage'] = round(line_usage/lineCount*100 ,3)
        Report['data']['reports'][0]['reportContent']['original_plan']['summary']['cargo_usage'] = round(cargo_usage/Days+1,3)
        Report['data']['reports'][0]['reportContent']['original_plan']['summary']['ave_work_hour'] = round(ddj_time/60/ddj_count,3)
        Report['data']['reports'][0]['reportContent']['original_plan']['summary']['efficiency'] = round(0.5*round(line_usage/lineCount*100 ,3) +0.5*round(cargo_usage/Days+1,3) ,3)
    #CreatReportJson()
    
def CALCType():
    global CargoNow
    #CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
    CargoNow = CargoOptimized[Days]
    LisType = []
    for i in CargoNow:
        LisType.append(int(i['type']))
    LisType = delList(LisType)
    LisType = sorted(LisType)
    return LisType
#报文函数
def GetOptimizedReport():
    global CargoNow
    global Report
    #CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
    CargoNow = CargoOptimized[Days]
    if Days > 0:
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'].append([])
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][0])
    #initCode(PlanFlag)
    #initReportJson()
    LisType = CALCType()
    #print(len(LisType))
    #获取所有类型
    # for i in range(len(LisType)-1):
    #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append({})
    #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i])
    #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i]['type'] = str(LisType[i])
    #     if(i == len(LisType)-2):
    #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i+1]['type'] = str(LisType[i+1])
    #获取所有类型及数量
    # dirType = {}
    # LisNum = [0,0,0,0]
    r = 0
    s = 0
    h = 0
    c = 0
    for i in range(len(LisType)):
        r = 0
        s = 0
        h = 0
        c = 0
        for j in CargoNow:
            if(int(j['type']) == LisType[i]):
                if(j['s1'] == 0 and j['s2'] == 0):
                    r += 1
                elif(j['s1'] == 0 and j['s2'] == 1):
                    s += 1
                elif(j['s1'] == 1 and j['s2'] == 0):
                    h += 1
                elif(j['s1'] == 1 and j['s2'] == 1):
                    c += 1
                else:
                    print("GetReport CargoNow error!")
        #优化计划
        # for k in range(len(LisType)):
        #     if(LisType[i] ==  int(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['type'])):
        #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['R'] = r
        #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['S'] = s
        #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['H'] = h
        #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['C'] = c
        #         break
    #各个堆垛机的时间
    for i in range(len(LisDdjTime)-1):
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'].append({})
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i])
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['stacker_id'] = i+1
        if(i == len(LisDdjTime)-2):
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['stacker_id'] = i+2
            if(LisDdjTime[i] > 28800):
                Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['normal_time'] = 28800
                Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['ex_work_time'] = round(LisDdjTime[i+1] - 28800,3)
            else:
                Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['normal_time'] = LisDdjTime[i+1]
                Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['ex_work_time'] = 0
        if(LisDdjTime[i] > 28800):
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['normal_time'] = 28800
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['ex_work_time'] = round(LisDdjTime[i] - 28800,3)
        else:
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['normal_time'] = LisDdjTime[i]
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['ex_work_time'] = 0
    
        #方案综述
    totalTime = 0
    for i in LisDdjTime:
        totalTime += i
    Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['ave_work_hour'] = round(totalTime/len(LisDdjTime),3)
    Report['data']['reports'][0]['reportContent']['optimized_plan']['handling_capacity'] = len(CargoNow)
    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['cargo_status']['newCount'] = 4327 - S + R
    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['cargo_status']['oldCount'] = 8041 - C + H
    #print(LisInspect)
    # LisInspectTaskTime = [[],[],[],[]]
    # LisInspectTaskNum = [0,0,0,0]
    LisInspectTimeX = [0,0,0,0]
    for i in range(len(LisInspectTaskTime)):
        LisInspectTaskTime[i] = sorted(LisInspectTaskTime[i])
        try:
            LisInspectTimeX[i] = abs(LisInspectTaskTime[i][0] - LisInspectTaskTime[i][-1])
        except IndexError:
            LisInspectTimeX[i] = 0
    for i in range(len(LisInspect)):
        typeLis = []
        for j in LisInspect[i]:
            typeLis = LisInspect[i].get('%d'%(int(j)))
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['assertType'] = typeLis
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['checkCount'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['backStorage'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['inStorage'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['humanTime'] = "03:49:24"
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['useRate'] = round(LisInspectTaskNum[i] / 60,3)
        if(LisInspectTimeX[i] > 28800):
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['workTime'] = strftime("%H:%M:%S", gmtime(28800))
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['overTime'] = strftime("%H:%M:%S", gmtime(abs(LisInspectTimeX[i] - 28800)))
        else:
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['workTime'] = strftime("%H:%M:%S", gmtime(LisInspectTimeX[i]))
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['overTime'] = strftime("%H:%M:%S", gmtime(0))
            
        pass
    #if Days > 0:
    for i in range(len(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'])):
        try:
            if Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]:
                pass
            else:
                del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][-1]
        except IndexError:
            del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][-1]
            #del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][-1]
            # print(i)
            # print("optimized_plan stacker_work_time IndexError")
            pass
    # for i in range(len(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'])):
    #     try:
    #         if Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i]:
    #             pass
    #         else:
    #             del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][-1]
    #     except IndexError:
    #         del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][-1]
    #         # print(i)
    #         # print("optimized_plan modules IndexError")
    #         pass
        #日期
    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['date'] = str(datetime.date(2022, 4, Days+1))
    #立库利用效率
    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['cargo_usage'] = len(CargoNow)/10
    #Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'] = delList(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'])
    lineCount = 0
    cargoCount = 0
    line_usage = 0
    cargo_usage = 0
    ddj_count = 0
    ddj_usage = 0
    ddj_time = 0
    #方案综述：最终计算
    if(Days == (len(CargoOptimized)-1)):
        OptimizedBatch()
        for i in range(Days):
            for j in range(len(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'])):
                lineCount += 1
                line_usage += Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][j]['useRate']
            cargo_usage += Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['cargo_usage']
            for k in range(len(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'])):
                ddj_count += 1
                ddj_time += int(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][k]['normal_time']) + int(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][k]['ex_work_time'])
        Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['line_usage'] = round(line_usage/lineCount*100 ,3)
        Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['cargo_usage'] = round(cargo_usage/Days+1,3)
        Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['ave_work_hour'] = round(ddj_time/60/ddj_count,3)
        Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['efficiency'] = round(0.5*round(line_usage/lineCount*100 ,3) +0.5*round(cargo_usage/Days+1,3) ,3)
    
    if Days == (len(CargoOptimized)-1) :
        CreatReportJson()
###
#GetReport()

#排列组合，C
def FunC(m,n):
    a=b=result=1 
    if m < n:
        pass
        # print("n不能于m且均为整数") 
    elif ((type(m)!=int) or (type(n)!=int)): 
        pass
        #print("n不能于m且均为整数") 
    else:
        minNI=min(n,m-n)#使运算最简便 
        for j in range(0,minNI):
        #使变量a,b让所的分母相乘后除以所有的分
            a=a*(m-j)
            b=b*(minNI-j)
            result=a//b#在此使“/”和“//”均可，因为a除以b为整数 
    return result
#print(FunC(4,2))  ---6

#对上货编码按照类型进行排序
def SortEnterCode(LisCode):
    item = FunC(len(LisTypeOrder),2)#排列组合次数
    if item == 1:
        return LisCode
    LisItemTemp = []#储存每个类型的匹配次数
    temp = len(LisTypeOrder)
    for i in range(len(LisTypeOrder) - 1):
        LisItemTemp.append(temp - 1)
        temp -= 1
    #print(LisItemTemp)
    LisMatchType = []
    indexInit = 1 #初始，要匹配的LisTypeOrder 下标
    indexStand = 1 # indexInit 初始化的指标
    for i in range(len(LisItemTemp)):
        LisMatchType.append([])
        for j in range(LisItemTemp[i]):
            LisMatchType[i].append(int(LisTypeOrder[indexInit]))
            indexInit += 1
        indexStand += 1
        indexInit = indexStand
    #print(LisMatchType)
    #开始按照 LisTypeOrder 存储的顺序进行匹配
    num = 0#当前匹配的类型索引
    #numPassive = 1# 当前被匹配的类型索引 
    for x in range(item):
        if x+1 == LisItemTemp[num]:
            num += 1
            #进入下一个匹配
        for i in range (len(LisCode)):
            if CargoNow[LisCode[i] - 1]['s1'] == 0 and CargoNow[LisCode[i] - 1]['s2'] == 0:
                if CargoNow[LisCode[i] - 1]['type'] == int(LisTypeOrder[num]):
                    for j in range (len(LisCode)):
                        if CargoNow[LisCode[j] - 1]['s1'] == 0 and CargoNow[LisCode[j] - 1]['s2'] == 0:
                            if CargoNow[LisCode[j] - 1]['type'] in LisMatchType[num]:
                                if j < i:
                                    temp = LisCode[i]
                                    LisCode[i] = LisCode[j]
                                    LisCode[j] = temp
                                    break
    #  for x in range (item):
    #     if x+1 == LisItemTemp[num]:
    #         num += 1
    #         #进入下一个匹配
    #     for i in range (len(LisCode)):
    #         if CargoNow[LisCode[i] - 1]['s1'] == 0 and CargoNow[LisCode[i] - 1]['s2'] == 0:
    #             if CargoNow[LisCode[i] - 1]['type'] == int(LisTypeOrder[num]):
    #                 for j in range (len(LisCode)):
    #                     if CargoNow[LisCode[j] - 1]['s1'] == 0 and CargoNow[LisCode[j] - 1]['s2'] == 0:
    #                         if CargoNow[LisCode[j] - 1]['type'] == int(LisTypeOrder[numPassive]):
    #                             if j < i:
    #                                 temp = LisCode[i]
    #                                 LisCode[i] = LisCode[j]
    #                                 LisCode[j] = temp
    #                                 break
    #                     pass
    #             pass
    #     # 自增或者重置 numPassive
    #     if numPassive == len(LisTypeOrder) - 1:
    #         numPassive = num + 1
    #     else:
    #         numPassive += 1
    
    pass
    return LisCode

#根据资产类型计算垛容量
def CALCcontain(type):
    if type == 14 or type == 19 or type == 12:
        return 12
    elif type == 10:
        return 60
    elif type == 13:
        return 36
    elif type == 11 or type == 15 or type == 16:
        return 20
    elif type == 18:
        return 90
    elif type == 17:
        return 180
    else:
        print("CALCcontain type Error!")

### 上货点任务流
def TaskUpLoad(LisCode):
    initCode(PlanFlag)
    global LisGoodsNum
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisGoodsNum = CALCLisGoodsNum()
    LisCrossTime = CALCupLoadFirstCrossTime(LisCross)
    LisCrossTime = sorted(LisCrossTime.items(), key=lambda item:item[1], reverse = True) #按照 value 倒序排序
    FoldToDdj()
    #LisCrossTime =  sorted(LisCrossTime,reverse=True)
    upLoadNum = len(LisCrossTime)
    LoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum)
    LisUpLoadType = list(LisGoodsNum[0].keys())
    for i in range(len(LisUpLoadType)):
        LisUpLoadType[i] = int(LisUpLoadType[i])
    LisUpLoadType = sorted(LisUpLoadType)
    # print(LisUpLoadType)
    # print(LoadGoodsNum)
    # print(LisupLoadParm)
    LisUpLoadTotal = []
    for i in range(len(LoadGoodsNum)):
        total = 0
        for j in LoadGoodsNum[i]:
            total += j
        LisUpLoadTotal.append(total)
        
    totalNum = 0#入库总箱数
    for i in LisUpLoadTotal:
        totalNum += i
    
    LisRunTime = [[],[]]
    LisDdjCode = getLisDdjCode(LisCode)#按照堆垛机分割的数组
    LisDdjEnterCode = []
    for i in range(len(LisDdjCode)):
        LisDdjEnterCode.append([])
        for j in range(len(LisDdjCode[i])):
            if CargoNow[LisDdjCode[i][j] - 1]['s1'] == 0 and CargoNow[LisDdjCode[i][j] - 1]['s2'] == 0:
                LisDdjEnterCode[i].append(LisDdjCode[i][j])
    LisDdjEnterCodeT = copy.deepcopy(LisDdjEnterCode)
    #将所有入库编码整合到一个列表中
    LisEnterCode = []
    for i in range (len(LisDdjEnterCodeT[-1])+1):
        for j in range(len(LisDdjCode)):
            try:
                LisEnterCode.append(LisDdjEnterCode[j][0])
            except IndexError:
                continue
            if j < len(LisDdjEnterCode) - 1:
                try:
                    LisEnterCode.append(LisDdjEnterCode[j][1])
                    del LisDdjEnterCode[j][0]
                    del LisDdjEnterCode[j][0]
                except IndexError:
                    del LisDdjEnterCode[j][0]
                    #continue
            else:
                del LisDdjEnterCode[j][0]
        
    #print(LisEnterCode)
    
    mod = 0
    ufmod = 1
    enterIndex = 0#已读的入库编码的索引
    upLoad1 = 0#上货点1的已上货数量
    upLoad2 = 0
    upType = int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10
    typeNum = 0
    for i in range (totalNum):
        mod = CALCmod(str(CargoNow[LisEnterCode[enterIndex] - 1]['type']))
        false = False
        initJson()
        if ufmod > mod:
            enterIndex += 1
            ufmod = 1
        nowType = int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10
        if ((i+1) % 2 == 0):
            if upType == nowType:
                runTime =  LisupLoadParm[0][0] + LisupLoadParm[0][1] * upLoad1 + typeNum * 600
            else:
                
                typeNum += 1
                runTime =  LisupLoadParm[0][0] + LisupLoadParm[0][1] * upLoad1 + typeNum * 600
                #print(runTime)
            LisRunTime[0].append(runTime)
            upLoad1 += 1
            TaskFlow['data']['taskContent']['stackerMachines'] = null
            TaskFlow['version'] = "上货点1"
            TaskFlow['runTime'] = runTime
            TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = "上货点1"
            TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = str(int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10)
            TaskFlow['data']['taskContent']['loadPointTask'][0]['cumulativeTask'] = LisUpLoadTotal[0]
            TaskFlow['data']['taskContent']['loadPointTask'][0]['currentTask'] = upLoad1
            TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[LisEnterCode[enterIndex] - 1]['factory']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[LisEnterCode[enterIndex] - 1]['batchNum']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[LisEnterCode[enterIndex] - 1]['bidBatch']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['checkStatus'] = false
            TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CALCcontain(int(CargoNow[LisEnterCode[enterIndex] - 1]['type']))
            TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(LisEnterCode[enterIndex]) + 2) + ',' + CargoNow[LisEnterCode[enterIndex] - 1]['flag']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['outTask'] = C
            CreatJson()
        else:
            #print(CargoNow[LisEnterCode[enterIndex] - 1])
            if upType == nowType:
                runTime =  LisupLoadParm[0][0] + LisupLoadParm[0][1] * upLoad2 + typeNum * 600
            else:
                typeNum += 1
                runTime =  LisupLoadParm[0][0] + LisupLoadParm[0][1] * upLoad2 + typeNum * 600
                #print(runTime)
            #runTime =  LisupLoadParm[1][0] + LisupLoadParm[1][1] * upLoad2
            LisRunTime[1].append(runTime)
            upLoad2 += 1
            TaskFlow['data']['taskContent']['stackerMachines'] = null
            TaskFlow['version'] = "上货点2"
            TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
            TaskFlow['runTime'] = runTime
            TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = "上货点2"
            TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = str(int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10)
            TaskFlow['data']['taskContent']['loadPointTask'][0]['cumulativeTask'] = LisUpLoadTotal[1]
            TaskFlow['data']['taskContent']['loadPointTask'][0]['currentTask'] = upLoad2
            TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[LisEnterCode[enterIndex] - 1]['factory']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[LisEnterCode[enterIndex] - 1]['batchNum']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[LisEnterCode[enterIndex] - 1]['bidBatch']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['checkStatus'] = false
            TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CALCcontain(int(CargoNow[LisEnterCode[enterIndex] - 1]['type']))
            TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(LisEnterCode[enterIndex]) + 2) + ',' + CargoNow[LisEnterCode[enterIndex] - 1]['flag']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['outTask'] = C
            CreatJson()
        ufmod += 1 
        upType = int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10
        pass
    
    # for upLoadName in range(len(LoadGoodsNum)):
    #     runTime = 0
    #     readYet = 0
    #     for i in range(len(LoadGoodsNum[upLoadName])):
    #         for j in range(LoadGoodsNum[upLoadName][i]):
    #             runTime =  LisupLoadParm[upLoadName][0] + LisupLoadParm[upLoadName][1]*(j+readYet)
    #             LisRunTime[upLoadName].append(runTime)
    #             initJson()
    #             TaskFlow['data']['taskContent']['stackerMachines'] = null
    #             TaskFlow['version'] = "上货点%d"%(upLoadName+1)
    #             TaskFlow['runTime'] = runTime
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = "上货点%d"%(upLoadName+1)
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = LisUpLoadType[i]
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['cumulativeTask'] = LisUpLoadTotal[upLoadName]
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['outTask'] = C
    #             CreatJson()
    #         readYet += LoadGoodsNum[upLoadName][i]
    #print(LisRunTime)
    pass
####

#处理SC RS的编码
def RepeatReadCode(LisCode):
    LisRS = [[],[],[]]# r s h
    LisSC = [[],[],[]]# s h c
    for i in LisCode:
        if (CargoNow[i - 1]['sign'] == 'RS'):#拿到所有RS的
            if (CargoNow[i - 1]['s1'] == 0 and CargoNow[i - 1]['s2'] == 0):#拿到RS中 入库的
                LisRS[0].append(i)
                pass
            elif (CargoNow[i - 1]['s1'] == 0 and CargoNow[i - 1]['s2'] == 1):#拿到RS 中 送检的
                LisRS[1].append(i)
                pass
            elif (CargoNow[i - 1]['s1'] == 1 and CargoNow[i - 1]['s2'] == 0):# 拿到 RS中 回库的
                LisRS[2].append(i)
                pass
        elif (CargoNow[i - 1]['sign'] == 'SC'):
            if (CargoNow[i - 1]['s1'] == 0 and CargoNow[i - 1]['s2'] == 1): #拿到SC 中送检的
                LisSC[0].append(i)
                pass
            elif (CargoNow[i - 1]['s1'] == 1 and CargoNow[i - 1]['s2'] == 0):#拿到 SC 中回库的
                LisSC[1].append(i)
                pass
            elif (CargoNow[i - 1]['s1'] == 1 and CargoNow[i - 1]['s2'] == 1):#拿到SC 中出库的
                LisSC[2].append(i)
                pass
    LisRSCode = []#存放RS的编码 依次存放 每个小列表中的编码的id相同
    LisSCCode = []
    if (len(LisRS[0]) == 0 and len(LisSC[0]) == 0):
        return LisCode
    elif (len(LisRS[0]) != 0):#对RS处理
        for i  in range(len(LisRS[0])):
            LisRSCode.append([])
            LisRSCode[i].append(LisRS[0][i])
            for n in range(2):#拿到与R相同id的 送检、回库编码
                for j in range(len(LisRS[n])):
                    if CargoNow[LisRSCode[i][0]-1]['id'] == CargoNow[LisRS[n][j]-1]['id']:
                        LisRSCode[i].append(LisRS[n][j])
    #print(LisRSCode)    
    elif (len(LisSC[0]) != 0):#对RS处理
        for i  in range(len(LisSC[0])):
            LisSCCode.append([])
            LisSCCode[i].append(LisSC[0][i])
            for n in range(1,3):#拿到与R相同id的 送检、回库编码
                for j in range(len(LisSC[n])):
                    if CargoNow[LisSCCode[i][0]-1]['id'] == CargoNow[LisSC[n][j]-1]['id']:
                        LisSCCode[i].append(LisSC[n][j])   
        #print(LisSCCode)
    #print(LisCode)
    for n in range(2):
        if n == 0:
            Lis = LisRSCode
        else:
            Lis = LisSCCode
        for i in Lis:
            LisIndex = []#存放三个数的索引
            for j in i:
                for k in range(len(LisCode)):
                    if j == LisCode[k]:
                        LisIndex.append(k)
            #print("LisIndex",LisIndex)
        #判断索引值是否符合生产实际，如不符合，则调整编码前后次序
            if (LisIndex[0] < LisIndex[1] and LisIndex[1] < LisIndex[2]):
                pass
            elif (LisIndex[0] > LisIndex[1] and LisIndex[0] > LisIndex[2]):
                temp =  LisCode[LisIndex[0]]
                LisCode[LisIndex[0]] = LisCode[LisIndex[2]]
                LisCode[LisIndex[2]] = temp
                if (LisIndex[1] > LisIndex[2]):
                    pass
                else:
                    temp =  LisCode[LisIndex[1]]
                    LisCode[LisIndex[1]] = LisCode[LisIndex[2]]
                    LisCode[LisIndex[2]] = temp
            elif (LisIndex[1] > LisIndex[0] and LisIndex[1] > LisIndex[2]):
                temp =  LisCode[LisIndex[1]]
                LisCode[LisIndex[1]] = LisCode[LisIndex[2]]
                LisCode[LisIndex[2]] = temp
                if(LisIndex[0] > LisIndex[1]):
                    temp =  LisCode[LisIndex[1]]
                    LisCode[LisIndex[1]] = LisCode[LisIndex[0]]
                    LisCode[LisIndex[0]] = temp
            elif(LisIndex[2] > LisIndex[0] and LisIndex[2] > LisIndex[1]):
                if(LisIndex[0] > LisIndex[1]):
                    temp =  LisCode[LisIndex[1]]
                    LisCode[LisIndex[1]] = LisCode[LisIndex[0]]
                    LisCode[LisIndex[0]] = temp
                else:
                    print("RepeatReadCode 1 Error!")
            else:
                print("RepeatReadCode 2 Error!",LisIndex)
    #print(LisCode)
    
    return LisCode

def Fitness(LisCode,DdjData):
    GetDdjDataXYZ(DdjData)
    global LisDdjTime 
    LisDdjCode = getLisDdjCode(LisCode) #按照堆垛机区分
    GetS_H(LisDdjCode)
    global dirDdjTime
    dirDdjTime = {}
    Read(LisDdjCode)
    for i in range(len(LisDdjTime)):
        dirDdjTime['%d'%(i+1)] = LisDdjTime[i]
    print(dirDdjTime)
    LisDdjTime = sorted(LisDdjTime, reverse=True)
    print(LisDdjTime[0])
    return LisDdjTime[0]

def enSimpleCode(LisCode:list,DdjData):
    fp = codecs.open('output.json', 'w+', 'utf-8')
    #fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
    fp.close()
    global LisEnterTime
    initCode(PlanFlag)
    if R > 0:
        LisEnterTime = FoldToDdj()
        LisCode = SortEnterCode(LisCode)
        LisCode = RepeatReadCode(LisCode)
        
        TaskUpLoad(LisCode)#上货点任务流
        initCode(PlanFlag)
    if(type(LisCode) == list and type(LisCode[0]) == int and type(LisCode[-1]) == int):
        #print("yes!")
        #LisEnterTime = cal(LisCode,5) #叠箱机到堆垛机入库口
        LisEnterTime = FoldToDdj()
        fitness = round(Fitness(LisCode,DdjData),3)
        return fitness
    else:
        print("LisCode Error!")
        return 0

def CALCLisCode(PlanFlag):
    initCode(PlanFlag)
    s = [x for x in range(1, len(CargoNow)+1)]
    random.shuffle(s)
    return s

#LisCode = [76, 2, 9, 14, 39, 22, 82, 60, 70, 58, 4, 59, 30, 74, 20, 80, 8, 71, 54, 48, 83, 65, 51, 75, 12, 36, 66, 34, 28, 73, 56, 13, 64, 68, 55, 24, 11, 45, 49, 26, 79, 46, 33, 18, 15, 10, 5, 27, 72, 31, 29, 23, 52, 38, 35, 6, 41, 25, 16, 69, 43, 19, 44, 1, 42, 40, 17, 84, 62, 32, 67, 61, 53, 63, 7, 50, 78, 37, 21, 77, 3, 57, 81, 47]
#print(len(LisCode))

# LisCode = CALCLisCode()
# print(LisCode)
# DdjData = ddjData_sql.getStacks()
# print(enSimpleCode(LisCode,DdjData))
# print(enSimpleCode(LisCode,DdjData))
#print(cal(LisCode,5))

# print(len(CargoNow_sql.getGoodsLocationInfoVice()))
#print(ddjData_sql.getStacks()[0])
def main():
    global Days
    global Report
    global PlanFlag
    Days = 0
    Report = initReportJson()
    DdjData = ddjData_sql.getStacks()
    if len(CargoOriginal) == len(CargoOptimized) :
        for i in range(len(CargoOptimized)):
            PlanFlag = False
            if(CargoOriginal[i]):
                LisCode = CALCLisCode(PlanFlag)
                #LisCode = LisOriginalCode[Days]
                enSimpleCode(LisCode,DdjData)
            GetOriginalReport()
            # PlanFlag = False
            # LisCode = CALCLisCode()
            # #LisCode = LisOriginalCode[Days]
            # enSimpleCode(LisCode,DdjData)
            # GetOriginalReport()
            PlanFlag = True
            LisCode = CALCLisCode(PlanFlag)
            #LisCode = LisOptimizedCode[Days]
            enSimpleCode(LisCode,DdjData)
            GetOptimizedReport()
            Days += 1
    else:
        print("len(CargoOriginal) != len(CargoOptimized) !")
    # Days = 0
    # for i in range(len(CargoOriginal)):
    #     PlanFlag = False
    #     if(CargoOriginal[i]):
    #         LisCode = CALCLisCode(PlanFlag)
    #         #LisCode = LisOriginalCode[Days]
    #         enSimpleCode(LisCode,DdjData)
    #     GetOriginalReport()
    #     Days += 1
#main()
# fp = codecs.open('outputReport.json', 'w+', 'utf-8')
# Lis = CargoNow_sql.getGoodsLocationInfoVice()
# fp.write(str(Lis))
# fp.close()

def CodeTest():
    Code = []
    s = 0
    c = 0
    r = 0
    h = 0
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'S':
            Code.append(int(CargoNow[i]['item']))
            s += 1
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'C':
            Code.append(int(CargoNow[i]['item']))
            c += 1
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'R':
            Code.append(int(CargoNow[i]['item']))
            r += 1
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'H':
            Code.append(int(CargoNow[i]['item']))
            h += 1
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'R' or CargoNow[i]['sign'] == 'S' or CargoNow[i]['sign'] == 'H' or CargoNow[i]['sign'] == 'C':
            pass
        else:
            if(CargoNow[i]['sign'] == 'RS'):
                if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0):#入库
                    Code.insert(s+c,int(CargoNow[i]['item']))
                    pass
                elif(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):#送检
                    Code.insert(s+c+2,int(CargoNow[i]['item']))
                    pass
                elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 0):#回库
                    Code.insert(s+c+r+h-1,int(CargoNow[i]['item']))
                    pass
                pass
            if(CargoNow[i]['sign'] == 'SC'):
                if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):#送检
                    Code.insert(0,int(CargoNow[i]['item']))
                    pass
                elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 0):#回库
                    Code.insert(s+c,int(CargoNow[i]['item']))
                    pass
                elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 1):#出库
                    Code.insert(s+c+2,int(CargoNow[i]['item']))
                    pass
                pass
            # print(CargoNow[i]['sign'])
            # print(CargoNow[i]['id'])
    return Code
    

def test():
    global Days
    global Report
    global PlanFlag
    Days = 0
    PlanFlag = False
    initCode(PlanFlag)
    #LisCode =[42, 16, 21, 17, 50, 23, 12, 44, 27, 39, 48, 41, 55, 36, 22, 13, 37, 57, 31, 45, 46, 38, 26, 56, 61, 47, 19, 60, 53, 65, 32, 2, 66, 43, 51, 18, 1, 62, 58, 59, 52, 49, 8, 5, 7, 24, 6, 63, 34, 69, 4, 54, 40, 28, 3, 68, 35, 64, 33, 20, 11, 25, 29, 10, 67, 15, 30, 14, 9]
    #LisCode = CodeTest()
    #LisCode =[29, 6, 24, 50, 11, 23, 26, 12, 57, 36, 30, 48, 34, 19, 32, 1, 41, 17, 21, 28, 14, 52, 9, 53, 31, 45, 25, 56, 46, 7, 5, 51, 47, 39, 22, 27, 38, 54, 40,15, 44, 20, 55, 42, 2, 13, 4, 8, 33, 18, 49, 37, 16, 35, 43, 10, 3]
    #LisCode = [304,  240, 176, 42, 253, 342, 208, 255, 83, 87, 58, 276, 72, 327, 248, 224, 280, 212, 244, 254, 10, 247, 245, 63, 103, 312, 20, 293, 196, 168, 344,278, 100, 306, 307, 318, 221, 266, 186, 289, 6, 99, 211, 316, 324, 57, 152,39, 339, 97, 130, 66, 199, 89, 282, 7, 223, 19, 341, 263, 69, 8, 226, 1, 305, 118, 201, 114, 195, 237, 256, 299, 53, 101, 145, 3, 249, 82, 79, 131, 94,47, 274, 135, 313, 214, 170, 155, 36, 141, 203, 106, 213, 122, 121, 74, 264, 159, 286, 21, 178, 323, 49, 34, 314, 242, 41, 207, 279, 123, 332, 98, 161,165, 225, 143, 205, 222, 281, 181, 187, 68, 73, 171, 55, 92, 33, 217, 294, 75, 231, 59, 269, 200, 193, 67, 48, 105, 163, 162, 37, 77, 227, 43, 24, 93, 275, 154, 258, 109, 309, 177, 183, 12, 238, 321, 296, 290, 219, 233, 142, 331, 335, 243, 251, 326, 56, 273, 308, 172, 330, 311, 78, 194, 65, 96, 232, 108, 111, 328, 188, 322, 110, 50, 184, 334, 204, 228, 285, 126, 84, 25, 300, 70, 206, 336, 40, 303, 46, 45, 151, 252, 9, 287, 156, 102, 310, 298, 340, 215, 153, 267, 220, 120, 38, 119, 189, 317, 28, 44, 51, 234, 18, 22, 117, 333, 144, 64, 85, 216, 31, 35, 230, 32, 81, 291, 15, 80, 197, 284, 257, 61, 173, 137, 60, 218, 337, 148, 175, 76, 182, 272, 113, 180, 191, 112, 125, 14, 4, 17, 116, 62, 283, 29, 292, 16, 262, 295, 23, 90, 88, 190, 198, 345, 301, 179, 185, 169, 107, 147, 86, 235, 320, 241, 164, 319, 239, 5, 13, 11, 270, 71, 91, 174, 297, 133, 265, 95, 150, 209, 139, 27, 149, 54, 26, 129, 288, 343, 268, 104, 325, 250, 271, 261, 52, 210, 124, 138, 302, 192, 246, 146, 2, 136, 140, 132, 329, 260, 128, 236, 315, 277, 134, 259, 127, 157, 160, 202, 167, 338, 158, 115, 229, 30, 166]
#     LisCode = [261, 160, 283, 132, 415, 381, 99, 169, 434, 444, 352, 58, 191, 424, 173, 345, 276, 269, 14, 459, 243, 309, 213, 121, 230, 358, 77, 135, 317, 252, 164, 175, 374, 330, 129, 202, 246, 249, 371, 258, 362, 240, 250, 62, 255, 310, 436, 85, 234, 441, 55, 232, 157, 174, 201, 364, 214, 94, 351, 448, 118, 154, 311, 395, 304, 325, 264, 384, 22, 359, 337, 216, 421, 354, 39, 430, 313, 236, 336, 199, 91, 344, 63, 458, 327, 373, 80, 294, 406, 370, 342, 103, 133, 187, 292, 2, 446, 316, 84, 74, 220, 299, 128, 270, 437, 338, 333, 302, 360, 376, 59, 145, 340, 425, 273, 363, 115, 451, 300, 280, 356, 410, 393, 194, 235, 30,
# 420, 56, 54, 170, 149, 130, 114, 308, 24, 438, 45, 222, 431, 117, 217, 244, 404, 383, 192, 108, 265, 165, 379, 188, 9, 126, 328, 43, 203, 366, 158, 71, 427, 355, 332, 163, 34, 127, 289, 442, 141, 315, 320, 343, 97, 392, 456, 70, 122, 274, 447, 156, 307, 225, 254, 408, 40, 120, 349, 215, 423, 339, 279, 29, 180, 162, 87, 82, 86, 256, 380, 104, 110, 377, 50, 102, 277, 386, 282, 239, 47, 66, 198, 25, 229, 413, 168, 147, 396, 267, 26, 146, 319, 361, 95, 98, 365, 435, 312, 67, 257, 326, 152, 221, 125, 93, 73, 150, 16, 394, 36, 357, 412, 140, 10, 226, 83, 271, 33, 6, 46, 382, 184, 287, 388, 306, 197, 37, 399, 293, 72, 323, 60, 378, 38, 57, 148, 41, 210, 398, 341, 314, 455, 247, 348, 178, 64, 460, 190, 295, 228,
# 219, 440, 19, 241, 368, 195, 172, 428, 233, 385, 23, 183, 109, 453, 90, 161, 182, 391, 452, 322, 242,
# 179, 189, 353, 112, 144, 419, 321, 196, 153, 28, 443, 297, 171, 318, 106, 407, 403, 4, 138, 245, 278,
# 387, 449, 251, 181, 409, 42, 35, 151, 372, 206, 238, 411, 324, 11, 414, 75, 113, 275, 17, 418, 285, 416, 369, 367, 15, 272, 268, 76, 426, 329, 224, 100, 167, 402, 49, 177, 417, 281, 88, 237, 119, 284, 331, 101, 433, 375, 131, 92, 305, 301, 166, 186, 286, 439, 288, 211, 79, 65, 61, 432, 259, 31, 123, 111,
# 78, 260, 390, 13, 155, 143, 450, 296, 1, 290, 27, 185, 405, 401, 176, 227, 48, 116, 52, 204, 142, 350, 53, 7, 218, 346, 32, 44, 454, 445, 89, 212, 5, 68, 303, 263, 262, 8, 81, 137, 12, 207, 291, 231, 20,
# 334, 429, 159, 397, 335, 3, 266, 248, 389, 107, 253, 193, 96, 200, 347, 105, 18, 134, 21, 457, 462, 400, 223, 208, 205, 139, 69, 124, 136, 298, 51, 422, 461, 209]
    LisCode = [27, 426, 321, 353, 274, 147, 69, 43, 162, 138, 451, 331, 269, 291, 265, 385, 146, 264, 122, 125, 239, 418, 165, 436, 460, 377, 217, 117, 2, 314, 113, 131, 365, 462, 166, 433, 422, 387, 363, 408, 414, 110, 79, 381, 455, 254, 398, 168, 6, 29, 333, 310, 307, 309, 112, 335, 77, 40, 369, 90, 416, 215, 224,
111, 223, 218, 454, 306, 92, 115, 194, 216, 400, 435, 268, 438, 380, 318, 238, 230, 175, 255, 447, 208, 292, 316, 114, 151, 157, 205, 152, 13, 449, 107, 430, 35, 404, 401, 347, 70, 319, 233, 197, 394, 170, 32, 453, 59, 73, 219,
130, 106, 294, 360, 357, 250, 49, 11, 171, 442, 312, 108, 344, 82, 47, 323,
84, 276, 48, 289, 22, 57, 133, 31, 145, 232, 132, 26, 201, 76, 313, 80, 135, 228, 407, 200, 257, 434, 376, 286, 245, 303, 206, 78, 136, 52, 450, 101, 71, 213, 237, 50, 199, 329, 396, 361, 373, 96, 164, 14, 159, 169, 155, 383, 283, 123, 160, 99, 251, 391, 19, 371, 459, 367, 358, 280, 399, 196, 439, 374,
66, 297, 103, 370, 235, 287, 277, 378, 247, 119, 21, 229, 336, 187, 39, 388, 322, 118, 317, 10, 411, 362, 63, 72, 354, 83, 17, 128, 249, 267, 141, 20, 345, 290, 260, 44, 234, 221, 182, 288, 320, 275, 421, 258, 190, 54, 402, 56,
368, 279, 443, 259, 352, 23, 30, 143, 126, 272, 427, 311, 203, 192, 177, 4,
343, 61, 209, 193, 351, 308, 9, 212, 28, 86, 75, 7, 293, 372, 204, 144, 452, 278, 173, 1, 139, 420, 100, 406, 3, 458, 120, 389, 89, 338, 98, 392, 332, 242, 211, 415, 55, 74, 340, 444, 195, 298, 282, 300, 256, 296, 246, 342, 97,
24, 263, 81, 355, 38, 116, 198, 227, 262, 163, 429, 231, 379, 330, 184, 384, 191, 5, 273, 395, 15, 302, 137, 220, 334, 178, 225, 181, 431, 85, 417, 179, 153, 140, 366, 349, 156, 324, 301, 95, 456, 127, 441, 188, 51, 226, 304, 93, 161, 428, 94, 409, 284, 129, 423, 375, 12, 337, 240, 243, 53, 45, 359, 412, 437, 425, 148, 346, 62, 104, 236, 87, 158, 386, 413, 440, 285, 33, 68, 424, 64, 403, 305, 91, 419, 341, 253, 154, 356, 445, 222, 252, 382, 37, 176, 67, 348, 350, 328, 109, 18, 339, 167, 124, 102, 189, 88, 315, 405, 271, 266, 134, 457, 180, 397, 172, 326, 261, 41, 410, 244, 270, 248, 58, 25, 185, 34, 36, 121, 241, 105, 183, 42, 281, 432, 46, 202, 446, 149, 186, 299, 207, 364,
174, 214, 210, 142, 8, 65, 390, 448, 325, 327, 16, 461, 295, 393, 60, 150]
    Report = initReportJson()
    DdjData = ddjData_sql.getStacks()
    enSimpleCode(LisCode,DdjData)
    
test()