#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-02 13:25:10
# @Version : Python2.7
# @Author  : AlanLau
# @Email   : rlalan@outlook.com
# @Blog    : http://blog.csdn.net/AlanConstantineLau

# from reader import readtxt as rt
# from distance import Edit_distance_array as ed
# from statistic import orderdic as od
#import jieba#在源代码的基础上添加分词功能
import random

#######################################
'''
edit_distance(str1, str2):函数说明
计算文本间的距离，原理如下：
文本的每一行为一个列表，通过比较每一行内元素的相同个数来确定两行之间的相似度
'''
def edit_distance(str1, str2):
    str1_len = len(str1) + 1
    str2_len = len(str2) + 1
    matrix = [[0 for col in range(str2_len)] for row in range(str1_len)]
    for i in range(1, str1_len):
        matrix[i][0] = i
    for j in range(1, str2_len):
        matrix[0][j] = j
    for row in range(1, str1_len):
        for col in range(1, str2_len):
            cos = 0
            if str1[row - 1] == str2[col - 1]:
                cos = 0
            else:
                cos = 1
            matrix[row][col] = min(
                matrix[row - 1][col] + 1, matrix[row][col - 1] + 1, matrix[row - 1][col - 1] + cos)
    distance = matrix[-1][-1]
    return int(distance)

'''
clean_data(data)函数说明
数据预处理  文本按照行分类，行内分割

'''
def clean_data(data):
    new_data = {}
    id = 0
    for datum in data:
        id += 1
        datum_list = datum.strip().split()
        new_data[id] = datum_list
    return new_data

'''
similarity(token1, token2)函数说明
找出文本相似度   (0,1)
1-相同元素/max(行一，行二）
'''
def similarity(token1, token2):#文本相似度
    distance = edit_distance(token1, token2)
    return 1.0 - float(distance) / max(len(token1), len(token2))

'''
orderdic(dic, reverse)函数说明
将一个字典内按键倒叙输出
'''
def orderdic(dic, reverse):#倒序输出
    ordered_list = sorted(
        dic.items(), key=lambda item: item[1], reverse=reverse)
    return ordered_list
'''
single_pass(data)函数说明
随机选中一行作为一簇 category为字典，保存分好的簇
对于剩下的每一行与category簇内的行匹配距离，
  如果相似度均小于我的设定值，将该行保存为新的簇保存在category
  如果有一个相似度大于我的设定值，将该行保存在最大的相似度的簇内
根据目前的实验，随机选中的行对于最后结果尚无影响
'''

def single_pass(data):
    sim_sum = 0
    random.seed()#设置种子是为了研究代码
    get_first_point = random.randint(1, len(data))
    #print("sss",get_first_point)
    category = {get_first_point: []}#随机选一行作为已知簇      
    #print(data)
    for datum in data:#遍历文本每一行
        #print("计数",datum)
        if datum == get_first_point:
            continue
        else:
            flag = 1
            sort_sim = {}#其他每一行对应我先选的那一行
            #print (len(category))
            for cate in category:#循环我选中的行，如果够近，就在sort_sim中保存
                sim = similarity(data[cate], data[datum])
                #print("simdzhi",sim)
                if sim > 0.01:
                    sort_sim[cate] = sim
                else:
                    sort_sim[cate] = 0
                    #flag=1
            if max(sort_sim.values())==0:
                flag=0
            
            if flag==0:
                category[datum] = []
                #continue
            else:
                
                sort = orderdic(sort_sim, True)
                category[sort[0][0]].append(datum)
        
    #print(sort_sim)
    return category

#文本读入
def readtxt(path, encoding):
    with open(path, 'r', encoding=encoding) as f:
        lines = f.readlines()
    return lines


def main():
    datapath = r'BPtest.txt'
    data = readtxt(datapath, 'utf8')
    data = clean_data(data)
    print(single_pass(data))
    print(len(single_pass(data)))
    #print(type(data))


if __name__ == '__main__':
    main()
