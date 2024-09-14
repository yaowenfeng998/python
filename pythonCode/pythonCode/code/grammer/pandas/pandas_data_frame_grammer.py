import pandas as pd
import numpy as np

data_by_list = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
data_frame_by_list = pd.DataFrame(data_by_list, columns=['Site', 'Age'])
data_frame_by_list['Site'] = data_frame_by_list['Site'].astype(str)
data_frame_by_list['Age'] = data_frame_by_list['Age'].astype(float)
print(data_frame_by_list)
print(data_frame_by_list.dtypes)

print('====' * 40)

# 通过字段创建data_frame,key自动变成了column_name
data_by_dict = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
data_frame_by_dict = pd.DataFrame(data_by_dict)
print(data_frame_by_dict)
print(data_frame_by_dict.dtypes)

print('====' * 40)

data_by_np_array = np.array([
    ['Google', 10],
    ['Runoob', 12],
    ['Wiki', 13]
])
data_frame_by_array = pd.DataFrame(data_by_np_array, columns=['Site', 'Age'])
print(data_frame_by_array)
print(data_frame_by_array.dtypes)

print('====' * 40)

data_by_list_dict = [
    {'a': 1, 'b': 2, 'c': 3},
    {'a': 5, 'b': 6, 'c': 7},
    {'a': 8, 'b': 9, 'c': 10, 'd': 11}
]
data_frame_by_list_dict = pd.DataFrame(data_by_list_dict)
print(data_frame_by_list_dict)
print(data_frame_by_list_dict.dtypes)

print('====' * 40)
# loc[index] 用于返回指定行 1行 -> series类型 多行-> dataFrame类型
res = data_frame_by_dict.loc[[0, 1]]
print(type(res))
print(res)
print(res.loc[0].iloc[0])
print(res.loc[0].iloc[1])
print(res.loc[1].iloc[0])
print(res.loc[1].iloc[1])
print('====' * 5)
print(res.loc[0, 'Site'])
print(res.loc[0, 'Age'])
print(res.loc[1, 'Site'])
print(res.loc[1, 'Age'])

print('====' * 40)
print(data_frame_by_dict.shape)  # 形状
print(data_frame_by_dict.columns)  # 列名
print(data_frame_by_dict.index)  # 索引
print(data_frame_by_dict.head())  # 前几行数据，默认是前 5 行
print(data_frame_by_dict.tail())  # 后几行数据，默认是后 5 行
print(data_frame_by_dict.info())  # 数据信息
print(data_frame_by_dict.describe())  # 描述统计信息
# print(data_frame_by_dict.mean())    # 求平均值
# print(data_frame_by_dict.sum())     # 求和

print('====' * 40)

# data frame修改 增加一列
data_frame_by_dict['address'] = [10, 11, 12]
# age修改一列
data_frame_by_dict['Age'] = [1, 2, 3]
# 添加新行
data_frame_by_dict.loc[3] = ['tom', 4, 13]
# 合并两个data_frame
now_row = pd.DataFrame({'Site': ['jack'], 'Age': [5], 'address': [14]})
r = pd.concat([data_frame_by_dict, now_row], ignore_index=True)
print(r)

print('====' * 40)
# 删除 行 axis=0  列  axis=1 inplace=True 直接在源data frame上删除 什么都不反悔, 默认 false 返回一个新的data frame 源不变
r.drop('address', axis=1, inplace=True)
print(r)
rr = r.drop('Age', axis=1)
print('====' * 5)
print(r)
print('====' * 5)
print(rr)
print('====' * 5)
# 删除行 直接返回新的data frame
rrr = r.drop(0)
print(rrr)

print('====' * 40)
print(r)
z = r['Age'].sum()
print(z)
print('====' * 5)
zz = r['Age'].mean()
print(zz)

print('====' * 40)
# 重置索引
t = pd.DataFrame({'A': [1, 2, 3]}, index=[2, 4, 6])
print(t)
print('====' * 5)
# 直接返回新的data frame, reset_index 默认参数 drop =false , 保留原始索引列 即index  可通过 name=''指定列名
# drop=true时 不保留原始索引
re_t = t.reset_index()
print(re_t)
print('====' * 5)
r_t = t.reset_index(drop=True)
print(r_t)

print('====' * 40)
data = {'Column1': ['A', 'B', 'C'],
        'Column2': [1, 2, 3],
        'Column3': [4, 5, 6]}
df = pd.DataFrame(data)
print("原始DataFrame:")
print(df)
# 将'Column1'设置为新的索引
df_set = df.set_index('Column1')
print("设置了新索引的DataFrame:")
print(df_set)
print(df_set.loc['B'])

print('====' * 40)
# 布尔表达式过滤data frame
d=df[df['Column2'] >= 2]
print(d)
