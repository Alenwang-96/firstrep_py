########################################################################################################################
'''将labelimg标签紧挨着排列,相邻标签横向最少差1个像素'''
import os,time
import shutil
from xml.etree import ElementTree as ET

path = "E:\\num8\\"  # xml文件存放路径
imgpath = "E:\\AIphoto\\"  # 新的照片path路径
save_imgpath = "E:\\adjust_num8photo\\"  # 修改后的img文件存放路径
save_newxmlpath = "E:\\adjust_num8\\" # 修改后的xml文件存放路径

files = os.listdir(path)  # 读取路径下所有文件名
start_time = time.time()
print('开始时间',start_time)
for xmlFile in files:
    if xmlFile.endswith('.xml'):
        tree = ET.ElementTree(file=path + xmlFile)  # 打开xml文件，送到tree解析
        root = tree.getroot()  # 得到文档元素对象
        num = len(root.findall('object')) # 判断车牌是7位还是8位的
        if num == 8 :
            list1 = []  # 存放修改前、后的xmin
            list2 = []  # 存放修改前、后的xmax
            list3 = [0,0,0,0,0,0,0,0]  # 存放预处理的xmin
            list4 = [0,0,0,0,0,0,0,0]  # 存放预处理的xmax
            for object in root.findall('object'):
                for child in object.iter('bndbox'):
                        list1.append(int(child.find('xmin').text))  #获取原文件中的初始xmin/xmax值
                        list2.append(int(child.find('xmax').text))
            # print(list1)    # 打印修改前的xmin
            # print(list2)    # 打印修改前的xmax
            for i in range(8):  # 可以根据所查询的xmin或xmax的数量自行更改，因为我的源文件中需要修改8处地方的xmin或xmax的值
                a = list1[i]
                b = list2[i]
                if i <= 6:        # 错位比较，相当于数学中的排列组合问题，避免了已经比较过的数值再次进行比较，提高效率
                    for j in range(i+1,8):  # 下面进行判断两个标签是否有重叠部分
                        if list1[j] in range(a,b):
                            c = abs((b-list1[j])/2) # xmin值存在于某个标签所对应的(xmin,xmax)内时，做平均值处理，同时判断差值的平均是否为整数
                            if isinstance(c,int):
                                list4[i] = list2[i] - c
                                list3[j] = list1[j] +c
                            else:
                                d = int(c+0.5)
                                list4[i] = list2[i] - d   # 在判断出哪些xmin和xmax需要改动时，把值放到预处理列表中的对应位置，这很重要
                                list3[j] = list1[j] +d
            for i in range(8):
                if list3[i] != 0 :
                    list1[i] = list3[i]  # 当预处理列表中存在不为0的值时，表明这个位置的xmin或xmax值需要改变，只需要将这个数值对应替换到列表1、2即可
                if list4[i] != 0:
                    list2[i] = list4[i]

            for i in range(8):
                for j in range(8):      # 在使用labelimg制作车牌字母标签时，有时候并不是按照从左到右的顺序依次标记的，所以还需要对列表1、2中的值
                    if list1[i] == list2[j]:    # 进一步判断是否存在相等的值，若相等，则表明标签边界重合，需要进一步处理，边界距离我这里设置为1
                        list1[i] += 1
                        list2[j] -= 1
            # print(list1)
            # print(list2)
            i = 0
            for object in root.findall('object'):    # 最后不要忘了，把修改后的xmin/xmax放回到原来对应的标签内容中去
                if i <= 8:
                    for child in object.iter('bndbox'):
                        child.find('xmin').text = str(list1[i])
                        child.find('xmax').text = str(list2[i])
                        i += 1
            tree.write(save_newxmlpath + xmlFile,encoding='utf8',xml_declaration=False) # 保存修改后的xml文件
            print(xmlFile)

        if num == 7:
            list1 = []  # 存放修改前、后的xmin
            list2 = []  # 存放修改前、后的xmax
            list3 = [0, 0, 0, 0, 0, 0, 0]  # 存放预处理的xmin
            list4 = [0, 0, 0, 0, 0, 0, 0]  # 存放预处理的xmax
            for object in root.findall('object'):
                for child in object.iter('bndbox'):
                    list1.append(int(child.find('xmin').text))  # 获取原文件中的初始xmin/xmax值
                    list2.append(int(child.find('xmax').text))
            # print(list1)  # 打印修改前的xmin
            # print(list2)  # 打印修改前的xmax
            for i in range(7):  # 可以根据所查询的xmin或xmax的数量自行更改，因为我的源文件中需要修改7处地方的xmin或xmax的值
                a = list1[i]
                b = list2[i]
                if i <= 5:  # 错位比较，相当于数学中的排列组合问题，避免了已经比较过的数值再次进行比较，提高效率
                    for j in range(i + 1, 7):  # 下面进行判断两个标签是否有重叠部分
                        if list1[j] in range(a, b):
                            c = abs((b - list1[j]) / 2)  # xmin值存在于某个标签所对应的(xmin,xmax)内时，做平均值处理，同时判断差值的平均是否为整数
                            if isinstance(c, int):
                                list4[i] = list2[i] - c
                                list3[j] = list1[j] + c
                            else:
                                d = int(c + 0.5)
                                list4[i] = list2[i] - d  # 在判断出哪些xmin和xmax需要改动时，把值放到预处理列表中的对应位置，这很重要
                                list3[j] = list1[j] + d
            for i in range(7):
                if list3[i] != 0:
                    list1[i] = list3[i]  # 当预处理列表中存在不为0的值时，表明这个位置的xmin或xmax值需要改变，只需要将这个数值对应替换到列表1、2即可
                if list4[i] != 0:
                    list2[i] = list4[i]

            for i in range(7):
                for j in range(7):  # 在使用labelimg制作车牌字母标签时，有时候并不是按照从左到右的顺序依次标记的，所以还需要对列表1、2中的值
                    if list1[i] == list2[j]:  # 进一步判断是否存在相等的值，若相等，则表明标签边界重合，需要进一步处理，边界距离我这里设置为1
                        list1[i] += 1
                        list2[j] -= 1
            # print(list1)
            # print(list2)
            i = 0
            for object in root.findall('object'):  # 最后不要忘了，把修改后的xmin/xmax放回到原来对应的标签内容中去
                if i <= 6:
                    for child in object.iter('bndbox'):
                        child.find('xmin').text = str(list1[i])
                        child.find('xmax').text = str(list2[i])
                        i += 1
            tree.write(save_newxmlpath + xmlFile,encoding='utf8',xml_declaration=False) # 保存修改后的xml文件
            print(xmlFile)
end_time = time.time()
dur_time = end_time - start_time
print('结束时间',end_time)
print('程序用时',dur_time)
########################################################################################################################