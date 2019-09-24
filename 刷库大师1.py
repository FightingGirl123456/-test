#coding=utf-8
import pprint
"""
对初始化结果文件label及其对应值的顺序进行校验：

"""
import json刷库大师
import os

def readLabelCsv(tableNameLabel):
    """
    读 *_label.csv文件，返回这个文件第1行有哪些label和label的个数
    :param tableNameLabel: 表的label模板文件
    :return: labelList-表的lable列表、labelsNum-表的的label数量
    """
    #初始化结果文件label列表和label个数--DEALIN_label.csv
    # openPath1=r'C:\Users\ChinaDaas\Desktop\ORVIAOFL下载文件\20190918_init'
    openPath1=json刷库大师.GKKWNBAPpath
    # openPath1 =r'C:\Users\ChinaDaas\Desktop\1'
    openPath=openPath1+"\\"+tableNameLabel
    with open(openPath,encoding="UTF-8") as f:
        labelList=f.readline().strip().split('#@!')
        labelsNum=len(labelList)
        # print('labelList=',labelList)
        # print('labelsNum=', labelsNum)
    return labelList,labelsNum



def readTableCsv(tableName):
    """
    读 *.csv文件，返回这个文件第1行有哪些值和值的个数
    :param tableName: 按照lable模板记录的表记录文件
    :return: TabRecodeDict-每行表记录的值的字典、TabRecodeNum-表记录的值的个数、OneRecodeValNum-1条记录的值的个数
    """
    # openPath1 = r'C:\Users\ChinaDaas\Desktop\ORVIAOFL下载文件\20190918_init'
    openPath1 = json刷库大师.GKKWNBAPpath
    # openPath1 =r'C:\Users\ChinaDaas\Desktop\1'
    openPath = openPath1 + "\\" + tableName
    TabRecodeDict={} #每个模块的记录字典
    with open(openPath,'r',encoding="UTF-8") as f:
        TabRecodeList=f.readlines()   #每个模块的记录列表.split('#@!')
        TabRecodeNum=len(TabRecodeList)#每个模块的记录数
        for i in range(TabRecodeNum):
            keyName="readline"+str(i)   #字典的key命名
            ValueList=TabRecodeList[i].strip().split('#@!') #模块中每行记录的值的列表
            TabRecodeDict[keyName]=ValueList
            OneRecodeValNum=len(ValueList)
    return (TabRecodeDict,TabRecodeNum,OneRecodeValNum)

#检查label文件与表文件中的值的个数是否1值，一致时并校验其值与json中的值是否1值
def cheackTabJson(tableNameFile,tableNameLabelFile):
    """
    校验生成结果文件与企业查询接口的响应json串的值是否一致
    :param tableNameLabelFile: 表的label模板文件
    :param tableNameFile: 按照lable模板记录的表记录文件
    :return:
    """
    labelList, labelsNum=readLabelCsv(tableNameLabelFile)
    TabRecodeDict, TabRecodeNum,OneRecodeValNum=readTableCsv(tableNameFile)
    TabName=tableNameFile[:-4]
    OneTableRecodes = json刷库大师.jsonDict["ENT_INFO"][TabName]  # json中1个模块表的记录列表或字典
    OneTableRecodesNum = len(json刷库大师.jsonDict["ENT_INFO"][TabName])  # json中1个模块表的记录条数
    if TabName not in ["BASIC", "ENT_HANGYEINFO", "ENT_ZONGHEINFO", "ENT_BIAOSHIINFO", "METADATA"]:
        # 校验列表形式的模块中的字典元素的字段值
        if labelsNum==OneRecodeValNum: #label数量与1条记录的值的数量是否一致
            if TabRecodeNum==OneTableRecodesNum:    #模块中的记录数与json中对应的模块记录数是否一致
                for j in range(TabRecodeNum):    #行
                    for i in range(1,OneRecodeValNum):  #列
                        Fkey=labelList[i]
                        Fvalue=TabRecodeDict["readline"+str(j)][i]
                        # print(j,Fkey,TabName,tableNameLabelFile,labelList)
                        if  OneTableRecodes!=[] and OneTableRecodes[j][Fkey]==Fvalue:
                            print("文件值与json值一致")
                        else:
                            print(f"文件值与json中的值不一致，表名为{TabName}，其key为{Fkey}，json的值{OneTableRecodes[j][Fkey]}，文件中的值{Fvalue}")
    else:
        #校验字典形式的模块中的字段值
        # print(TabRecodeDict)
        for i in range(1,labelsNum):
            Fkey2 = labelList[i]
            if TabRecodeDict["readline0"][i]==OneTableRecodes[Fkey2]:
                print("文件值与json值一致")
            else:
                print(f"文件值与json中的值不一致，表名为{TabName}，其key为{Fkey2}，json的值{OneTableRecodes[Fkey2]}，文件中的值{TabRecodeDict['readline0'][i]}")

def readSysFile(file_dir):
    """
    获取下载的文件有哪些
    :param file_dir: 当前目录路径
    :return: 前路径下所有非目录子文件
    """
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
    fileSort=[] #定义排序是后的文件列表
    for tablefile in files:
        if "_label.csv" not in tablefile:
            fileSort.append(tablefile)
            table_lableFile = tablefile[:-4] + "_label.csv"
            if table_lableFile in files:
                fileSort.append(table_lableFile)
            else:
                print(f"{table_lableFile}文件不存在")
        else:
            continue
    return fileSort

#企业查询的json响应的某个表的label列表和label数
# jsonTableLabels=json刷库大师.jsonDict["ENT_INFO"]["SHAREHOLDER"][0]
# print("jsonTableLabels=",jsonTableLabels)
# print(len(jsonTableLabels))

if __name__=='__main__':

    # ORVIAOFLpath=r'C:\Users\ChinaDaas\Desktop\ORVIAOFL下载文件\20190918_init'
    # GKKWNBAPpath=r'C:\Users\ChinaDaas\Desktop\GKKWNBAP下载文件\20190918_init'
    CSVPath=json刷库大师.GKKWNBAPpath
    filesList = readSysFile(CSVPath)
    # pprint.pprint(filesList)
    for i in range(len(filesList)):
        if i%2==0:   #初始化结果文件夹下的文件顺序：*.csv  , *_label.csv
            print(filesList[i], filesList[i + 1])
            cheackTabJson(filesList[i],filesList[i+1])
        else:
            continue

