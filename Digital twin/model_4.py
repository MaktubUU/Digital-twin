'''
Date: 2022-04-10 21:06:05
LastEditors: ZSudoku
LastEditTime: 2022-04-17 19:05:37
FilePath: \Digital-twin\Digital twin\model_4.py
入库资产的仿真算法
input:所有入口到交通点，交通点到所有出口的数据结构信息和相关参数，入库编码子序列(a1,a2,a3,……,at)
output:资产到达堆垛机入口的时刻序列(t1,t2,t3,……,tn)
'''

#去重
def delList(L):
    L1 = []
    for i in L:
        if i not in L1:
            L1.append(i)
    return L1

#n个上货点的最短上货频率和资产初始上货时刻
def upLoad():
    
    return 0

#3箱一垛或者是5箱一垛
mod1 = 3
mod2 = 5
inrTime = 4 #叠一次货物运行时长
flodTime = 5 #两次叠箱间的等待时长
lostTime = inrTime + flodTime
#计算上货点的上货频率
def CALCupLoadFre(lostTime,upLoadNum):
    return lostTime*upLoadNum

LisCross = [[[1,3,8.5],[3,4,15]],[[2,3,18],[3,4,15]],[[5,3,20],[3,4,15]]] 

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

LisUpLoadFirstCrossTime = CALCupLoadFirstCrossTime(LisCross)#各个上货点到第一个交汇点的时间

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
            LisupLoadStartTime.append((LisCrossTime[i-1][1] + (i) * lostTime) - LisCrossTime[i][1])
    dir = {}
    for i in range(upLoadNum):
        dir['%s'%(LisCrossTime[i][0])] = LisupLoadStartTime[i]
    tuple = sorted(dir.items(),key=lambda x:x[0]) #按照key的值正序排序
    LisupLoadStartTime = []
    for i in range(upLoadNum):
        LisupLoadStartTime.append(tuple[i][1])
    return LisupLoadStartTime 

#各种类型的上货数量  
LisGoodsNum = [{'0':13,'1':8,'2':6,'3':7,'4':2}]
#上货点分配任务量
def CALCupLoadGoodsNum(upLoadNum,LisGoodsNum):
    LisupLoadGoodsNum = []
    LisTemp = []
    #按照上货点数量对列表进行分割
    for i in range(upLoadNum):
        LisupLoadGoodsNum.append([])
    #获取每种资产的上货数量
    for i in LisGoodsNum[0]:
        #print(LisGoodsNum[0][i])
        LisTemp.append(LisGoodsNum[0][i])
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
        LisupLoadParm[i].append(LisupLoadStartTime[i])
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
    print(LisupLoadParm)
    return LisupLoadTimeLis

#货物到达叠箱机的时间序列(总时间序列)
def CALCupLoadAllTimeLis():
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum)
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisupLoadTimeLis = []
    for i in range(len(LisupLoadGoodsNum)):
        time = 0
        index = 0
        for n in LisupLoadGoodsNum[i]:
            #k = len((LisupLoadGoodsNum[i]))
            for j in range(n):
                time +=  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
                LisupLoadTimeLis.append(time)
            index += 1
    print(LisupLoadParm)
    LisupLoadTimeLis = sorted(LisupLoadTimeLis)
    return LisupLoadTimeLis

def model_4():
    
    return 0

if __name__ == '__main__':
    # CALCupLoadFre(lostTime=lostTime,upLoadNum=2)
    # CALCupLoadTime(LisCrossTime=LisUpLoadFirstCrossTime,upLoadFre=1)
    #print(CALCupLoadSign(LisCross))
    #print(CALCupLoadSameCross(LisCross))
    #print(CALCupLoadCross(LisCross))
    #print(CALCupLoadSameCross(LisCross,CALCupLoadCross(LisCross)))
    upLoadNum=len(LisUpLoadFirstCrossTime)
    # print(CALCupLoadTime(LisUpLoadFirstCrossTime,CALCupLoadFre(lostTime=lostTime,upLoadNum=upLoadNum)))
    # print(CALCupLoadGoodsNum(upLoadNum,LisGoodsNum))
    # print(CALCeachUpLoadNum(upLoadNum=upLoadNum,GoodsNum=13))
    #print(CALCupLoadGoodsNum(upLoadNum,LisGoodsNum))
    #print(CALCupLoadTime(LisCrossTime,upLoadFre,upLoadNum))
    #print(CALCupLoadFirstCrossTime(LisCross))
    print(CALCupLoadAllTimeLis())
    #print(CALCupLoadFirstCrossTime(LisCross))
    #print(CALCupLoadTime())
