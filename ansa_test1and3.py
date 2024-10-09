import os
import sys
third_packages=r"G:\\anaconda3\\envs\\ansa_meta_env\\Lib\\site-packages"
sys.path.append(third_packages)

import ansa
from ansa import *
import numpy as np
import time  # 用于计算程序运行时间

# 选择节点，返回节点ID列表
def pick_nodes():
    print("请在界面中选择节点...")
    selected_nodes = base.PickNodes(constants.LSDYNA, ("NODE",)) # 限定只能选择节点类型
    
    if selected_nodes:
        node_ids = [] # 用于存储所有选中的节点ID
        for node in selected_nodes:
            entity_values = base.GetEntityCardValues(constants.LSDYNA, node, ("NID",)) # 获取每个节点的ID
            node_ids.append(entity_values["NID"]) # 将ID添加到node_ids列表中
        return node_ids # 返回选中的节点ID列表
    else:
        return []  # 如果没有选择节点，返回空列表

#旋转节点并返回旋转的节点ID列表
def rotate_nodes(node_ids, rotation_axis, angle_degrees):
    if not node_ids:  # 如果没有节点ID，返回空列表
        return []
    
    # 归一化旋转轴向量并构建旋转矩阵
    rotation_axis = np.array(rotation_axis) / np.linalg.norm(rotation_axis) # 归一化旋转轴
    ux, uy, uz = rotation_axis # 提取旋转轴的各个分量
    theta = np.radians(angle_degrees) # 将角度从度转换为弧度

    # 构建旋转矩阵罗德里格旋转公式（Rodrigues' rotation formula），可用于将点围绕给定旋转轴旋转指定的角度
        #x轴=[1,0,0]，y轴=[0,1,0], z轴=[0,0,1];旋转角度:正角度按照右手定则，当你围绕 x 轴旋转时，角度向上（从 y 轴转向 z 轴）是正的。
    R = np.array([[np.cos(theta) + ux**2 * (1 - np.cos(theta)),
                   ux*uy * (1 - np.cos(theta)) - uz*np.sin(theta),
                   ux*uz * (1 - np.cos(theta)) + uy*np.sin(theta)],
                  [uy*ux * (1 - np.cos(theta)) + uz*np.sin(theta),
                   np.cos(theta) + uy**2 * (1 - np.cos(theta)),
                   uy*uz * (1 - np.cos(theta)) - ux*np.sin(theta)],
                  [uz*ux * (1 - np.cos(theta)) - uy*np.sin(theta),
                   uz*uy * (1 - np.cos(theta)) + ux*np.sin(theta),
                   np.cos(theta) + uz**2 * (1 - np.cos(theta))]])

    rotated_nodes = []  # 存储成功旋转的节点ID

    # 遍历每个节点并更新其坐标
    for node_id in node_ids:
        node = base.GetEntity(constants.LSDYNA, 'NODE', node_id)
        if node:
            new_coordinates = np.dot(R, np.array(node.position)) # 计算新的旋转坐标
            node.position = new_coordinates # 更新节点的坐标
            rotated_nodes.append(node_id) # 将旋转成功的节点ID添加到rotated_nodes列表中

    return rotated_nodes # 返回旋转的节点ID列表

def main():
    start_time = time.time()  # 记录程序开始时间

    # Step 1: 选择节点
    node_ids = pick_nodes()

    # Step 2: 定义旋转轴和旋转角度
    rotation_axis = [1, 0, 0]  # 围绕x轴旋转
    angle_degrees = 45  # 旋转45度

    # Step 3: 对选中的节点进行旋转
    rotated_nodes = rotate_nodes(node_ids, rotation_axis, angle_degrees)

    # 计算程序总用时间
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"程序运行时间: {elapsed_time:.2f}秒")

    # 输出旋转的节点ID，以逗号分隔
    if rotated_nodes:
        print(f"旋转的节点: {', '.join(map(str, rotated_nodes))}") #map(str, rotated_nodes) 的作用是将每个数字节点ID转换为字符串，结果类似于 ['810001', '810002', '810003']
    else:
        print("没有旋转任何节点。")

# 调用 main 函数进行操作
main()

